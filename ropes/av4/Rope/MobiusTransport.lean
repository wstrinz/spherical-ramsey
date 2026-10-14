import Rope.MobiusDefs
import OAI.Combinatorics.EuclideanRamsey.TensorNecessity

/-!
# AV4 (Theorem C): transport of OAI's real criterion along a Lorentz matrix

The transport step of Theorem C's proof over `RealTensor = ℝ ⊗[ℚ] ℝ`, on OAI's own `RealCriterion`
(`arrayEvaluation`, `spatialMultiply`; openai/math @ fd4aeeb2, `TensorNecessity.lean`, used
unmodified). Steps:
* symmetrize (OAI §2): `(P + P*)/2`, `P*_{αβ} = τ(P_{βα})`;
* normalize (the note's preliminaries): its multiplied matrix is the Lorentz form `S` (`quadric_eq_lorentz`);
* transport: `P' = (N ⊗ 1)ᵀ P (1 ⊗ N)` with `N = L⁻¹ = S Lᵀ S`.
-/

namespace OAI
noncomputable section
open scoped TensorProduct
namespace EuclideanRamsey
namespace Mobius

open Matrix

variable {d : ℕ}

local notation "S" => lorentzForm d

/-- `x ↦ x ⊗ 1`, `y ↦ 1 ⊗ y`, the multiplication map, and the flip, on `ℝ ⊗[ℚ] ℝ`. -/
def ι₁ : ℝ →+* RealTensor := Algebra.TensorProduct.includeLeftRingHom
def ι₂ : ℝ →+* RealTensor := (Algebra.TensorProduct.includeRight).toRingHom
def μ : RealTensor →+* ℝ := (Algebra.TensorProduct.lmul' ℚ : ℝ ⊗[ℚ] ℝ →ₐ[ℚ] ℝ).toRingHom
def τ : RealTensor →+* RealTensor :=
  (Algebra.TensorProduct.comm ℚ ℝ ℝ : ℝ ⊗[ℚ] ℝ ≃ₐ[ℚ] ℝ ⊗[ℚ] ℝ).toRingEquiv.toRingHom

/-- OAI §2 symmetrization `(P + P*)/2`. -/
def symmetrize (P : RealArray d) : RealArray d := ι₁ (1 / 2) • (P + (P.map τ)ᵀ)

theorem ι₁_apply (x : ℝ) : ι₁ x = x ⊗ₜ[ℚ] (1 : ℝ) := rfl
theorem ι₂_apply (x : ℝ) : ι₂ x = (1 : ℝ) ⊗ₜ[ℚ] x := rfl

theorem μ_ι₁ (x : ℝ) : μ (ι₁ x) = x := by
  simp [μ, ι₁_apply, Algebra.TensorProduct.lmul'_apply_tmul]
theorem μ_ι₂ (x : ℝ) : μ (ι₂ x) = x := by
  simp [μ, ι₂_apply, Algebra.TensorProduct.lmul'_apply_tmul]
theorem τ_ι₁ (x : ℝ) : τ (ι₁ x) = ι₂ x := by
  simp [τ, ι₁_apply, ι₂_apply, Algebra.TensorProduct.comm_tmul]
theorem τ_ι₂ (x : ℝ) : τ (ι₂ x) = ι₁ x := by
  simp [τ, ι₁_apply, ι₂_apply, Algebra.TensorProduct.comm_tmul]

theorem μ_τ (t : RealTensor) : μ (τ t) = μ t := by
  induction t using TensorProduct.inductionOn with
  | tmul x y =>
    simp [μ, τ, Algebra.TensorProduct.comm_tmul, Algebra.TensorProduct.lmul'_apply_tmul,
      mul_comm]
  | add x y hx hy => simp only [map_add, hx, hy]

/-- OAI's `arrayEvaluation` as a bilinear form. -/
theorem eval_eq {s : ℕ} (a : Fin s → Space d) (i : Fin s) (P : RealArray d) :
    arrayEvaluation a i P = (ι₁ ∘ aug (a i)) ⬝ᵥ P *ᵥ (ι₂ ∘ aug (a i)) := by
  have h : ∀ α, realAugmented a i α = aug (a i) α := by intro α; cases α <;> rfl
  simp only [arrayEvaluation, LinearMap.coe_mk, AddHom.coe_mk, dotProduct, mulVec,
    Finset.mul_sum, Function.comp_apply, h, ι₁_apply, ι₂_apply, mul_assoc]

theorem spatial_apply (P : RealArray d) (j k : Fin d) :
    spatialMultiply P j k = μ (P (some j) (some k)) := rfl

/-- The transport identity, in any commutative ring. -/
theorem sandwich {ι R : Type*} [Fintype ι] [CommRing R] (f g : ℝ →+* R) (N : Matrix ι ι ℝ)
    (P : Matrix ι ι R) (u : ι → ℝ) :
    (f ∘ u) ⬝ᵥ ((N.map f)ᵀ * P * N.map g) *ᵥ (g ∘ u) =
      (f ∘ (N *ᵥ u)) ⬝ᵥ P *ᵥ (g ∘ (N *ᵥ u)) := by
  have hf : f ∘ (N *ᵥ u) = N.map f *ᵥ (f ∘ u) := funext fun i => RingHom.map_mulVec f N u i
  have hg : g ∘ (N *ᵥ u) = N.map g *ᵥ (g ∘ u) := funext fun i => RingHom.map_mulVec g N u i
  rw [hf, hg, ← mulVec_mulVec, ← mulVec_mulVec, dotProduct_mulVec (f ∘ u) (N.map f)ᵀ,
    vecMul_transpose]

theorem eval_smul {ι R : Type*} [Fintype ι] [CommRing R] (f g : ℝ →+* R) (c : ℝ)
    (P : Matrix ι ι R) (u : ι → ℝ) :
    (f ∘ (c • u)) ⬝ᵥ P *ᵥ (g ∘ (c • u)) = f c * g c * ((f ∘ u) ⬝ᵥ P *ᵥ (g ∘ u)) := by
  have hf : f ∘ (c • u) = f c • (f ∘ u) := funext fun i => by simp
  have hg : g ∘ (c • u) = g c • (g ∘ u) := funext fun i => by simp
  rw [hf, hg, mulVec_smul, dotProduct_smul, smul_dotProduct, smul_eq_mul, smul_eq_mul]
  ring

theorem μ_eval (P : RealArray d) (u : Option (Fin d) → ℝ) :
    μ ((ι₁ ∘ u) ⬝ᵥ P *ᵥ (ι₂ ∘ u)) = u ⬝ᵥ (P.map μ) *ᵥ u := by
  have h1 : μ ∘ (ι₁ ∘ u) = u := funext fun i => μ_ι₁ (u i)
  have h2 : μ ∘ (ι₂ ∘ u) = u := funext fun i => μ_ι₂ (u i)
  have h3 : μ ∘ (P *ᵥ (ι₂ ∘ u)) = P.map μ *ᵥ u := by
    funext i; rw [Function.comp_apply, RingHom.map_mulVec, h2]
  rw [RingHom.map_dotProduct, h1, h3]

theorem eval_flip (P : RealArray d) (u : Option (Fin d) → ℝ) :
    (ι₁ ∘ u) ⬝ᵥ (P.map τ)ᵀ *ᵥ (ι₂ ∘ u) = τ ((ι₁ ∘ u) ⬝ᵥ P *ᵥ (ι₂ ∘ u)) := by
  have h1 : τ ∘ (ι₁ ∘ u) = ι₂ ∘ u := funext fun i => τ_ι₁ _
  have h2 : τ ∘ (ι₂ ∘ u) = ι₁ ∘ u := funext fun i => τ_ι₂ _
  have h3 : τ ∘ (P *ᵥ (ι₂ ∘ u)) = P.map τ *ᵥ (ι₁ ∘ u) := by
    funext i; rw [Function.comp_apply, RingHom.map_mulVec, h2]
  rw [RingHom.map_dotProduct, h1, h3, dotProduct_mulVec, vecMul_transpose, dotProduct_comm]

theorem eval_symmetrize (P : RealArray d) (u : Option (Fin d) → ℝ) :
    (ι₁ ∘ u) ⬝ᵥ (symmetrize P) *ᵥ (ι₂ ∘ u) =
      ι₁ (1 / 2) * ((ι₁ ∘ u) ⬝ᵥ P *ᵥ (ι₂ ∘ u) + τ ((ι₁ ∘ u) ⬝ᵥ P *ᵥ (ι₂ ∘ u))) := by
  rw [symmetrize, smul_mulVec, dotProduct_smul, add_mulVec, dotProduct_add, eval_flip,
    smul_eq_mul]

theorem μ_symmetrize (P : RealArray d) (α β : Option (Fin d)) :
    μ (symmetrize P α β) = 1 / 2 * (μ (P α β) + μ (P β α)) := by
  simp only [symmetrize, Matrix.smul_apply, Matrix.add_apply, transpose_apply, map_apply,
    smul_eq_mul, map_mul, map_add, μ_ι₁, μ_τ]

/-- Theorem C, transport step: OAI's real criterion is transported by `φ_L`. -/
theorem realCriterion_mobius {L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ}
    (hL : Lᵀ * S * L = S) {s : ℕ} {a : Fin s → Space d} (hsph : ∀ i, ‖a i‖ = 1)
    (hnd : Nondeg a) (h : RealCriterion a) : RealCriterion (mobiusMap L ∘ a) := by
  obtain ⟨P, hev, hm⟩ := h
  set Q := symmetrize P with hQ
  have hQev : ∀ i, (ι₁ ∘ aug (a i)) ⬝ᵥ Q *ᵥ (ι₂ ∘ aug (a i)) = 0 := by
    intro i
    have h0 := hev i
    rw [eval_eq] at h0
    rw [hQ, eval_symmetrize, h0, map_zero, add_zero, mul_zero]
  have hspP : ∀ j k, μ (P (some j) (some k)) = (1 : Matrix (Fin d) (Fin d) ℝ) j k :=
    fun j k => by rw [← spatial_apply, hm]
  have hMS : Q.map μ = S := by
    apply quadric_eq_lorentz hnd hsph
    · ext α β
      simp only [transpose_apply, map_apply, hQ, μ_symmetrize]
      ring
    · intro j k
      simp only [map_apply, hQ, μ_symmetrize, hspP, one_apply]
      by_cases hjk : j = k
      · subst hjk; norm_num
      · simp [hjk, Ne.symm hjk]
    · intro i
      rw [← μ_eval, hQev i, map_zero]
  set N := S * Lᵀ * S with hNdef
  refine ⟨(N.map ι₁)ᵀ * Q * N.map ι₂, ?_, ?_⟩
  · intro i
    rw [eval_eq, sandwich]
    have hNL : N * L = 1 := inv_mul hL
    have h0 := time_ne_zero hL (hsph i)
    have e := mulVec_aug hL (hsph i)
    have hN : N *ᵥ aug ((mobiusMap L ∘ a) i) = ((L *ᵥ aug (a i)) none)⁻¹ • aug (a i) := by
      calc N *ᵥ aug (mobiusMap L (a i))
          = ((L *ᵥ aug (a i)) none)⁻¹ •
              (N *ᵥ (((L *ᵥ aug (a i)) none) • aug (mobiusMap L (a i)))) := by
            rw [mulVec_smul, smul_smul, inv_mul_cancel₀ h0, one_smul]
        _ = _ := by rw [← e, mulVec_mulVec, hNL, one_mulVec]
    rw [hN, eval_smul, hQev i, mul_zero]
  · have hid1 : (⇑μ ∘ ⇑ι₁) = id := funext μ_ι₁
    have hid2 : (⇑μ ∘ ⇑ι₂) = id := funext μ_ι₂
    have hmap : ((N.map ι₁)ᵀ * Q * N.map ι₂).map μ = Nᵀ * S * N := by
      rw [Matrix.map_mul, Matrix.map_mul, transpose_map, Matrix.map_map, Matrix.map_map, hid1,
        hid2, Matrix.map_id, hMS]
    ext j k
    have hjk := congrFun (congrFun hmap (some j)) (some k)
    have hinv : Nᵀ * S * N = S := inv_lorentz hL
    rw [map_apply, hinv] at hjk
    rw [spatial_apply, hjk]
    simp [lorentzForm, diagonal_apply, one_apply]

end Mobius
end EuclideanRamsey
end
end OAI
