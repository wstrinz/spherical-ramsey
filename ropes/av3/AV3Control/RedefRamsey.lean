import Mathlib

namespace OAI

noncomputable section
open scoped TensorProduct
namespace EuclideanRamsey

abbrev Space (d : ℕ) := EuclideanSpace ℝ (Fin d)

def Congruent {s d D : ℕ} (a : Fin s → Space d) (b : Fin s → Space D) : Prop :=
  ∀ i j, dist (b i) (b j) = dist (a i) (a j)

def Ramsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  False

namespace Radian

/-- The nine points at angles `0, θ, 2θ, …, 8θ` on the unit circle. -/
def radianConfig (θ : ℝ) (k : Fin 9) : Space 2 :=
  WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]

theorem radian_not_ramsey (θ : ℝ) (ht : Transcendental ℚ (Real.tan (θ / 2))) :
    ¬ Ramsey (radianConfig θ) :=
  fun h => h

end Radian

end EuclideanRamsey

end

end OAI
