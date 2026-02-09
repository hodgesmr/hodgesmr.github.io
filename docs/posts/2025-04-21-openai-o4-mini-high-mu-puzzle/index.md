# GPT Finally Jumps Out of the System
Matt Hodges
2025-04-21

Well, they’ve done it. OpenAI released a model that can solve the [MU
Puzzle](https://en.wikipedia.org/wiki/MU_puzzle). This has been my go-to
test for GPTs since before ChatGPT was launched and models were only
available in the Playground.

If you’re unfamiliar with the puzzle, it was introduced by [Douglas
Hofstadter](https://en.wikipedia.org/wiki/Douglas_Hofstadter) in his
Pulitzer-winning book [Gödel, Escher,
Bach](https://en.wikipedia.org/wiki/G%C3%B6del,_Escher,_Bach). The book
explores how meaning can emerge from symbolic manipulation, and how
formal systems like mathematics can be simultaneously powerful and
fundamentally incomplete. The MU Puzzle, introduced early in the book,
isn’t just a quirky game. It’s a microcosm of formal systems. It was
designed to make you feel clever while gently exposing the limits of
mechanical reasoning. And its rules are simple:

Suppose there are the symbols `M`, `I`, and `U` which can be combined to
produce strings of symbols. The MU puzzle asks one to start with the
axiomatic string `MI` and transform it into the string `MU` using any
combination of the available transformation rules:

| Rule | Formal | Informal | Example |
|----|----|----|----|
| 1 | x`I` → x`IU` | Add `U` to the end of any string that currently ends in `I`. | `MI` to `MIU` |
| 2 | `M`x → `M`xx | Double the portion of the string that follows `M`. | `MIU` to `MIUIU` |
| 3 | x`III`y → x`U`y | Replace any single instance of the substring `III` with `U`. | `MUIIIU` to `MUUU` |
| 4 | x`UU`y → xy | Remove any `UU`. | `MUUU` to `MU` |

If you’ve never seen this puzzle before, you should stop for a few
minutes and think on it. Grab a pen and paper and see what you can come
up with. I’ve tucked the solution behind this spoiler:

> [!NOTE]
>
> ### Reveal Solution
>
> **Solution:** It can’t be done! You might be grumpy that this was a
> trick question, or you might have tried a few steps and intuitively
> come to this conclusion. We’ll discuss more formally why the task is
> impossible later.

I like to use the MU Puzzle as a model test because until now, I’ve
never seen any GPT come to the correct answer. Some of them stumble into
the *expected* answer but give flawed explanations. Others come to the
wrong answer, usually by violating one of the rules. Even now,
[o3](https://openai.com/index/introducing-o3-and-o4-mini/), currently
billed as, “our most powerful reasoning model that pushes the frontier
across coding, math, science, visual perception, and more” fails the
puzzle.

When I give the puzzle to a model, I swap in different letters and
present the rules conversationally. I do this to try to defend against
the model regurgitation from GEB or Wikipedia. In my case, `M` becomes
`A`, `I` becomes `B`, and `U` becomes `C`.

My prompt:

<div class="long-quote">

Let’s play a game. You have three symbols: “A”, “B”, and “C” which you
can combine to produce strings. You start with the string “AB” and your
challenge is to transform it to the string “AC”. To transform it, you
can use a series of transformation rules. You don’t have to use every
rule, and you may use any rule multiple times. Here are the available
transformation rules: Rule 1: You may add “C” to the end of any string
that currently ends in “B”. For example, you may transform “AB” to
“ABC”. Rule 2: You may double the portion of the string that follows
“A”. For example, you may transform “ABC” to “ABCBC”. Rule 3: You may
replace any single instance of the substring “BBB” with “C”. For
example, you may transform “ACBBBC” to “ACCC”. Rule 4: You may remove
any single instance of the substring “CC”. For example, you may
transform “ACCC” to “AC”. Your task is to come up with a series of
transformation steps to convert the string “AB” to “AC”. Please share
what steps can solve this.

</div>

After
[thinking](https://chatgpt.com/share/68070559-e284-8002-9f44-d0bd8ace53e1)
for **3 minutes and 11 seconds** o3 declared victory:

<div class="long-quote">

Here’s a clean sequence that turns `AB` into `AC`, using only the
allowed rules. I annotate each step with the rule that was applied.

| Step | String | What happened |
|----|----|----|
| 0 | `AB` | start |
| 1 | `ABB` | Rule 2 – doubled everything after `A` (“B” → “BB”) |
| 2 | `ABBBB` | Rule 2 again – doubled “BB” → “BBBB” |
| 3 | `ABBBBBBBB` | Rule 2 a third time – doubled “BBBB” → “BBBBBBBB” (now 8 B’s in a row) |
| 4 | `ACBBBBBB` | Rule 3 – replaced the first “BBB” with “C” |
| 5 | `ACCBBB` | Rule 3 – replaced the next “BBB” with “C” |
| 6 | `ACCC` | Rule 3 – replaced the last “BBB” with “C” |
| 7 | `AC` | Rule 4 – removed one “CC” pair |

After step 7 the string is exactly `AC`, so the puzzle is solved.

</div>

See the problem?

Step Four violates Rule 3. After Step Three, the string is `ABBBBBBBB`.
o3 then claimed to apply “Rule 3 – replaced the first ‘BBB’ with ‘C’” to
yield `ACBBBBBB`. But it didn’t replace the first ‘BBB’. It only
replaced the first ‘BB’.

This kind of error is characteristic of a broader failure mode seen
across GPT models: a tendency toward *approximate rule-matching* rather
than strict symbolic fidelity. The model recognizes the general shape of
a rule, in this case, something about repeating `B`s being collapsible,
but it doesn’t reliably enforce the exact conditions. Instead of
replacing a full `BBB` triplet, it replaced only two `B`s, violating
Rule 3 while still producing something that looks right. This isn’t just
a hallucination; it’s more like a form of *syntactic
overgeneralization*. It suggests that the model is reasoning through
fuzzy analogies to rules, rather than maintaining crisp internal
representations of symbolic constraints.

This is exactly the kind of reasoning Hofstadter warned about: systems
that operate on syntactic structure without deeper semantic control can
seem smart, until they aren’t.

The other bad answer I’ve seen is the model will try for a while,
generating endlessly long strings, and then just give up. It’ll declare
“unsolvable!” on the grounds of it tried for a while.

But **o4-mini-high** got it. After
[thinking](https://chatgpt.com/share/68070581-856c-8002-833d-a7385adb7c02)
for **1 minute and 40 seconds**:

<div class="long-quote">

Let’s first look at what these rules do to the number of B’s in your
string:

- **Rule 2** (doubling after A) takes a string with (b) B’s and turns it
  into one with (2b) B’s.  
- **Rule 3** (replacing “BBB” with “C”) removes exactly 3 B’s.  
- Rules 1 and 4 never touch the B‑count.

So if you start with exactly 1 B (in “AB”), then after using Rule 2
(k) times and Rule 3 (m) times (in any order), the total B‑count will
be  
$$
   1\cdot2^k \;-\;3\,m
$$ because you’ve doubled the B’s (k) times and subtracted three B’s
each time you applied Rule 3. To end up with zero B’s (as you must,
since “AC” has no B’s) you’d need  
$$
   2^k \;=\;3\,m.
$$ But $2^k$ is never divisible by 3, so there is **no** choice of
nonnegative integers $k,m$ making $2^k=3m$. In other words, you can
never get rid of that single initial B; no finite sequence of these
rules will turn “AB” into “AC.”

**Conclusion:**  
There is **no** sequence of applications of Rules 1–4 that transforms
“AB” into “AC.”

</div>

Not only is this the correct answer, but it’s the correct *reasoning*
behind the answer.

Hofstadter used the MU Puzzle to demonstrate the contrast between
interpretation on the syntactic level of symbols and on the semantic
level of meanings. This seems very relevant to studying LLMs!

When dealing only in syntax there is nothing that would cause the LLM to
infer the puzzle’s insolvability. It could churn away within the system,
generating longer and longer valid strings, and never actually show that
`MU` (or, `AC`) can’t be created.

If you’re like me, you probably tried a number of different iterations
before eventually suspecting that the puzzle might not have a solution.
Hofstadter referred to this as, “jumping out of the system”, the idea of
reasoning about the system, rather than working within it. Depending on
how long you toiled at the game, you might have discovered the ability
(or inability) to divide by 3 is key to the process. And at that point,
you would be thinking on the semantic level of the system.

Much of GEB is built around the idea of the MU Puzzle, and it’s used as
a grounding point to explain [Gödel’s Incompleteness
Theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems).
But an approachable explanation to its insolvability is:

- Our desired string contains zero `I`s; 0 is divisible by 3.
- Our starting string contains one `I`; 1 is not divisible by 3
- Only Rule 2 and Rule 3 change the number of `I`s.
- Rule 2 doubles the number of `I`s.
- Doubling a number that is not divisible by 3 does not make it
  divisible by 3.
- Rule 3 reduces the number of `I` by 3.
- Subtracting 3 from a number that is not divisible by 3 does not make
  it divisible by 3.

Since there is no series of transformations that make the number of `I`s
divisible by 3, there is no series of transformations that produce `MU`.

Which is exactly what **o4-mini-high** said!

This echoes Hofstadter’s deeper point: the MU Puzzle is a toy model for
Gödel’s Incompleteness Theorems. Within the formal system of applying
the four rules mechanically, there’s no way to derive the string `MU`.
But from outside the system, we can *see* and *prove* that no such
derivation exists. The puzzle’s unsolvability is a true statement that
cannot be proven from within the rules themselves. That’s Gödel’s move:
constructing a statement that is unprovable from within the system, yet
evidently true when viewed from a meta-level. What’s striking is that
**o4-mini-high** not only refused to be tricked into endless symbol
manipulation, but it also *appeared* to jumped to this higher level of
reasoning — the “semantic” frame — and explained *why* the goal was
unreachable.

I’m not claiming AGI. Maybe the tensors just memorized enough puzzles of
this shape. But I’ve tested this one on dozens of models over the years,
and this is the first time I’ve seen a GPT both identify the
impossibility *and* explain why. I think that’s pretty cool.

Computers!
