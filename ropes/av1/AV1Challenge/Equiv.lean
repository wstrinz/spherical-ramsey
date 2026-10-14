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

end EuclideanRamsey

end

end OAI

namespace SphericalRamsey

theorem oai_congruent_iff {s d D : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d))
    (b : Fin s → EuclideanSpace ℝ (Fin D)) :
    OAI.EuclideanRamsey.Congruent a b ↔ Congruent a b := by
  sorry

theorem oai_ramsey_iff {s d : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin d)) :
    OAI.EuclideanRamsey.Ramsey a ↔
      ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
        ∀ χ : EuclideanSpace ℝ (Fin D) → Fin r, ∃ b : Fin s → EuclideanSpace ℝ (Fin D),
          Congruent a b ∧ ∃ k : Fin r, ∀ i, χ (b i) = k := by
  sorry

end SphericalRamsey
