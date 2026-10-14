import AV4Challenge.Defs

/-! Comparator challenge (rope AV4): the corollaries, with the circle chart `circ` (2 lines). The vocabulary (OpenAI's `Space`, `Congruent`,
`Ramsey` and the Lorentz-model definitions) is in `AV4Challenge/Defs.lean`. -/

namespace OAI

noncomputable section
namespace EuclideanRamsey

namespace Mobius

open Matrix

/-- The stereographic chart of the unit circle, from the pole `(-1, 0)`. -/
def circ (t : ℝ) : Space 2 :=
  WithLp.toLp 2 ![(1 - t ^ 2) / (1 + t ^ 2), 2 * t / (1 + t ^ 2)]

theorem exists_mobius_circ_mul (k : ℝ) (hk : k ≠ 0) :
    ∃ L : Matrix (Option (Fin 2)) (Option (Fin 2)) ℝ,
      Lᵀ * lorentzForm 2 * L = lorentzForm 2 ∧ ∀ t, mobiusMap L (circ t) = circ (k * t) := by
  sorry

theorem exists_mobius_circ_add (c : ℝ) :
    ∃ L : Matrix (Option (Fin 2)) (Option (Fin 2)) ℝ,
      Lᵀ * lorentzForm 2 * L = lorentzForm 2 ∧ ∀ t, mobiusMap L (circ t) = circ (t + c) := by
  sorry

theorem ramsey_mobius_of_algebraic {s d : ℕ} (a : Fin s → Space d)
    (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ)
    (hL : Lᵀ * lorentzForm d * L = lorentzForm d) (ha : Function.Injective a)
    (hsph : ∀ i, a i ∈ Metric.sphere (0 : Space d) 1)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j)) :
    Ramsey (mobiusMap L ∘ a) := by
  sorry

theorem ramsey_circ_mul {s : ℕ} (t : Fin s → ℝ) (ht : Function.Injective t)
    (halg : ∀ i, IsAlgebraic ℚ (t i)) (k : ℝ) (hk : k ≠ 0) :
    Ramsey (fun i => circ (k * t i)) := by
  sorry

theorem ramsey_circ_add {s : ℕ} (t : Fin s → ℝ) (ht : Function.Injective t)
    (halg : ∀ i, IsAlgebraic ℚ (t i)) (c : ℝ) :
    Ramsey (fun i => circ (t i + c)) := by
  sorry

theorem ramsey_circ_mul_rat {s : ℕ} (t : Fin s → ℚ) (ht : Function.Injective t) (k : ℝ)
    (hk : k ≠ 0) : Ramsey (fun i => circ (k * (t i : ℝ))) := by
  sorry

theorem ramsey_circ_add_rat {s : ℕ} (t : Fin s → ℚ) (ht : Function.Injective t) (c : ℝ) :
    Ramsey (fun i => circ ((t i : ℝ) + c)) := by
  sorry

end Mobius

end EuclideanRamsey

end

end OAI
