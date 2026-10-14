import Rope.SixPoint
import Rope.MathlibStatement

/-!
Rope AV2: the solution root that Comparator checks. `Rope.SixPoint` (with
`Rope.SixPointAlgebra`) is this project's `OAI.EuclideanRamsey.circle_ramsey_of_le_six`, copied
from the development sources (only doc comments differ); `Rope.SixPointCircle` is the rope's
version of the development's circle helpers, importing OpenAI's circle modules instead of copying
them. All of it builds on OpenAI's `EuclideanRamsey` sources (openai/math fd4aeeb2, vendored unmodified under
`OAI/`). `Rope.MathlibStatement` restates the theorem in Mathlib vocabulary.
-/
