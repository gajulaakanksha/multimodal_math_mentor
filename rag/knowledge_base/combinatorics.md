# Permutations, Combinations & Binomial Theorem

## Fundamental Principle of Counting
- If task A can be done in m ways and task B in n ways:
  - Both A AND B: m × n ways
  - A OR B (exclusive): m + n ways

## Factorials
- n! = n × (n-1) × (n-2) × ... × 2 × 1
- 0! = 1
- n! = n × (n-1)!

## Permutations (Order Matters)
- P(n, r) = nPr = n! / (n-r)!
- Circular permutation of n distinct objects: (n-1)!
- Permutations with repetition:
  - n things, where a repeat p times, b repeat q times: n! / (p! × q!)
- All permutations of n objects: n!

## Combinations (Order Doesn't Matter)
- C(n, r) = nCr = n! / [r!(n-r)!]
- nC0 = nCn = 1
- nCr = nC(n-r)
- nCr + nC(r-1) = (n+1)Cr  [Pascal's Identity]

## Binomial Theorem
- (a + b)ⁿ = Σᵣ₌₀ⁿ C(n,r) × aⁿ⁻ʳ × bʳ
- General term: T(r+1) = C(n,r) × aⁿ⁻ʳ × bʳ
- Number of terms: n + 1
- Middle term (n even): T(n/2 + 1) [one middle term]
- Middle terms (n odd): T((n+1)/2) and T((n+3)/2) [two middle terms]

### Special Cases
- (1 + x)ⁿ: coefficient of xʳ is C(n,r)
- Sum of all coefficients: put x=1 → 2ⁿ
- Sum of odd coefficients = Sum of even coefficients = 2ⁿ⁻¹
- (1+x)ⁿ + (1-x)ⁿ: only even power terms remain

## Stars and Bars (Distribution)
- Distributing n identical objects into r distinct bins (any bin can be empty):
  C(n + r - 1, r - 1)
- Distributing n identical objects into r distinct bins (each bin ≥ 1):
  C(n - 1, r - 1)

## Derangements
- D(n) = n! × Σ (-1)ᵏ / k! for k=0 to n
- D(1)=0, D(2)=1, D(3)=2, D(4)=9

## Important Summation Identities
- Σ C(n,r) for r=0 to n = 2ⁿ
- Σ r × C(n,r) = n × 2ⁿ⁻¹
- C(n,0) + C(n,1) + ... = 2ⁿ
