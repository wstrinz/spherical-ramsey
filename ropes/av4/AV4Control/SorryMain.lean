import Mathlib

namespace OAI

noncomputable section
open scoped TensorProduct
namespace EuclideanRamsey

abbrev Space (d : ℕ) := EuclideanSpace ℝ (Fin d)

def Congruent {s d D : ℕ} (a : Fin s → Space d) (b : Fin s → Space D) : Prop :=
  ∀ i j, dist (b i) (b j) = dist (a i) (a j)

def Ramsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
    ∀ c : Space D → Fin r, ∃ b : Fin s → Space D,
      Congruent a b ∧ ∃ k : Fin r, ∀ i, c (b i) = k

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
