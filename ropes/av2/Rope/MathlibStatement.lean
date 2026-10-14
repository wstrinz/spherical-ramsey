import Rope.SixPoint

/-!
# AV2 in Mathlib vocabulary

`OAI.EuclideanRamsey.circle_ramsey_of_le_six` restated without OpenAI's definitions: the points
live in `EuclideanSpace ℝ (Fin 2)`, "on a circle" is `Metric.sphere`, and "congruent copy" is
Mathlib's `Congruent` (which compares `edist`, in the order `a`-then-`b`).

`oai_congruent_iff` and `oai_ramsey_iff` are rope AV1's vocabulary bridge
(`ropes/av1/Rope/MathlibStatement.lean`), with the same statements and proofs: OpenAI's
`Congruent` (`dist`, order `b`-then-`a`) is Mathlib's, and OpenAI's `Ramsey` is the unfolded
Mathlib-vocabulary property. `circle_ramsey_of_le_six_nonvacuous` exhibits six distinct points on
a circle, so the case `s = 6` of the theorem is not vacuous.
-/

namespace SphericalRamsey

/-- OpenAI's `Congruent` (`dist (b i) (b j) = dist (a i) (a j)`) is Mathlib's `Congruent`
(`edist (a i) (a j) = edist (b i) (b j)`). -/
theorem oai_congruent_iff {s d D : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (b : Fin s → EuclideanSpace ℝ (Fin D)) :
    OAI.EuclideanRamsey.Congruent a b ↔ Congruent a b := by
  rw [congruent_iff_dist_eq]
  exact forall₂_congr fun _ _ => eq_comm

/-- OpenAI's `Ramsey`, unfolded into Mathlib vocabulary. -/
theorem oai_ramsey_iff {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d)) :
    OAI.EuclideanRamsey.Ramsey a ↔
      ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
        ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
          Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k := by
  unfold OAI.EuclideanRamsey.Ramsey
  simp only [oai_congruent_iff]

/-- **AV2, Mathlib vocabulary.** Any at most six distinct points on a circle of the Euclidean
plane form a Euclidean Ramsey configuration: for every number `r ≥ 2` of colours there is a
dimension `D ≥ 1` such that every `r`-colouring of `EuclideanSpace ℝ (Fin D)` has a monochromatic
congruent copy. No condition on the coordinates. -/
theorem circle_ramsey_of_le_six_mathlib {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (hs : s ≤ 6) (ha : Function.Injective a)
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k :=
  (oai_ramsey_iff a).1 <| OAI.EuclideanRamsey.circle_ramsey_of_le_six a hs ha hsph

/-- The hypotheses of `circle_ramsey_of_le_six_mathlib` are satisfiable with `s = 6`: the points
`(±1, 0)`, `(0, ±1)`, `(3/5, 4/5)` and `(-3/5, -4/5)` are distinct and lie on the unit circle
about `0`. -/
theorem circle_ramsey_of_le_six_nonvacuous :
    ∃ a : Fin 6 → EuclideanSpace ℝ (Fin 2), Function.Injective a ∧
      ∃ (c : EuclideanSpace ℝ (Fin 2)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ := by
  let x : Fin 6 → ℝ := ![1, -1, 0, 0, 3 / 5, -3 / 5]
  let y : Fin 6 → ℝ := ![0, 0, 1, -1, 4 / 5, -4 / 5]
  refine ⟨fun i => WithLp.toLp 2 ![x i, y i], ?_, 0, 1, ?_⟩
  · intro i j hij
    have h0 := congrArg (fun p : EuclideanSpace ℝ (Fin 2) => p 0) hij
    have h1 := congrArg (fun p : EuclideanSpace ℝ (Fin 2) => p 1) hij
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    fin_cases i <;> fin_cases j <;> simp [x, y] at h0 h1 ⊢ <;> linarith
  · intro i
    rw [mem_sphere_zero_iff_norm, EuclideanSpace.norm_eq, Real.sqrt_eq_one, Fin.sum_univ_two]
    fin_cases i <;> norm_num [x, y, Real.norm_eq_abs, sq_abs]

end SphericalRamsey
