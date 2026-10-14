import Mathlib

/-!
# Spherical Ramsey conjecture ledger: statement-only Lean stubs

Statement-only Lean stubs for selected entries of the public conjecture ledger
(`ledger/LEDGER.md`). **Every `sorry` here is a conjecture or an unformalized result, never a
proof.** Nothing in this file is used by any rope, and no entry's status depends on it. The status
line above each stub repeats the ledger status; the ledger is authoritative.

* Vocabulary is Mathlib's: `EuclideanSpace ℝ (Fin d)`, Mathlib's `Congruent` (edist),
  `Metric.sphere`, `IsAlgebraic`, `AlgebraicIndependent`, `MeasurableSet`,
  `IntermediateField.adjoin`.
* `IsRamsey` is OpenAI's `OAI.EuclideanRamsey.Ramsey` (openai/math `fd4aeeb2`,
  `Combinatorics/EuclideanRamsey/Model.lean`) unfolded into Mathlib vocabulary. The two are proved
  equivalent in rope AV1 (`ropes/av1`, `oai_ramsey_iff`).
* The non-Mathlib definitions in this file take fewer than 40 lines.

Check: from any Lake project pinned to Lean v4.34.1 and Mathlib `d13f23b7` (for example a rope
directory of this release after its setup), run `lake env lean <path to this file>`. Expected
output: one `declaration uses 'sorry'` warning per stub, and nothing else.

## Public form

For a google-deepmind/formal-conjectures PR, each theorem would become its own file with
`@[category research open, AMS 5 52]` (or `research solved` once a proof is public and accepted);
the definitions would move to `FormalConjecturesForMathlib` with basic API tests.
-/

namespace SphericalRamseyLedger

noncomputable section

open scoped Real

/-- Euclidean space `ℝ^d`. -/
abbrev Space (d : ℕ) := EuclideanSpace ℝ (Fin d)

