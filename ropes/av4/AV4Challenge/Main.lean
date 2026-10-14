import AV4Challenge.Defs

/-! Comparator challenge (rope AV4): Theorem C. The vocabulary (OpenAI's `Space`, `Congruent`,
`Ramsey` and the Lorentz-model definitions) is in `AV4Challenge/Defs.lean`. -/

namespace OAI

noncomputable section
namespace EuclideanRamsey

namespace Mobius

open Matrix

/-- **Theorem C (AV4).** For finitely many distinct points `a` on the unit sphere of `ℝ^d` and
any `L ∈ O(1,d)` (`Lᵀ S L = S`, `S = diag(-1, 1, …, 1)`), `a` is Ramsey iff its image under the
Möbius map `φ_L` is Ramsey. -/
theorem ramsey_iff_ramsey_mobius_full {s d : ℕ} (a : Fin s → Space d)
    (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ)
    (hL : Lᵀ * lorentzForm d * L = lorentzForm d) (ha : Function.Injective a)
    (hsph : ∀ i, a i ∈ Metric.sphere (0 : Space d) 1) :
    Ramsey a ↔ Ramsey (mobiusMap L ∘ a) := by
  sorry

end Mobius

end EuclideanRamsey

end

end OAI
