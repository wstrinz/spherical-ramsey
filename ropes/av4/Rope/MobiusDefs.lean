import OAI.Combinatorics.EuclideanRamsey.Model

/-!
# AV4 (Theorem C): Möbius maps of the unit sphere through the Lorentz group

Real-matrix geometry only (no tensor products). Points are OAI's `Space d`, and the augmented
vector `(1, x)` is indexed by `Option (Fin d)` exactly as in OAI's `augmented` / `realAugmented`
(`none` is the extra coordinate).

**Fidelity.** A Möbius (conformal) transformation of the unit sphere `S^{d-1}` is modelled as
`mobiusMap L` for a matrix `L` with `Lᵀ S L = S`, `S = diag(-1, 1, …, 1)` (that is, `L ∈ O(1,d)`).
`L` acts on null lines of `S`, and the null line of `(1, x)` meets the affine chart
`{v_none = 1}` in `(1, mobiusMap L x)`. That these maps are exactly the Möbius group of
`S^{d-1}` (`PO(1,d) ≅ Möb(S^{d-1})`) is the classical identification (cited in the note) and is
**not** proved here. Both signs `±L` give the same map; no time-orientation condition is needed.
-/

namespace OAI
noncomputable section
namespace EuclideanRamsey
namespace Mobius

open Matrix

variable {d : ℕ}

/-- The Lorentz form `S = diag(-1, 1, …, 1)` on `ℝ^{1+d}`, indexed by `Option (Fin d)`. -/
def lorentzForm (d : ℕ) : Matrix (Option (Fin d)) (Option (Fin d)) ℝ :=
  Matrix.diagonal fun α => Option.elim α (-1) fun _ => 1

/-- The augmented vector `(1, x)`, as OAI's `realAugmented`. -/
def aug (x : Space d) : Option (Fin d) → ℝ
  | none => 1
  | some j => x j

/-- The point map of `L ∈ O(1,d)` on the unit sphere: the spatial part of `L (1, x)` divided by
its `none` coordinate (nonzero on the sphere, `time_ne_zero`). -/
def mobiusMap (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ) (x : Space d) : Space d :=
  WithLp.toLp 2 fun j => (L *ᵥ aug x) (some j) / (L *ᵥ aug x) none

/-- No nonzero affine function `w_none + Σ w_j x_j` vanishes on every point. -/
def Nondeg {s : ℕ} (a : Fin s → Space d) : Prop :=
  ∀ w : Option (Fin d) → ℝ, (∀ i, w ⬝ᵥ aug (a i) = 0) → w = 0

local notation "S" => lorentzForm d

theorem lorentzForm_mul_self : S * S = 1 := by
  rw [lorentzForm, diagonal_mul_diagonal, ← diagonal_one]
  congr 1
  funext α
  cases α <;> simp

theorem lorentzForm_transpose : Sᵀ = S := diagonal_transpose _

theorem quad_lorentz (v : Option (Fin d) → ℝ) :
    v ⬝ᵥ S *ᵥ v = -(v none) ^ 2 + ∑ j, v (some j) ^ 2 := by
  simp [lorentzForm, mulVec_diagonal, dotProduct, Fintype.sum_option, sq]

theorem quad_aug (x : Space d) : aug x ⬝ᵥ S *ᵥ aug x = ‖x‖ ^ 2 - 1 := by
  rw [quad_lorentz, EuclideanSpace.real_norm_sq_eq]
  simp only [aug]
  ring

theorem aug_injective {x y : Space d} (h : aug x = aug y) : x = y :=
  PiLp.ext fun j => congrFun h (some j)

theorem dot_aug (w : Option (Fin d) → ℝ) (x : Space d) :
    w ⬝ᵥ aug x = w none + ∑ j, w (some j) * x j := by
  simp [dotProduct, Fintype.sum_option, aug]

variable {L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ}

theorem quad_mulVec (hL : Lᵀ * S * L = S) (v : Option (Fin d) → ℝ) :
    (L *ᵥ v) ⬝ᵥ S *ᵥ (L *ᵥ v) = v ⬝ᵥ S *ᵥ v := by
  rw [mulVec_mulVec, dotProduct_mulVec, ← vecMul_transpose, vecMul_vecMul, ← dotProduct_mulVec,
    ← Matrix.mul_assoc, hL]

/-- The inverse of a Lorentz matrix is `S Lᵀ S`. -/
theorem inv_mul (hL : Lᵀ * S * L = S) : (S * Lᵀ * S) * L = 1 := by
  rw [show S * Lᵀ * S * L = S * (Lᵀ * S * L) by simp only [Matrix.mul_assoc], hL,
    lorentzForm_mul_self]

