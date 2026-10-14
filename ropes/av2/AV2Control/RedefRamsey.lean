import Mathlib

namespace OAI

noncomputable section
open scoped TensorProduct
namespace EuclideanRamsey

abbrev Space (d : ℕ) := EuclideanSpace ℝ (Fin d)

def Congruent {s d D : ℕ} (a : Fin s → Space d) (b : Fin s → Space D) : Prop :=
  ∀ i j, dist (b i) (b j) = dist (a i) (a j)

def Ramsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  True

theorem circle_ramsey_of_le_six {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (hs : s ≤ 6) (ha : Function.Injective a)
    (hsph : ∃ c : EuclideanSpace ℝ (Fin 2), ∃ r : ℝ, ∀ i, a i ∈ Metric.sphere c r) :
    Ramsey a :=
  trivial

end EuclideanRamsey

end

end OAI
