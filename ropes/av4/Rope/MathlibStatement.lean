import Rope.MobiusFull
import Rope.MathlibBridge

/-!
# AV4 (Theorem C) in Mathlib vocabulary

`OAI.EuclideanRamsey.Mobius.ramsey_iff_ramsey_mobius_full` restated with no definitions beyond
Mathlib: the points live in `EuclideanSpace ℝ (Fin d)`, "on the unit sphere" is `Metric.sphere`,
"congruent copy" is Mathlib's `Congruent`, the Lorentz form `S = diag(-1, 1, …, 1)` is written as
a `Matrix.diagonal`, and the Möbius image `φ_L x` of a point is written out: the spatial part of
`L (1, x)` divided by its first (`none`) coordinate. OpenAI's `Ramsey` is unfolded by
`oai_ramsey_iff`. `ramsey_iff_ramsey_mobius_nonvacuous` exhibits data meeting every hypothesis.
-/

namespace SphericalRamsey

open Matrix

/-- **AV4 (Theorem C), Mathlib vocabulary.** Let `L` be a real `(1+d) × (1+d)` matrix (indices
`Option (Fin d)`, `none` first) with `Lᵀ S L = S` for `S = diag(-1, 1, …, 1)`, that is `L ∈ O(1,d)`.
For finitely many distinct points `a i` on the unit sphere of `EuclideanSpace ℝ (Fin d)`, `a` is
Euclidean Ramsey iff its image under the Möbius map of `L` is. No spanning hypothesis. -/
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
  have e : ∀ x : EuclideanSpace ℝ (Fin d),
      (fun α : Option (Fin d) => Option.elim α (1 : ℝ) fun k => x k) =
        OAI.EuclideanRamsey.Mobius.aug x := by
    intro x
    funext α
    cases α <;> rfl
  have hb : (fun i => WithLp.toLp 2 fun j : Fin d =>
      (L *ᵥ fun α => Option.elim α 1 fun k => a i k) (some j) /
        (L *ᵥ fun α => Option.elim α 1 fun k => a i k) none) =
      OAI.EuclideanRamsey.Mobius.mobiusMap L ∘ a := by
    funext i
    simp only [Function.comp_apply, OAI.EuclideanRamsey.Mobius.mobiusMap, e (a i)]
  rw [hb]
  exact (oai_ramsey_iff a).symm.trans
    ((OAI.EuclideanRamsey.Mobius.ramsey_iff_ramsey_mobius_full a L hL ha hsph).trans
      (oai_ramsey_iff _))

/-- The hypotheses of `ramsey_iff_ramsey_mobius_mathlib` are satisfiable: the two points `±e₀` of
the line `EuclideanSpace ℝ (Fin 1)` are distinct and lie on the unit sphere,
and `L = 1` satisfies `Lᵀ S L = S`. -/
theorem ramsey_iff_ramsey_mobius_nonvacuous :
    ∃ (a : Fin 2 → EuclideanSpace ℝ (Fin 1)) (L : Matrix (Option (Fin 1)) (Option (Fin 1)) ℝ),
      Lᵀ * Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1) * L =
        Matrix.diagonal (fun α => Option.elim α (-1 : ℝ) fun _ => 1) ∧
      Function.Injective a ∧ (∀ i, a i ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 1)) 1) := by
  have hinj : Function.Injective
      ![EuclideanSpace.single (0 : Fin 1) (1 : ℝ), EuclideanSpace.single 0 (-1)] := by
    intro i j hij
    have h0 := congrArg (fun x : EuclideanSpace ℝ (Fin 1) => x 0) hij
    fin_cases i <;> fin_cases j <;> first | rfl | norm_num at h0
  refine ⟨![EuclideanSpace.single 0 1, EuclideanSpace.single 0 (-1)], 1, by simp, hinj, ?_⟩
  intro i
  fin_cases i <;> simp

end SphericalRamsey
