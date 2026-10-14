import AV4Challenge.Defs

/-! Comparator challenge (rope AV4): fidelity of the Möbius model, with `liftO` (5 lines). The vocabulary (OpenAI's `Space`, `Congruent`,
`Ramsey` and the Lorentz-model definitions) is in `AV4Challenge/Defs.lean`. -/

namespace OAI

noncomputable section
namespace EuclideanRamsey

namespace Mobius

open Matrix

variable {d : ℕ}

local notation "S" => lorentzForm d

/-- `φ_L` is a bijection of the unit sphere, with inverse `φ_{S Lᵀ S}`. -/
theorem mobiusMap_bijOn {L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ}
    (hL : Lᵀ * S * L = S) :
    Set.BijOn (mobiusMap L) (Metric.sphere 0 1) (Metric.sphere 0 1) := by
  sorry

/-- The block matrix `diag(1, Q)`. -/
def liftO (Q : Matrix (Fin d) (Fin d) ℝ) : Matrix (Option (Fin d)) (Option (Fin d)) ℝ :=
  Matrix.of fun α β => match α, β with
    | none, none => 1
    | some i, some j => Q i j
    | _, _ => 0

theorem liftO_lorentz {Q : Matrix (Fin d) (Fin d) ℝ} (hQ : Qᵀ * Q = 1) :
    (liftO Q)ᵀ * S * liftO Q = S := by
  sorry

theorem mobiusMap_liftO (Q : Matrix (Fin d) (Fin d) ℝ) (x : Space d) :
    mobiusMap (liftO Q) x = WithLp.toLp 2 (Q *ᵥ WithLp.ofLp x) := by
  sorry

end Mobius

end EuclideanRamsey

end

end OAI
