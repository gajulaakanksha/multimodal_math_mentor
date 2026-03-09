# Calculus — Limits, Derivatives & Basic Integration

## Limits

### Standard Limits
- lim(x→0) sin(x)/x = 1
- lim(x→0) (1 - cos x)/x = 0
- lim(x→0) (1 - cos x)/x² = 1/2
- lim(x→0) (eˣ - 1)/x = 1
- lim(x→0) ln(1 + x)/x = 1
- lim(x→∞) (1 + 1/x)ˣ = e
- lim(x→∞) (1 + a/x)ˣ = eᵃ
- lim(x→a) (xⁿ - aⁿ)/(x - a) = nᵃⁿ⁻¹

### L'Hôpital's Rule
- If lim f(x)/g(x) is 0/0 or ∞/∞:
- lim f(x)/g(x) = lim f'(x)/g'(x)
- Apply repeatedly if needed

### Squeeze Theorem
- If g(x) ≤ f(x) ≤ h(x) and lim g(x) = lim h(x) = L, then lim f(x) = L

## Differentiation

### Basic Rules
- d/dx [c] = 0 (constant)
- d/dx [xⁿ] = nxⁿ⁻¹ (power rule)
- d/dx [eˣ] = eˣ
- d/dx [aˣ] = aˣ ln(a)
- d/dx [ln x] = 1/x
- d/dx [log_a x] = 1/(x ln a)

### Trigonometric Derivatives
- d/dx [sin x] = cos x
- d/dx [cos x] = -sin x
- d/dx [tan x] = sec²x
- d/dx [cot x] = -csc²x
- d/dx [sec x] = sec x tan x
- d/dx [csc x] = -csc x cot x
- d/dx [sin⁻¹ x] = 1/√(1-x²)
- d/dx [cos⁻¹ x] = -1/√(1-x²)
- d/dx [tan⁻¹ x] = 1/(1+x²)

### Chain, Product, Quotient Rules
- Chain Rule: d/dx [f(g(x))] = f'(g(x)) × g'(x)
- Product Rule: d/dx [uv] = u'v + uv'
- Quotient Rule: d/dx [u/v] = (u'v - uv') / v²

### Higher-Order Derivatives
- f''(x): concave up if f''(x) > 0, concave down if f''(x) < 0
- Inflection point: f''(x) = 0 (and sign changes)

## Maxima & Minima (Optimization)
1. Find f'(x) = 0 → critical points
2. First Derivative Test: f' changes + → 0 → - means local max; - → 0 → + means local min
3. Second Derivative Test: f''(c) < 0 → local max; f''(c) > 0 → local min
4. Check endpoints for global extrema on closed interval

## Integration

### Basic Integrals
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C, n ≠ -1
- ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C
- ∫ aˣ dx = aˣ/ln(a) + C
- ∫ sin x dx = -cos x + C
- ∫ cos x dx = sin x + C
- ∫ sec²x dx = tan x + C
- ∫ 1/√(1-x²) dx = sin⁻¹x + C
- ∫ 1/(1+x²) dx = tan⁻¹x + C

### Integration Techniques
- Substitution: let u = g(x), du = g'(x) dx
- Integration by Parts: ∫ u dv = uv - ∫ v du
  - ILATE order: Inverse trig, Logarithmic, Algebraic, Trig, Exponential

### Definite Integral Properties
- ∫ₐᵃ f(x) dx = 0
- ∫ₐᵇ f(x) dx = -∫ᵦₐ f(x) dx
- ∫ₐᵇ f(x) dx = ∫ₐᶜ f(x) dx + ∫ᶜᵇ f(x) dx
- ∫₀ᵃ f(x) dx = ∫₀ᵃ f(a-x) dx

## Fundamental Theorem of Calculus
- If F'(x) = f(x), then ∫ₐᵇ f(x) dx = F(b) - F(a)
