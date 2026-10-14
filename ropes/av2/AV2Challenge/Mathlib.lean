import Mathlib

/-! Comparator challenge (rope AV2): the Mathlib-vocabulary statement. No definitions beyond Mathlib. -/

namespace SphericalRamsey

theorem circle_ramsey_of_le_six_mathlib {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (hs : s ≤ 6) (ha : Function.Injective a)
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k := by
  sorry

theorem circle_ramsey_of_le_six_nonvacuous :
    ∃ a : Fin 6 → EuclideanSpace ℝ (Fin 2), Function.Injective a ∧
      ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ := by
  sorry

end SphericalRamsey
