import Mathlib

/-! Control (weaker) for `SphericalRamsey.ramsey_alg_plus_three_mathlib`: the conclusion without
`Congruent a b`, proved outright (a constant map is monochromatic). Comparator must refuse it. -/

namespace SphericalRamsey

theorem ramsey_alg_plus_three_mathlib {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (ha : Function.Injective a)
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ)
    (T : Finset (Fin s)) (hT : T.card ≤ 3) (halg : ∀ i ∉ T, ∀ j, IsAlgebraic ℚ (a i j)) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        ∃ k : Fin r, ∀ i, χ (b i) = k :=
  fun _ _ => ⟨1, le_rfl, fun χ => ⟨fun _ => 0, χ 0, fun _ => rfl⟩⟩

end SphericalRamsey
