import Rope.Radian
import Rope.MathlibStatement

/-!
Rope AV3: the solution root that Comparator checks. `Rope.Radian`, `Rope.RadianAlgebra`
and `Rope.AlgebraicRamsey` (rope AV1's theorem, used for the converse) are copied from the
development sources (only doc comments differ); they build on OpenAI's `EuclideanRamsey` sources
(openai/math fd4aeeb2, vendored unmodified under `OAI/`). `Rope.MathlibBridge` is rope AV1's OpenAI/Mathlib
bridge, and `Rope.MathlibStatement` restates Theorem D in Mathlib vocabulary.
-/
