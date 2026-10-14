import Mathlib

/-! Comparator challenge (rope AV4): the Mathlib-vocabulary statement. No definitions beyond Mathlib. -/

namespace SphericalRamsey

open Matrix

theorem ramsey_iff_ramsey_mobius_mathlib {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ)
    (hL : Lᵀ * Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1) * L =
      Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1))
    (ha : Function.Injective a)
    (hsph : ∀ i, a i ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin d)) 1) :
    (∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k) ↔
    (∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent (fun i => WithLp.toLp 2 fun j : Fin d =>
            (L *ᵥ fun α => Option.elim α 1 fun k => a i k) (some j) /
              (L *ᵥ fun α => Option.elim α 1 fun k => a i k) none) b ∧
          ∃ k : Fin r, ∀ i, χ (b i) = k) := by
  sorry

theorem ramsey_iff_ramsey_mobius_nonvacuous :
    ∃ (a : Fin 2 → EuclideanSpace ℝ (Fin 1)) (L : Matrix (Option (Fin 1)) (Option (Fin 1)) ℝ),
      Lᵀ * Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1) * L =
        Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1) ∧
      Function.Injective a ∧ (∀ i, a i ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 1)) 1) := by
  sorry

end SphericalRamsey
