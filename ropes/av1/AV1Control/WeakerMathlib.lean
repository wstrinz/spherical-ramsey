import Mathlib

/-! Control (weaker) for `SphericalRamsey.ramsey_of_algebraic_mathlib`: the conclusion without
`Congruent a b`, proved outright (a constant map is monochromatic). Comparator must refuse it. -/

namespace SphericalRamsey

theorem ramsey_of_algebraic_mathlib {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin d)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        ∃ k : Fin r, ∀ i, χ (b i) = k :=
  fun _ _ => ⟨1, le_rfl, fun χ => ⟨fun _ => 0, χ 0, fun _ => rfl⟩⟩

end SphericalRamsey
