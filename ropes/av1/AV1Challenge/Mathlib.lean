import Mathlib

/-! Comparator challenge (rope AV1): the Mathlib-vocabulary statement. No definitions beyond Mathlib. -/

namespace SphericalRamsey

theorem ramsey_of_algebraic_mathlib {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin d)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k := by
  sorry

theorem ramsey_of_algebraic_nonvacuous :
    ∃ a : Fin 2 → EuclideanSpace ℝ (Fin 1), Function.Injective a ∧
      (∀ i j, IsAlgebraic ℚ (a i j)) ∧
      ∃ (c : EuclideanSpace ℝ (Fin 1)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ := by
  sorry

end SphericalRamsey