/-- A finite configuration `a` is **Ramsey** (Erdős et al. 1973; OpenAI's `Ramsey`): for every number
`r ≥ 2` of colours there is a dimension `D ≥ 1` such that every `r`-colouring of `ℝ^D` contains a
monochromatic congruent copy of `a`. -/
def IsRamsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
    ∀ χ : Space D → Fin r, ∃ b : Fin s → Space D, Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k

/-- `a` is **measurably Ramsey**: as `IsRamsey`, but only Lebesgue-measurable colourings are tested
(each colour class is a measurable set). -/
def IsMeasurablyRamsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
    ∀ χ : Space D → Fin r, (∀ k, MeasurableSet (χ ⁻¹' {k})) →
      ∃ b : Fin s → Space D, Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k

/-- `a` lies on some sphere. -/
def IsSpherical {s d : ℕ} (a : Fin s → Space d) : Prop :=
  ∃ (c : Space d) (ρ : ℝ), ∀ i, a i ∈ Metric.sphere c ρ

/-- The field generated over `ℚ` by all coordinates of `a` (OpenAI's `coordinateField`). -/
def coordField {s d : ℕ} (a : Fin s → Space d) : IntermediateField ℚ ℝ :=
  IntermediateField.adjoin ℚ (Set.range fun ij : Fin s × Fin d => a ij.1 ij.2)

/-- A planar point as a complex number. -/
def toC (x : Space 2) : ℂ := ⟨x 0, x 1⟩

/-- The cross-ratio `(z₁ - z₃)(z₂ - z₄) / ((z₁ - z₄)(z₂ - z₃))`. -/
def crossRatio (z₁ z₂ z₃ z₄ : ℂ) : ℂ := (z₁ - z₃) * (z₂ - z₄) / ((z₁ - z₄) * (z₂ - z₃))

/-- All cross-ratios of the points of `a` indexed by `G` are rational. Repeated indices give
`0` or `1`, which are rational, so no distinctness side condition is needed. -/
def RationalCrossRatios {s : ℕ} (a : Fin s → Space 2) (G : Finset (Fin s)) : Prop :=
  ∀ i ∈ G, ∀ j ∈ G, ∀ k ∈ G, ∀ l ∈ G,
    ∃ q : ℚ, crossRatio (toC (a i)) (toC (a j)) (toC (a k)) (toC (a l)) = (q : ℂ)

/-- The Lorentz form `diag(-1, 1, …, 1)` on `ℝ^{1+d}`. -/
def lorentz (d : ℕ) : Matrix (Fin (d + 1)) (Fin (d + 1)) ℝ :=
  Matrix.diagonal fun i => if i = 0 then -1 else 1

/-- The null-cone lift `(1, x)` of a point `x` of `ℝ^d`. -/
def lift {d : ℕ} (x : Space d) : Fin (d + 1) → ℝ := Fin.cons 1 fun j => x j

/-- On the unit sphere, the points `a i` for `i ∈ G` are a Möbius image of a configuration with
algebraic coordinates: some Lorentz matrix `L` carries the null rays of `c i` to those of `a i`.
Möbius maps of `S^{d-1}` are exactly `O(1,d)` acting on null rays; this is the definition used in
the published Möbius-invariance package (mobius-ramsey v1.0.0). -/
def MobiusAlgebraicOn {s d : ℕ} (a : Fin s → Space d) (G : Finset (Fin s)) : Prop :=
  ∃ (c : Fin s → Space d) (L : Matrix (Fin (d + 1)) (Fin (d + 1)) ℝ),
    L.transpose * lorentz d * L = lorentz d ∧
    ∀ i ∈ G, ‖c i‖ = 1 ∧ (∀ j, IsAlgebraic ℚ (c i j)) ∧
      ∃ μ : ℝ, μ ≠ 0 ∧ L.mulVec (lift (c i)) = μ • lift (a i)

/-! ## SR-C5 (M1): measurable Graham. Status: open. -/

/-- **SR-C5 (M1), literal form.** Every finite spherical configuration is Ramsey for measurable
colourings. (The recommended positive-measure form M1w needs Haar measure on `O(D)`; not stubbed.) -/
theorem C5_measurable_graham {s d : ℕ} (a : Fin s → Space d) (ha : IsSpherical a) :
    IsMeasurablyRamsey a := by
  sorry

/-! ## SR-C2: the two-group theorem. Status: proved, `[CERT]` + written glue for `d ≤ 6` and
`[HAND]` for every `d ≥ 2`, reviewed by AI agents only; not formalized. -/

/-- **SR-C2 (two-group theorem).** For `d ≥ 2`, a finite subset of the unit sphere `S^{d-1}` that is
the union of two Möbius images of finite algebraic sets is Ramsey. -/
theorem C2_two_group {s d : ℕ} (hd : 2 ≤ d) (a : Fin s → Space d) (ha : Function.Injective a)
    (hsph : ∀ i, ‖a i‖ = 1) (G H : Finset (Fin s)) (hGH : G ∪ H = Finset.univ)
    (hG : MobiusAlgebraicOn a G) (hH : MobiusAlgebraicOn a H) :
    IsRamsey a := by
  sorry

/-! ## SR-C10: the 8-point radian progression. Status: proved `[HAND]` (via SR-C24 and an exact rank
computation), reviewed by AI agents only; not formalized. -/

/-- The radian progression `k ↦ (cos kθ, sin kθ)`, `k < n`. -/
def radian (n : ℕ) (θ : ℝ) : Fin n → Space 2 :=
  fun k => !₂[Real.cos (k * θ), Real.sin (k * θ)]

/-- **SR-C10.** Eight consecutive radian multiples, if distinct, form a Ramsey set, for every `θ`.
(Nine do not, unless `e^{iθ}` is algebraic: Theorem D, rope AV3.) -/
theorem C10_radian_eight (θ : ℝ) (hinj : Function.Injective (radian 8 θ)) :
    IsRamsey (radian 8 θ) := by
  sorry

/-! ## SR-C13: the naive seven-point classification. Status: refuted `[CERT]`. The stub states the
refutation (the negation of the conjecture); it is not formalized. -/

/-- **SR-C13, refuted.** It is not true that a 7-point subset of the unit circle is Ramsey iff it is
a union of two Möbius images of algebraic sets: the set
`{0, 1/2, 1/3} ∪ {t, t+1, 2t, 1/t}` (stereographic parameters, `t` transcendental) is Ramsey and is
not two-group (`certificates/cert_nontwogroup.py`). -/
theorem C13_refuted :
    ¬ ∀ a : Fin 7 → Space 2, Function.Injective a → (∀ i, ‖a i‖ = 1) →
      (IsRamsey a ↔ ∃ G H : Finset (Fin 7), G ∪ H = Finset.univ ∧
        MobiusAlgebraicOn a G ∧ MobiusAlgebraicOn a H) := by
  sorry

/-! ## SR-C14: rigid-group absorption on the circle. Status: proved `[HAND]` for regular coordinate
fields, reviewed by AI agents only; not formalized. -/

/-- **SR-C14.** Let `a` be finitely many distinct points of the unit circle whose coordinate field is
regular over `ℚ` (every element algebraic over `ℚ` is rational). If some 5 of them have rational
cross-ratios, then `a` is Ramsey iff it is the union of two subsets with rational cross-ratios. -/
theorem C14_rigid_absorption {s : ℕ} (a : Fin s → Space 2) (ha : Function.Injective a)
    (hcirc : ∀ i, ‖a i‖ = 1)
    (hreg : ∀ x ∈ coordField a, IsAlgebraic ℚ x → ∃ q : ℚ, x = q)
    (h5 : ∃ G₀ : Finset (Fin s), 5 ≤ G₀.card ∧ RationalCrossRatios a G₀) :
    IsRamsey a ↔ ∃ G H : Finset (Fin s), G ∪ H = Finset.univ ∧
      RationalCrossRatios a G ∧ RationalCrossRatios a H := by
  sorry

/-! ## SR-C16: Ramsey-ness is not closed under specialization. Status: consistent on sample
(part (a) `[PROBE]`). -/

/-- Stereographic coordinates of a point of the unit sphere `S²` from the pole `(0, 0, 1)`. -/
def stereo (x : Space 3) : Fin 2 → ℝ := fun j => x (Fin.castSucc j) / (1 - x 2)

/-- **SR-C16 (a).** Seven points of `S²` whose fourteen stereographic coordinates are algebraically
independent over `ℚ` form a Ramsey set. With the circle phase diagram (seven independent points on a
great circle are not Ramsey), this would show that Ramsey-ness is not closed under specialization
off the circle. -/
theorem C16_generic_seven_S2 (a : Fin 7 → Space 3) (hsph : ∀ i, ‖a i‖ = 1)
    (hgen : AlgebraicIndependent ℚ fun p : Fin 7 × Fin 2 => stereo (a p.1) p.2) :
    IsRamsey a := by
  sorry

end

end SphericalRamseyLedger