theorem mul_inv (hL : Lᵀ * S * L = S) : L * (S * Lᵀ * S) = 1 :=
  mul_eq_one_comm.mp (inv_mul hL)

theorem inv_lorentz (hL : Lᵀ * S * L = S) : (S * Lᵀ * S)ᵀ * S * (S * Lᵀ * S) = S := by
  have h1 : L * S * Lᵀ * S = 1 := by
    rw [← mul_inv hL]; simp only [Matrix.mul_assoc]
  have h2 : L * S * Lᵀ = S := by
    calc L * S * Lᵀ = L * S * Lᵀ * S * S := by
          rw [Matrix.mul_assoc (L * S * Lᵀ), lorentzForm_mul_self, Matrix.mul_one]
      _ = S := by rw [h1, Matrix.one_mul]
  rw [transpose_mul, transpose_mul, transpose_transpose, lorentzForm_transpose]
  have e : S * (L * S) * S * (S * Lᵀ * S) = S * (L * (S * S) * S * Lᵀ) * S := by
    simp only [Matrix.mul_assoc]
  rw [e, lorentzForm_mul_self, Matrix.mul_one, h2, lorentzForm_mul_self, Matrix.one_mul]

theorem time_ne_zero (hL : Lᵀ * S * L = S) {x : Space d} (hx : ‖x‖ = 1) :
    (L *ᵥ aug x) none ≠ 0 := by
  intro h0
  have hq := quad_mulVec hL (aug x)
  rw [quad_aug, hx, quad_lorentz, h0] at hq
  have hsum : ∑ j, (L *ᵥ aug x) (some j) ^ 2 = 0 := by linarith
  have hall : ∀ j, (L *ᵥ aug x) (some j) = 0 := fun j =>
    pow_eq_zero_iff two_ne_zero |>.mp
      ((Finset.sum_eq_zero_iff_of_nonneg (fun _ _ => sq_nonneg _)).mp hsum j (Finset.mem_univ _))
  have hv : L *ᵥ aug x = 0 := by
    funext α
    cases α with
    | none => exact h0
    | some j => exact hall j
  have h1 : aug x = (S * Lᵀ * S) *ᵥ (L *ᵥ aug x) := by
    rw [mulVec_mulVec, inv_mul hL, one_mulVec]
  rw [hv, mulVec_zero] at h1
  have := congrFun h1 none
  simp [aug] at this

/-- Theorem C, proof: `L (1, x) = μ (1, φ_L x)` with `μ ≠ 0`. -/
theorem mulVec_aug (hL : Lᵀ * S * L = S) {x : Space d} (hx : ‖x‖ = 1) :
    L *ᵥ aug x = (L *ᵥ aug x) none • aug (mobiusMap L x) := by
  have h0 := time_ne_zero hL hx
  funext α
  cases α with
  | none => simp [aug]
  | some j =>
    simp only [Pi.smul_apply, smul_eq_mul, aug, mobiusMap]
    field_simp

theorem norm_mobiusMap (hL : Lᵀ * S * L = S) {x : Space d} (hx : ‖x‖ = 1) :
    ‖mobiusMap L x‖ = 1 := by
  have h0 := time_ne_zero hL hx
  have hq := quad_mulVec hL (aug x)
  rw [mulVec_aug hL hx, mulVec_smul, dotProduct_smul, smul_dotProduct, quad_aug, quad_aug, hx]
    at hq
  simp only [smul_eq_mul] at hq
  have h2 : ‖mobiusMap L x‖ ^ 2 = 1 := by
    have : ((L *ᵥ aug x) none * (L *ᵥ aug x) none) * (‖mobiusMap L x‖ ^ 2 - 1) = 0 := by
      linarith
    rcases mul_eq_zero.mp this with h | h
    · exact absurd (mul_self_eq_zero.mp h) h0
    · linarith
  have hn := norm_nonneg (mobiusMap L x)
  nlinarith

