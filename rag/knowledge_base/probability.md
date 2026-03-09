# Probability — Formulas, Theorems & Rules

## Basic Definitions
- Sample Space (S): set of all possible outcomes
- Event (A): subset of sample space
- P(A) = (favorable outcomes) / (total outcomes)
- 0 ≤ P(A) ≤ 1 always
- P(S) = 1, P(∅) = 0

## Addition Rule
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- If A and B are mutually exclusive: P(A ∪ B) = P(A) + P(B)
- P(Aᶜ) = 1 - P(A) (complement rule)

## Multiplication Rule
- P(A ∩ B) = P(A) × P(B|A) = P(B) × P(A|B)
- If A and B are independent: P(A ∩ B) = P(A) × P(B)

## Conditional Probability
- P(A|B) = P(A ∩ B) / P(B), provided P(B) > 0
- P(B|A) = P(A ∩ B) / P(A), provided P(A) > 0

## Bayes' Theorem
- P(A|B) = [P(B|A) × P(A)] / P(B)
- Extended: P(Aᵢ|B) = [P(B|Aᵢ) × P(Aᵢ)] / [Σ P(B|Aⱼ) × P(Aⱼ)]
- Prior: P(Aᵢ) | Likelihood: P(B|Aᵢ) | Posterior: P(Aᵢ|B)

## Combinatorics
- Permutation: P(n,r) = n! / (n-r)!  [ordered selection]
- Combination: C(n,r) = n! / [r!(n-r)!]  [unordered selection]
- C(n,0) = C(n,n) = 1
- C(n,r) = C(n, n-r)

## Common Probability Problems
### Dice
- Two dice sum = 7: ways = 6, total = 36, P = 1/6
- Two dice sum = 6: ways = 5, total = 36, P = 5/36
- At least one six: P = 1 - (5/6)² = 11/36

### Cards (standard deck of 52)
- P(Ace) = 4/52 = 1/13
- P(Heart) = 13/52 = 1/4
- P(Face card) = 12/52 = 3/13
- P(Red card) = 26/52 = 1/2

### Coins
- n fair coins: P(exactly k heads) = C(n,k) × (1/2)ⁿ
- P(at least one head with n coins) = 1 - (1/2)ⁿ

## Binomial Distribution
- X ~ B(n, p): n trials, p = success probability
- P(X = k) = C(n,k) × pᵏ × (1-p)^(n-k)
- Mean: μ = np
- Variance: σ² = np(1-p)

## Expected Value
- E(X) = Σ [x × P(X = x)]
- E(aX + b) = aE(X) + b
- E(X + Y) = E(X) + E(Y)

## Geometric Probability
- P(X = k) = (1-p)^(k-1) × p  [first success on kth trial]
- E(X) = 1/p

## Common Mistakes in Probability
- Not checking if events are mutually exclusive before adding
- Forgetting to subtract intersection in P(A ∪ B)
- Confusing P(A|B) with P(B|A) (prosecutor's fallacy)
- Assuming independence without verification
