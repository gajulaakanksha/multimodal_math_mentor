# Linear Algebra — Matrices, Determinants & Systems

## Matrices

### Basic Definitions
- Matrix: rectangular array of numbers; m×n means m rows, n columns
- Square matrix: m = n
- Identity matrix (I): diagonal 1s, off-diagonal 0s; AI = IA = A
- Zero matrix: all entries zero

### Matrix Operations
- Addition: (A + B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ (same dimensions required)
- Scalar multiplication: (cA)ᵢⱼ = c·Aᵢⱼ
- Matrix multiplication: (AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ (A is m×p, B is p×n → AB is m×n)
- Transpose: (Aᵀ)ᵢⱼ = Aⱼᵢ

### Properties
- (AB)ᵀ = BᵀAᵀ
- (A + B)ᵀ = Aᵀ + Bᵀ
- (AB)⁻¹ = B⁻¹A⁻¹
- Matrix multiplication is NOT generally commutative (AB ≠ BA)

## Determinants

### 2×2 Determinant
- det([a b; c d]) = ad - bc

### 3×3 Determinant (expansion along first row)
- det(A) = a₁₁(a₂₂a₃₃ - a₂₃a₃₂) - a₁₂(a₂₁a₃₃ - a₂₃a₃₁) + a₁₃(a₂₁a₃₂ - a₂₂a₃₁)

### Determinant Properties
- det(AB) = det(A) × det(B)
- det(Aᵀ) = det(A)
- det(cA) = cⁿ det(A) for n×n matrix
- If any row/column is zero: det = 0
- If two rows/columns are equal: det = 0
- Row swap: det sign flips
- A is invertible ⟺ det(A) ≠ 0

## Matrix Inverse
- A⁻¹ = adj(A) / det(A)
- For 2×2: [a b; c d]⁻¹ = (1/(ad-bc)) × [d -b; -c a]
- AA⁻¹ = A⁻¹A = I

## Eigenvalues & Eigenvectors
- Definition: Av = λv (v ≠ 0)
- Characteristic equation: det(A - λI) = 0
- Eigenvalues are roots of characteristic polynomial
- For each eigenvalue λ, eigenvector v satisfies (A - λI)v = 0

### Properties of Eigenvalues
- Trace(A) = Σ eigenvalues = sum of diagonal entries
- det(A) = product of eigenvalues
- Eigenvalues of A² are λ² (same eigenvectors)
- Eigenvalues of A⁻¹ are 1/λ

## Systems of Linear Equations
- System Ax = b
  - Unique solution: det(A) ≠ 0 → x = A⁻¹b
  - No solution: inconsistent
  - Infinite solutions: det(A) = 0 and consistent

### Cramer's Rule (for n×n non-singular A)
- xᵢ = det(Aᵢ) / det(A)
- Aᵢ: replace i-th column of A with b

### Gaussian Elimination
- Convert to row echelon form (REF) via row operations
- Back-substitute to find solution
- Row operations: swap rows, scale row, add multiple of one row to another

## Rank
- Rank(A) = number of linearly independent rows (or columns)
- For m×n matrix: rank ≤ min(m, n)
- rank(A) + nullity(A) = n (rank-nullity theorem)

## Special Matrices
- Symmetric: A = Aᵀ → real eigenvalues
- Orthogonal: AᵀA = I → eigenvalues ±1, det = ±1
- Diagonal: Dᵢⱼ = 0 for i ≠ j → eigenvalues are diagonal entries