/-- `φ_N ∘ φ_L = id` on the sphere when `N L = 1`. -/
theorem mobiusMap_left_inv {N : Matrix (Option (Fin d)) (Option (Fin d)) ℝ}
    (hN : Nᵀ * S * N = S) (hL : Lᵀ * S * L = S) (hNL : N * L = 1) {x : Space d}
    (hx : ‖x‖ = 1) : mobiusMap N (mobiusMap L x) = x := by
  have hy := norm_mobiusMap hL hx
  have e1 := mulVec_aug hL hx
  have e2 := mulVec_aug hN hy
  have h : aug x = ((L *ᵥ aug x) none * (N *ᵥ aug (mobiusMap L x)) none) •
      aug (mobiusMap N (mobiusMap L x)) := by
    calc aug x = N *ᵥ (L *ᵥ aug x) := by rw [mulVec_mulVec, hNL, one_mulVec]
      _ = N *ᵥ ((L *ᵥ aug x) none • aug (mobiusMap L x)) := congrArg (N *ᵥ ·) e1
      _ = (L *ᵥ aug x) none • (N *ᵥ aug (mobiusMap L x)) := by rw [mulVec_smul]
      _ = (L *ᵥ aug x) none • ((N *ᵥ aug (mobiusMap L x)) none •
          aug (mobiusMap N (mobiusMap L x))) := congrArg _ e2
      _ = _ := smul_smul _ _ _
  have hc := congrFun h none
  simp only [aug, Pi.smul_apply, smul_eq_mul, mul_one] at hc
  rw [← hc, one_smul] at h
  exact (aug_injective h).symm

/-- `φ_L` is injective on the sphere. -/
theorem mobiusMap_injOn (hL : Lᵀ * S * L = S) {x y : Space d} (hx : ‖x‖ = 1) (hy : ‖y‖ = 1)
    (h : mobiusMap L x = mobiusMap L y) : x = y := by
  rw [← mobiusMap_left_inv (inv_lorentz hL) hL (inv_mul hL) hx,
    ← mobiusMap_left_inv (inv_lorentz hL) hL (inv_mul hL) hy, h]

/-! ## Affine span and nondegeneracy -/

