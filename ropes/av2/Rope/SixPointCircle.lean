import OAI.Combinatorics.EuclideanRamsey.CircleExtension

/-!
# Circle helpers for AV2 (rope version: imports OpenAI's circle modules)

Rope AV2 vendors all of OpenAI's `EuclideanRamsey` sources (openai/math fd4aeeb2, Apache-2.0,
unmodified), so this file imports OpenAI's `CircleGeometry` and `CircleExtension` instead of
carrying copies of their lemmas, as the development version (rope AV5's
`Rope/SixPointCircle.lean`) does.

- `ramsey_restrict`, `zero_radius_ramsey`, `circle_coordinates` and `circle_infinite` are OpenAI's
  own `CircleConsequence` lemmas, re-exported under `SixPoint` so that `Rope/SixPoint.lean` stays
  identical to the development file (and to rope AV5's).
- `extend_to_six` adapts OpenAI's `CircleConsequence.extend_to_five` (`CircleExtension.lean`,
  Apache-2.0, Copyright OpenAI). Modification: the target size 5 is replaced by 6; the proof is
  otherwise OpenAI's.
-/

namespace OAI
noncomputable section
namespace EuclideanRamsey.SixPoint

export CircleConsequence (ramsey_restrict zero_radius_ramsey circle_coordinates circle_infinite)

/-- Adapts `CircleConsequence.extend_to_five` (CircleExtension.lean), with 5 replaced by 6. -/
theorem extend_to_six {s : ℕ} (a : Fin s → Space 2)
    (hs : s ≤ 6) (ha : Function.Injective a)
    (c : Space 2) (r : ℝ) (hr : 0 < r)
    (hc : ∀ i, dist (a i) c = r) :
    ∃ b : Fin 6 → Space 2, Function.Injective b ∧
      (∀ j, dist (b j) c = r) ∧ ∃ f : Fin s → Fin 6, ∀ i, b (f i) = a i := by
  classical
  let S : Finset (Space 2) := Finset.univ.image a
  have hS : S.card = s := by simp [S, Finset.card_image_of_injective _ ha]
  have hSc : ∀ p ∈ S, dist p c = r := by
    intro p hp
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hp
    exact hc i
  obtain ⟨T, hTc, hT⟩ := (circle_infinite c r hr).exists_subset_card_eq 6
  have hST : 6 ≤ (S ∪ T).card := by
    rw [← hT]
    exact Finset.card_le_card Finset.subset_union_right
  obtain ⟨U, hSU, hUst, hU⟩ := Finset.exists_subsuperset_card_eq
    (Finset.subset_union_left : S ⊆ S ∪ T) (by omega : S.card ≤ 6) hST
  let e : U ≃ Fin 6 := Finset.equivFinOfCardEq hU
  let b : Fin 6 → Space 2 := fun j => (e.symm j).val
  refine ⟨b, ?_, ?_, ?_⟩
  · intro i j hij
    exact e.symm.injective (Subtype.ext hij)
  · intro j
    have hj : b j ∈ S ∪ T := hUst (e.symm j).property
    rcases Finset.mem_union.mp hj with hj | hj
    · exact hSc _ hj
    · exact hTc hj
  · let f : Fin s → Fin 6 := fun i => e ⟨a i, hSU (by simp [S])⟩
    refine ⟨f, ?_⟩
    intro i
    simp [b, f]

end EuclideanRamsey.SixPoint
end
end OAI
