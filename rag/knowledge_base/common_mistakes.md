# Common Mistakes & Pitfalls in JEE Mathematics

## Algebra Mistakes

### Quadratic Equations
- MISTAKE: Forgetting to check if discriminant is negative (leads to complex roots, not real)
- MISTAKE: Taking square root without ± sign: √x² = |x|, not just x
- MISTAKE: Dividing both sides by variable that could be zero (e.g., dividing by x when x=0 is possible)
- CORRECT: Always verify roots by substituting back into original equation
- MISTAKE: Ignoring extraneous roots introduced by squaring both sides

### Logarithms
- MISTAKE: log(a + b) ≠ log(a) + log(b)
- MISTAKE: log(a × b) ≠ log(a) × log(b)  [it's log(a) + log(b)]
- CORRECT: log(a × b) = log(a) + log(b)
- MISTAKE: Solving log(x) = y without checking x > 0 (domain restriction)
- MISTAKE: ln(x²) = 2ln(x) only when x > 0; for all x: ln(x²) = 2ln|x|

### Inequalities
- MISTAKE: Multiplying or dividing by negative number without flipping inequality
- MISTAKE: Not considering all cases when |x| expressions are involved
- CORRECT: When solving |x - a| < b, always write -b < x - a < b

## Calculus Mistakes

### Limits
- MISTAKE: Plugging in directly without checking if 0/0 or ∞/∞ form
- MISTAKE: Applying L'Hôpital's Rule when limit is NOT indeterminate
- MISTAKE: Forgetting that lim sin(x)/x = 1 only as x → 0 (not other values)
- CORRECT: Always simplify first, then apply limit rules

### Derivatives
- MISTAKE: Applying chain rule incorrectly: d/dx[f(g(x))] = f'(g(x))·g'(x), NOT f'(g'(x))
- MISTAKE: Forgetting implicit differentiation when y appears on both sides
- MISTAKE: d/dx[uv] ≠ u'v' (not product of derivatives—use product rule!)
- MISTAKE: Not simplifying derivative before finding critical points
- CORRECT: After finding critical points, always classify using first or second derivative test

### Integration
- MISTAKE: Forgetting +C for indefinite integrals
- MISTAKE: Not changing limits of integration when using substitution in definite integral
- MISTAKE: ∫ 1/x² dx ≠ ln(x²) ; it equals -1/x + C
- CORRECT: ∫ f(x)·g(x) dx ≠ [∫f(x)dx][∫g(x)dx] (no product rule for integrals)

## Probability Mistakes

### Basic Probability
- MISTAKE: Assuming P(A and B) = P(A) × P(B) without verifying independence
- MISTAKE: Confusing "at least one" with "exactly one"
  - P(at least one) = 1 - P(none)
- MISTAKE: Double-counting when using addition rule without subtracting intersection
- CORRECT: Always draw Venn diagram or list sample space for complex problems

### Combinatorics
- MISTAKE: Confusing permutation (order matters) with combination (order doesn't matter)
- MISTAKE: Not dividing by repeated elements in arrangements (e.g., AABB has 4!/(2!2!) arrangements)
- MISTAKE: Off-by-one errors when counting (inclusive vs exclusive ranges)
- CORRECT: nCr = nPr / r! always

## Linear Algebra Mistakes

### Matrices
- MISTAKE: Assuming AB = BA (matrix multiplication is NOT commutative in general)
- MISTAKE: (A+B)² ≠ A² + 2AB + B² in general (unless AB = BA)
- MISTAKE: det(A + B) ≠ det(A) + det(B)
- CORRECT: det(AB) = det(A) × det(B) is valid

### Eigenvalues
- MISTAKE: Confusing null space with eigenspace
- MISTAKE: Assuming n×n matrix always has n distinct eigenvalues (repeated eigenvalues possible)
- CORRECT: det(A - λI) = 0 is always correct starting point

## Domain & Range Checks
- √x is only real for x ≥ 0
- ln(x) is only defined for x > 0
- 1/x is undefined at x = 0
- arcsin(x) and arccos(x) require -1 ≤ x ≤ 1
- tan(x) is undefined at x = π/2 + nπ
- Always state domain restrictions in final answer