theorem nondeg_of_span {s : ℕ} {a : Fin s → Space d}
    (hspan : affineSpan ℝ (Set.range a) = ⊤) : Nondeg a := by
  intro w hw
  let ℓ : Space d →ₗ[ℝ] ℝ :=
    { toFun := fun x => ∑ j, w (some j) * x j
      map_add' := by
        intro x y
        simp only [PiLp.add_apply, mul_add, Finset.sum_add_distrib]
      map_smul' := by
        intro c x
        simp only [PiLp.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
        exact Finset.sum_congr rfl fun j _ => by ring }
  let f : Space d →ᵃ[ℝ] ℝ := ℓ.toAffineMap + AffineMap.const ℝ (Space d) (w none)
  have hf : ∀ x, f x = w ⬝ᵥ aug x := by
    intro x
    rw [dot_aug]
    simp only [f, ℓ, AffineMap.coe_add, Pi.add_apply, LinearMap.coe_toAffineMap,
      AffineMap.const_apply, LinearMap.coe_mk, AddHom.coe_mk]
    ring
  have h0 : f = AffineMap.const ℝ (Space d) (0 : ℝ) := by
    apply AffineMap.ext_on hspan
    rintro _ ⟨i, rfl⟩
    simp [hf, hw i]
  have hz := congrArg (fun g : Space d →ᵃ[ℝ] ℝ => g 0) h0
  simp only [hf, AffineMap.const_apply, dot_aug] at hz
  simp only [PiLp.zero_apply, mul_zero, Finset.sum_const_zero, add_zero] at hz
  funext α
  cases α with
  | none => exact hz
  | some j =>
    have h1 := congrArg (fun g : Space d →ᵃ[ℝ] ℝ => g (EuclideanSpace.single j 1)) h0
    simp only [hf, AffineMap.const_apply, dot_aug, hz, zero_add] at h1
    simpa [EuclideanSpace.single_apply] using h1

theorem span_of_nondeg {s : ℕ} {a : Fin s → Space d} (i₀ : Fin s) (h : Nondeg a) :
    affineSpan ℝ (Set.range a) = ⊤ := by
  by_contra hne
  set A := affineSpan ℝ (Set.range a)
  have hmem : ∀ i, a i ∈ A := fun i => subset_affineSpan ℝ _ (Set.mem_range_self i)
  have hdir : A.direction ≠ ⊤ := fun ht =>
    hne ((AffineSubspace.direction_eq_top_iff_of_nonempty ⟨a i₀, hmem i₀⟩).mp ht)
  have hperp : A.directionᗮ ≠ ⊥ := fun hb => hdir (Submodule.orthogonal_eq_bot_iff.mp hb)
  obtain ⟨u, hu, hu0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hperp
  let w : Option (Fin d) → ℝ := fun
    | none => -∑ j, u j * a i₀ j
    | some j => u j
  have hw : ∀ i, w ⬝ᵥ aug (a i) = 0 := by
    intro i
    have hi : inner ℝ (a i - a i₀) u = (0 : ℝ) :=
      Submodule.inner_right_of_mem_orthogonal (AffineSubspace.vsub_mem_direction (hmem i)
        (hmem i₀)) hu
    rw [dot_aug]
    simp only [w]
    simp only [PiLp.inner_apply, PiLp.sub_apply, RCLike.inner_apply, conj_trivial] at hi
    have : ∑ j, u j * a i j - ∑ j, u j * a i₀ j = 0 := by
      rw [← Finset.sum_sub_distrib, ← hi]
      exact Finset.sum_congr rfl fun j _ => by ring
    linarith
  have := congrFun (h w hw)
  apply hu0
  exact PiLp.ext fun j => this (some j)

/-- Theorem C, proof, in the dual form: nondegeneracy is preserved by `φ_L`. -/
theorem nondeg_mobius (hL : Lᵀ * S * L = S) {s : ℕ} {a : Fin s → Space d}
    (hsph : ∀ i, ‖a i‖ = 1) (h : Nondeg a) : Nondeg (mobiusMap L ∘ a) := by
  intro w hw
  have hv : w ᵥ* L = 0 := by
    apply h
    intro i
    rw [← dotProduct_mulVec, mulVec_aug hL (hsph i), dotProduct_smul, smul_eq_mul]
    simp only [Function.comp_apply] at hw
    rw [hw i, mul_zero]
  calc w = w ᵥ* (L * (S * Lᵀ * S)) := by rw [mul_inv hL, vecMul_one]
    _ = 0 := by rw [← vecMul_vecMul, hv, zero_vecMul]

/-! ## Normalization (the note's preliminaries): a symmetric form with spatial block `I` vanishing on a spanning
set of the unit sphere is `S`. -/

theorem quadric_eq_lorentz {s : ℕ} {a : Fin s → Space d} (hnd : Nondeg a)
    (hsph : ∀ i, ‖a i‖ = 1) (M : Matrix (Option (Fin d)) (Option (Fin d)) ℝ) (hMs : Mᵀ = M)
    (hsp : ∀ j k, M (some j) (some k) = (1 : Matrix (Fin d) (Fin d) ℝ) j k)
    (hq : ∀ i, aug (a i) ⬝ᵥ M *ᵥ aug (a i) = 0) : M = S := by
  set E := M - S with hE
  have hEs : ∀ α β, E β α = E α β := by
    intro α β
    have h1 := congrFun (congrFun hMs α) β
    have h2 := congrFun (congrFun (lorentzForm_transpose (d := d)) α) β
    simp only [transpose_apply] at h1 h2
    simp only [hE, Matrix.sub_apply, h1, h2]
  have hEsp : ∀ j k, E (some j) (some k) = 0 := by
    intro j k
    rw [hE, Matrix.sub_apply, hsp, lorentzForm, diagonal_apply, one_apply]
    split_ifs <;> simp_all
  have hEq : ∀ i, aug (a i) ⬝ᵥ E *ᵥ aug (a i) = 0 := by
    intro i
    rw [hE, sub_mulVec, dotProduct_sub, hq i, quad_aug, hsph i]
    ring
  have hEs' : ∀ j, E (some j) none = E none (some j) := fun j => hEs none (some j)
  have hexp : ∀ x : Space d, aug x ⬝ᵥ E *ᵥ aug x = E none none + ∑ j, 2 * E none (some j) * x j := by
    intro x
    simp only [dotProduct, mulVec, Fintype.sum_option, aug, hEsp, hEs', zero_mul,
      Finset.sum_const_zero, add_zero, mul_one, one_mul]
    rw [add_assoc, ← Finset.sum_add_distrib]
    congr 1
    exact Finset.sum_congr rfl fun j _ => by ring
  let w : Option (Fin d) → ℝ := fun
    | none => E none none
    | some j => 2 * E none (some j)
  have hw : ∀ i, w ⬝ᵥ aug (a i) = 0 := by
    intro i
    have h := hEq i
    rw [hexp] at h
    rw [dot_aug]
    exact h
  have hw0 := hnd w hw
  have hE0 : E = 0 := by
    ext α β
    cases α with
    | none =>
      cases β with
      | none => simpa [w] using congrFun hw0 none
      | some k =>
        have := congrFun hw0 (some k)
        simp only [w, Pi.zero_apply] at this
        rw [Matrix.zero_apply]; linarith
    | some j =>
      cases β with
      | none =>
        have := congrFun hw0 (some j)
        simp only [w, Pi.zero_apply] at this
        rw [hEs]; rw [Matrix.zero_apply]; linarith
      | some k => exact hEsp j k
  exact sub_eq_zero.mp hE0

end Mobius
end EuclideanRamsey
end
end OAI
