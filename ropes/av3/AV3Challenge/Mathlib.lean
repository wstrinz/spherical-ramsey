import Mathlib

/-! Comparator challenge (rope AV3): the Mathlib-vocabulary statement. No definitions beyond Mathlib. -/

namespace SphericalRamsey

theorem radian_configuration_mathlib (θ : ℝ) (ht : Transcendental ℚ (Real.tan (θ / 2))) :
    let a : Fin 9 → EuclideanSpace ℝ (Fin 2) := fun k =>
      WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]
    Function.Injective a ∧ (∀ k, a k ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) 1) ∧
      ¬ (∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
        ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin 9 → EuclideanSpace ℝ (Fin D),
          Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k) := by
  sorry

theorem radian_ramsey_iff_mathlib (θ : ℝ) :
    let a : Fin 9 → EuclideanSpace ℝ (Fin 2) := fun k =>
      WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]
    Function.Injective a →
      ((∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
          ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin 9 → EuclideanSpace ℝ (Fin D),
            Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k) ↔
        IsAlgebraic ℚ (Real.cos θ) ∧ IsAlgebraic ℚ (Real.sin θ)) := by
  sorry

theorem radian_ramsey_iff_tan_mathlib (θ : ℝ) :
    let a : Fin 9 → EuclideanSpace ℝ (Fin 2) := fun k =>
      WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]
    Function.Injective a →
      ((∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
          ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin 9 → EuclideanSpace ℝ (Fin D),
            Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k) ↔
        IsAlgebraic ℚ (Real.tan (θ / 2))) := by
  sorry

end SphericalRamsey
