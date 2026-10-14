import Mathlib

/-! Control (weaker) for `SphericalRamsey.circle_ramsey_of_le_six_mathlib`: the conclusion without
`Congruent a b`, proved outright (a constant map is monochromatic). Comparator must refuse it. -/

namespace SphericalRamsey

theorem circle_ramsey_of_le_six_mathlib {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (hs : s ≤ 6) (ha : Function.Injective a)
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        ∃ k : Fin r, ∀ i, χ (b i) = k :=
  fun _ _ => ⟨1, le_rfl, fun χ => ⟨fun _ => 0, χ 0, fun _ => rfl⟩⟩

end SphericalRamsey
