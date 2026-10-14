import Mathlib

/-! Control (weaker) for `SphericalRamsey.ramsey_iff_ramsey_mobius_mathlib`: the same hypotheses, but the
right-hand side is the Ramsey property of `a` itself instead of its Möbius image, proved outright
(`Iff.rfl`). Comparator must refuse it. -/

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
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k) :=
  Iff.rfl

end SphericalRamsey
