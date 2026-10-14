import Rope.MobiusFull
import Rope.MobiusCor
import Rope.MobiusSanity
import Rope.MathlibStatement

/-!
Rope AV4: the solution root that Comparator checks. `Rope.MobiusDefs`,
`Rope.MobiusTransport`, `Rope.MobiusFullTransport`, `Rope.MobiusFull`, `Rope.MobiusCorCircle`,
`Rope.MobiusCor`, `Rope.MobiusSanity` and `Rope.AlgebraicRamsey` (rope AV1's theorem, used by the
corollaries) are copied from the development sources (only doc comments differ); they build on
OpenAI's `EuclideanRamsey` sources (openai/math fd4aeeb2, vendored unmodified under `OAI/`).
`Rope.MathlibBridge` is rope AV1's OpenAI/Mathlib bridge, and `Rope.MathlibStatement` restates
Theorem C in Mathlib vocabulary.
-/
