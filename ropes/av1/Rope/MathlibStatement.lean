import Rope.AlgebraicRamsey

/-!
# AV1 in Mathlib vocabulary

`OAI.EuclideanRamsey.ramsey_of_algebraic` restated without OpenAI's definitions: the points live
in `EuclideanSpace ℝ (Fin d)`, "on a sphere" is `Metric.sphere`, and "congruent copy" is
Mathlib's `Congruent` (which compares `edist`, in the order `a`-then-`b`). OpenAI's `Congruent`
(which compares `dist`, in the order `b`-then-`a`) is proved equivalent to Mathlib's
(`oai_congruent_iff`), and OpenAI's `Ramsey` is proved equivalent to the unfolded Mathlib-vocabulary
property (`oai_ramsey_iff`). `ramsey_of_algebraic_nonvacuous` exhibits a configuration meeting
every hypothesis of the theorem.
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

/-- **AV1, Mathlib vocabulary.** A finite configuration of at least two distinct points of
`EuclideanSpace ℝ (Fin d)`, `d ≥ 1`, lying on a sphere, all of whose coordinates are algebraic
over `ℚ`, is Euclidean Ramsey: for every number `r ≥ 2` of colours there is a dimension `D ≥ 1`
such that every `r`-colouring of `EuclideanSpace ℝ (Fin D)` has a monochromatic congruent copy. -/
theorem ramsey_of_algebraic_mathlib {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hsph : ∃ (c : EuclideanSpace ℝ (Fin d)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ) :
    ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
      ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
        Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k :=
  (oai_ramsey_iff a).1 <| OAI.EuclideanRamsey.ramsey_of_algebraic a hs hd ha halg
    (by simpa only [Metric.mem_sphere] using hsph)

/-- The hypotheses of `ramsey_of_algebraic_mathlib` are satisfiable: the two points `±e₀` of the
line `EuclideanSpace ℝ (Fin 1)` are distinct, have algebraic coordinates and lie on the unit
sphere about `0`. -/
theorem ramsey_of_algebraic_nonvacuous :
    ∃ a : Fin 2 → EuclideanSpace ℝ (Fin 1), Function.Injective a ∧
      (∀ i j, IsAlgebraic ℚ (a i j)) ∧
      ∃ (c : EuclideanSpace ℝ (Fin 1)) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ := by
  refine ⟨![EuclideanSpace.single 0 1, EuclideanSpace.single 0 (-1)], ?_, ?_, 0, 1, ?_⟩
  · intro i j hij
    have h0 := congrArg (fun x : EuclideanSpace ℝ (Fin 1) => x 0) hij
    fin_cases i <;> fin_cases j <;> first | rfl | norm_num at h0
  · intro i j
    fin_cases i <;> fin_cases j <;>
      simp [isAlgebraic_one, isAlgebraic_one.neg]
  · intro i
    fin_cases i <;> simp

end SphericalRamsey
