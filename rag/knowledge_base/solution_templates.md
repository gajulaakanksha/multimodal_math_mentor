# Solution Templates for Common Problem Types

## Template 1: Quadratic Equation
**Given**: ax² + bx + c = 0, find x
**Steps**:
1. Calculate D = b² - 4ac
2. If D < 0: No real solutions (state this clearly)
3. If D = 0: x = -b/(2a) [one real root]
4. If D > 0: x = (-b ± √D) / (2a) [two real roots]
5. Verify by substituting back

## Template 2: Optimization (Maxima/Minima)
**Given**: Maximize/minimize f(x) over domain
**Steps**:
1. Find f'(x)
2. Solve f'(x) = 0 to get critical points x₁, x₂, ...
3. Find f''(x)
4. Evaluate f''(xᵢ): if < 0 → local max; if > 0 → local min
5. Evaluate f at critical points AND endpoints of domain
6. State the global max/min with its x-value

## Template 3: Limit Evaluation
**Given**: lim(x→a) f(x)
**Steps**:
1. Try direct substitution
2. If 0/0 or ∞/∞: factor/simplify or apply L'Hôpital
3. If indeterminate form e^0·∞: rewrite as fraction, then apply L'Hôpital
4. Check known standard limit patterns first

## Template 4: Find P(A|B) using Bayes' Theorem
**Given**: P(A), P(B|A), P(B|Aᶜ), find P(A|B)
**Steps**:
1. Calculate P(Aᶜ) = 1 - P(A)
2. Calculate P(B) = P(B|A)·P(A) + P(B|Aᶜ)·P(Aᶜ)  [Total Probability]
3. Apply Bayes': P(A|B) = P(B|A)·P(A) / P(B)

## Template 5: Definite Integration by Substitution
**Given**: ∫ₐᵇ f(g(x))·g'(x) dx
**Steps**:
1. Let u = g(x), then du = g'(x) dx
2. Change limits: when x=a, u=g(a); when x=b, u=g(b)
3. Rewrite integral as ∫ f(u) du from g(a) to g(b)
4. Integrate and substitute limits

## Template 6: Area Between Curves
**Given**: Find area between y = f(x) and y = g(x) from x=a to x=b
**Steps**:
1. Find intersections: f(x) = g(x) → solve for x
2. Determine which function is on top in each sub-interval
3. Area = ∫ₐᵇ |f(x) - g(x)| dx = ∫ₐᵇ [top - bottom] dx

## Template 7: System of Linear Equations (2×2)
**Given**: a₁x + b₁y = c₁, a₂x + b₂y = c₂
**Steps**:
1. Write as matrix: [A|b] where A = [[a₁,b₁],[a₂,b₂]], b = [c₁,c₂]
2. If det(A) ≠ 0: unique solution via Cramer's or matrix inverse
3. If det(A) = 0: check augmented matrix rank for infinite/no solution

## Template 8: Probability with Counting
**Given**: Find probability of specific arrangement/selection
**Steps**:
1. Identify: is order important? (Permutation) or not? (Combination)
2. Count favorable outcomes using P(n,r) or C(n,r)
3. Count total outcomes (sample space)
4. P = favorable / total
5. Check: does answer satisfy 0 ≤ P ≤ 1?

## Template 9:Indefinite Integral Template
**Given**: ∫ f(x) dx
**Steps**:
1. Find antiderivative F(x)
2. Apply integration rules (power rule, substitution, etc.)
3. Add constant +C
4. Answer: F(x) + C

## Template 10:Definite Integral Template
**Given**: ∫ₐᵇ f(x) dx
**Steps**:
1. Find antiderivative F(x)
2. Evaluate F(b)
3. Evaluate F(a)
4. Compute F(b) − F(a)
5. Note: Constant C cancels.