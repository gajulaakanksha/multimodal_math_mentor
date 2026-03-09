"""Streamlit UI for Math Mentor."""
import streamlit as st
import os
import json
import uuid
import sys
from PIL import Image
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from inputs.ocr_handler import extract_text_from_image
from inputs.asr_handler import transcribe_audio
from inputs.text_handler import clean_text_input
from agents.orchestrator import run_pipeline
from memory.memory_store import save_feedback

# --- Page Config ---
st.set_page_config(
    page_title="Math Mentor AI",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize session state ---
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "current_extracted_text" not in st.session_state:
    st.session_state.current_extracted_text = ""
if "current_input_mode" not in st.session_state:
    st.session_state.current_input_mode = "Text"
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "hitl_state" not in st.session_state:
    st.session_state.hitl_state = "none" # none, pending, resolved
if "processing" not in st.session_state:
    st.session_state.processing = False


def check_api_key():
    """Verify Groq API key is set."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY", "")
    if key and key != "your_groq_api_key_here":
        st.session_state.api_key_valid = True
    else:
        st.sidebar.error("⚠️ GROQ_API_KEY not found in .env")
        with st.sidebar.expander("How to fix"):
            st.markdown(
                "1. Get a free API key at [Groq Console](https://console.groq.com/keys)\n"
                "2. Edit the `.env` file\n"
                "3. Restart the app"
            )


def handle_process_input(text_to_process: str, mode: str):
    """Run the orchestrator pipeline."""
    if not text_to_process.strip():
        st.warning("Please provide a math problem to solve.")
        return

    st.session_state.processing = True
    st.session_state.pipeline_result = None
    st.session_state.hitl_state = "none"
    
    with st.spinner("🤖 Agents are working on the problem..."):
        try:
            result = run_pipeline(text_to_process, input_mode=mode)
            st.session_state.pipeline_result = result
            
            if result.get("hitl_needed"):
                st.session_state.hitl_state = "pending"
                st.toast("⚠️ Human review requested by agents!", icon="⚠️")
            else:
                st.session_state.hitl_state = "resolved"
                st.toast("✅ Solution generated successfully!", icon="🎉")
                
        except Exception as e:
            st.error(f"Pipeline crashed: {str(e)}")
            
    st.session_state.processing = False


def render_agent_traces(traces: list):
    """Render the agent execution logs."""
    for trace in traces:
        agent_name = trace.get("agent", "Agent")
        status = "✅" if trace.get("success") else "❌"
        with st.expander(f"{status} {agent_name} Log", expanded=False):
            if "input" in trace:
                st.text("Input preview:")
                st.info(trace["input"])
            st.text("Execution steps:")
            for step in trace.get("steps", []):
                st.markdown(f"- {step}")


def render_explanation(exp: dict):
    """Render the final student explanation nicely."""
    st.header(exp.get("title", "Solution"))
    st.write(exp.get("introduction", ""))
    
    for step in exp.get("steps", []):
        st.markdown(f"**Step {step.get('step_number')}: {step.get('title')}**")
        st.info(step.get("explanation"))
        if step.get("formula_used"):
            st.latex(step.get("formula_used"))
        st.success(f"↳ {step.get('result')}")
        st.divider()
        
    st.subheader("🎯 Final Answer")
    st.success(f"**{exp.get('final_answer')}**")
    
    if exp.get("common_mistakes"):
        with st.expander("🛑 Common Mistakes to Avoid"):
            for m in exp.get("common_mistakes"):
                st.error(m)
                
    st.info(f"💡 **Takeaway:** {exp.get('key_takeaway')}")


# --- Main App ---
def main():
    check_api_key()
    
    st.title("📐 Multi-Agent Math Mentor")
    st.markdown("Upload an image, record audio, or type a JEE-style math problem. Watch the agents solve it!")

    if not st.session_state.api_key_valid:
        st.stop()
        
    # --- Input Section ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Input Method")
        mode = st.radio("Select input format:", ["Text", "Image", "Audio"], horizontal=True)
        st.session_state.current_input_mode = mode
        
        extracted_text = ""
        is_low_confidence = False
        
        if mode == "Text":
            raw_text = st.text_area("Type your math problem here:", height=150)
            if st.button("Submit Text", type="primary", disabled=st.session_state.processing):
                res = clean_text_input(raw_text)
                st.session_state.current_extracted_text = res["text"]
                handle_process_input(st.session_state.current_extracted_text, "text")
                
        elif mode == "Image":
            upload = st.file_uploader("Upload textbook photo or screenshot", type=["png", "jpg", "jpeg"])
            if upload is not None:
                st.image(upload, caption="Uploaded Image", use_column_width=True)
                if st.button("Extract Text (OCR)", type="primary", disabled=st.session_state.processing):
                    with st.spinner("Running EasyOCR..."):
                        res = extract_text_from_image(upload.getvalue())
                        st.session_state.current_extracted_text = res["text"]
                        
                        if res["low_confidence"]:
                            st.warning(f"⚠️ Low OCR confidence ({res['confidence']:.0%}). Please review the text below before solving.")
                        else:
                            st.success(f"OCR successful ({res['confidence']:.0%} confidence)")
            
            # Show preview for Image/Audio
            if st.session_state.current_extracted_text and mode == "Image":
                st.subheader("Review Extracted Text")
                edited_text = st.text_area("Correct any OCR mistakes here:", value=st.session_state.current_extracted_text, height=100)
                if st.button("Solve Problem", type="primary"):
                    st.session_state.current_extracted_text = edited_text
                    handle_process_input(edited_text, "image")
                    
        elif mode == "Audio":
            st.write("🎤 **Record or Upload Question**")
            # 1. Live Recording
            audio_data = st.audio_input("Speak your math problem:")
            
            # 2. File Upload (Alternative)
            upload = st.file_uploader("Or upload an audio file", type=["wav", "mp3", "m4a"])
            
            audio_to_process = None
            source_name = ""
            
            if audio_data is not None:
                audio_to_process = audio_data.getvalue()
                source_name = "recording.wav"
            elif upload is not None:
                audio_to_process = upload.getvalue()
                source_name = upload.name
                st.audio(upload)

            if audio_to_process is not None:
                if st.button("Transcribe & Solve", type="primary", disabled=st.session_state.processing):
                    with st.spinner("Running Whisper ASR..."):
                        res = transcribe_audio(audio_to_process, file_extension=source_name.split('.')[-1])
                        st.session_state.current_extracted_text = res["text"]
                        
                        if res["low_confidence"]:
                            st.warning(f"⚠️ Low audio confidence ({res['confidence']:.0%}). Please review.")
                        else:
                            st.success("Transcription successful!")
                            
            if st.session_state.current_extracted_text and mode == "Audio":
                st.subheader("Review Transcript")
                edited_text = st.text_area("Correct any transcription mistakes here:", value=st.session_state.current_extracted_text, height=100)
                if st.button("Solve Problem", type="primary"):
                    st.session_state.current_extracted_text = edited_text
                    handle_process_input(edited_text, "audio")

    # --- Results & HITL Section ---
    with col2:
        st.subheader("2. Solution & Agents")
        
        res = st.session_state.pipeline_result
        if not res:
            st.info("Results will appear here once you submit a problem.")
            return

        # HITL Flow
        if st.session_state.hitl_state == "pending":
            st.error(f"🛑 **Human-In-The-Loop Triggered**\n\nReason: {res.get('hitl_reason')}")
            
            st.markdown("### Agent Progress Before Pause:")
            if res.get("parsed_problem"):
                with st.expander("Parsed Problem Context"):
                    st.json(res["parsed_problem"])
            if res.get("solution"):
                with st.expander("Proposed Solution (Unverified)"):
                    st.write(res["solution"].get("final_answer", "No answer generated"))
                    
            st.markdown("### How would you like to proceed?")
            
            new_text = st.text_area("Edit problem text & try again:", value=st.session_state.current_extracted_text)
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔄 Retry with Edited Text"):
                    handle_process_input(new_text, st.session_state.current_input_mode)
            with col_b:
                if st.button("⚠️ Force Accept Solution Anyway"):
                    st.session_state.hitl_state = "resolved"
                    st.rerun()
            return
            
        # Normal Display Pattern
        if st.session_state.hitl_state == "resolved":
            # 1. Answer display
            if res.get("explanation"):
                render_explanation(res["explanation"])
            else:
                st.error("Failed to generate explanation.")
                
            # 2. Feedback metrics
            st.divider()
            fcol1, fcol2, fcol3 = st.columns(3)
            with fcol1:
                conf = res.get("verification", {}).get("confidence", 0)
                st.metric("Verifier Confidence", f"{conf:.0%}")
            with fcol2:
                if st.button("✅ Mark as Correct"):
                    save_feedback(res.get("problem_id"), "correct", "")
                    st.toast("Feedback saved for memory learning!")
            with fcol3:
                if st.button("❌ Mark as Incorrect"):
                    save_feedback(res.get("problem_id"), "incorrect", "User flagged error")
                    st.toast("Error noted for future learning")

            # 3. Agent traces & Memory
            st.divider()
            st.subheader("Behind the Scenes")
            tabs = st.tabs(["Agent Traces", "Retrieved Context", "Memory Used"])
            
            with tabs[0]:
                render_agent_traces(res.get("agent_traces", []))
                
            with tabs[1]:
                chunks = res.get("retrieved_chunks", [])
                if chunks:
                    for i, c in enumerate(chunks):
                        st.markdown(f"**Source: {c['source']}** (Score: {c['score']:.2f})")
                        st.caption(c['text'])
                        st.divider()
                else:
                    st.info("No relevant formulas extracted from KB.")
                    
            with tabs[2]:
                mems = res.get("memory_results", [])
                if mems:
                    for m in mems:
                        st.markdown(f"**Similar Problem** (Similarity: {m.get('similarity', 0):.2f})")
                        st.write(m.get("input_text"))
                        st.success(f"Past Answer: {m.get('answer')}")
                else:
                    st.info("No similar past problems found in SQLite memory.")


if __name__ == "__main__":
    main()
