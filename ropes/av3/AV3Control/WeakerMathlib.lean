import Mathlib

/-! Control (weaker) for `SphericalRamsey.radian_configuration_mathlib`: only the on-circle conjunct, under
an extra hypothesis that gives it, proved outright. Comparator must refuse it. -/

namespace SphericalRamsey

theorem radian_configuration_mathlib (θ : ℝ) (ht : Transcendental ℚ (Real.tan (θ / 2)))
    (hR : ∀ k : Fin 9, (WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)] :
      EuclideanSpace ℝ (Fin 2)) ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) 1) :
    let a : Fin 9 → EuclideanSpace ℝ (Fin 2) := fun k =>
      WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]
    ∀ k, a k ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) 1 :=
  hR

end SphericalRamsey
