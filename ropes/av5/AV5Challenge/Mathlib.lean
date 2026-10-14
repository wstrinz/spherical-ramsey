import Mathlib

/-! Comparator challenge (rope AV5): the Mathlib-vocabulary statement. No definitions beyond Mathlib. -/

namespace SphericalRamsey

theorem ramsey_alg_plus_three_mathlib {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (ha : Function.Injective a)
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ)
    (T : Finset (Fin s)) (hT : T.card ≤ 3) (halg : ∀ i ∉ T, ∀ j, IsAlgebraic ℚ (a i j)) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k := by
  sorry

theorem ramsey_alg_plus_three_nonvacuous :
    ∃ (a : Fin 2 → EuclideanSpace ℝ (Fin 2)) (T : Finset (Fin 2)), T.Nonempty ∧
      Function.Injective a ∧ (∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) ∧
      T.card ≤ 3 ∧ ∀ i ∉ T, ∀ j, IsAlgebraic ℚ (a i j) := by
  sorry

end SphericalRamsey
