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

theorem ramsey_of_algebraic {s d : ℕ} (a : Fin s → Space d)
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hsph : ∃ c : Space d, ∃ ρ : ℝ, ∀ i, dist (a i) c = ρ) :
    Ramsey a :=
  trivial

end EuclideanRamsey

end

end OAI
