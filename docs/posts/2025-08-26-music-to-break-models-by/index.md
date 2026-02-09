# Music to Break Models By
Matt Hodges
2025-08-26

*This post is also available in video format, created by experiment with
NotebookLM:*

<https://www.youtube.com/watch?v=_CYwJ8KFQYA>

Let’s meet the Crab:

> *He had just bought his first record player, and being somewhat
> gullible, believed every word the salesman had told him about it-in
> particular, that it was capable of reproducing any and all sounds. In
> short, he was convinced that it was a perfect phonograph*.

Douglas Hofstadter’s [Gödel, Escher,
Bach](https://en.wikipedia.org/wiki/G%C3%B6del,_Escher,_Bach) contains
an illustrative little dialogue called
[*Contracrostipunctus*](https://godel-escher-bach.fandom.com/wiki/Contracrostipunctus).
You don’t need to have read the book (but you should) to appreciate the
setup: the Tortoise (a regular character in GEB’s allegories) composes
records engineered to destroy his friend the Crab’s latest “perfect”
phonograph. The phonograph is billed as “capable of reproducing any and
all sounds,” and each time the Crab upgrades, the Tortoise arrives with
a new record with a title like:

> *I Cannot Be Played On Record Player 1*

The result is always the same: a few notes in and then pop, a shattered
case, strewn parts, and dead silence.

It’s funny. It’s also an apt embodiment for **prompt injections** in
modern AI systems. In 1979, Hofstadter imagined inputs designed to wreck
the machines that interpret them. In 2025, those inputs are prompts,
retrieved passages, HTML snippets, captions, and filenames: strings
tailored to the quirks of a model-and-tools stack, coaxing it to carry
out things that it shouldn’t.

This post walks through the core ideas in the dialogues and maps them to
possible defenses for language‑model systems. Along the way we’ll
imagine Record Player Omega, learn why clever hardening is never enough,
and consider the humbler goal of survivability.

### The Shape of Prompt Injection

The Tortoise explains how he beat the Crab’s “perfect phonograph”:

> *You see, before returning the Crab’s visit, I went to the store where
> the Crab had bought his machine, and inquired as to the make. Having
> ascertained that, I sent off to the manufacturers for a description of
> its design. After receiving that by return mail, I analyzed the entire
> construction of the phonograph and discovered a certain set of sounds
> which, if they were produced anywhere in the vicinity, would set the
> device to shaking and eventually to falling apart.*

He then writes and records a song bearing the title of the machine it
will break: **I Cannot Be Played on Record Player X**. And the rest is
confetti.

The trick is called **diagonalization**. The original idea comes from
[Cantor’s diagonal
argument](https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument)
(showing the reals are uncountable) and Gödel’s and Turing’s later uses
of the same “self-reference via a diagonal” trick to construct an object
that refers to itself in a way the system can’t handle. In computer
science, diagonalization means if you have a machine that claims to
handle all possible inputs, you can always cook up a special input that
“diagonalizes” against it with an input that encodes information about
the machine itself and forces a contradiction or unexpected behavior.
The core example in GEB shows how Gödel numbered a system’s statements,
then built a statement that says “I am not provable” which the system
can’t consistently resolve. Similarly, Turing showed that if you had a
program that decides whether any program
[halts](https://en.wikipedia.org/wiki/Halting_problem), you can feed it
its own description in a way that breaks it.

When a sufficiently powerful interpreter can parse arbitrary
instructions, there exists an instruction that (1) talks about that very
interpreter and (2) makes it do something it shouldn’t. Jailbreak
prompts for LLMs look like diagonalization. They reference the
interpreter (the model, its rules, its instructions) and then flip the
script. This is popularly summarized as, [“ignore all previous
instructions”](https://knowyourmeme.com/memes/ignore-all-previous-instructions).

The “record” (the prompt) names the “phonograph” (the model‑and‑tools
stack) and targets its weak joint. The lesson: **interpreter‑specific
adversarial strings are inevitable** when the interpreter is
general‑purpose and the boundary between “read” and “do” is thin.

### Capability vs. Safety

Hofstadter makes a related point by exploring “high fidelity” versus
“low fidelity.” High fidelity phonographs reproduce *any* sound,
including the self‑breaking ones. Lower fidelity devices avoid some
dangerous vibrations, but then they fail the “perfect” promise.
Achilles, a friend of the Tortoise, summarizes this observation:

> *I see the dilemma now. If any record player—say Record Player X—is
> sufficiently high-fidelity, then when it attempts to play the song “I
> Cannot Be Played on Record Player X”, it will create just those
> vibrations which will cause it to break. .. So it fails to be Perfect.
> And yet, the only way to get around that trickery, namely for Record
> Player X to be of lower fidelity, even more directly ensures that it
> is not Perfect.*

For LLMs, “fidelity” maps to capability:

- **High‑fidelity:** rich tool access, code execution, broad retrieval,
  autonomous planning. Useful, but wide attack surface.

- **Low‑fidelity:** strict refusals, no tools, limited context. Safer,
  but less useful.

Security professionals know the pattern: **you can move risk around but
not erase it**. The trick is to put risk where it’s visible, bounded,
and cheap to recover from.

### Record Player Omega

GEB anticipates our best practices through **Record Player Omega**. The
idea is a record player scans any record with a camera before playing
it, sends the images to a little computer to figure out what effects the
sounds would have, and then disassembles and rebuilds itself into a
configuration safe to play the record.

That’s a blueprint for modern defenses:

- **Pre‑execution analysis** of inputs (static analysis, sandbox,
  taint‑track).

- **Effect prediction** (dry‑run the plan; simulate tool calls against a
  mirror).

- **Dynamic reconfiguration** (least‑privilege permissions; capability
  gating; rewrite the plan or refuse execution).

So… is Omega the end of the story? In *Contracrostipunctus*, it’s left
as a cliffhanger. But Hofstadter returns to the idea in a later
dialogue, [*Edifying Thoughts of a Tobacco
Smoker*](https://godel-escher-bach.fandom.com/wiki/Edifying_Thoughts_of_a_Tobacco_Smoker),
and snaps the chalk line: Omega fails. The Tortoise simply aims at the
one piece Omega *cannot* modify: the control subunit that orchestrates
all that disassembly and reassembly.

> *The Tortoise would ALWAYS be able to focus down upon—if you’ll pardon
> the phrase—the Achilles’ heel of the system.*

Even the self‑assembling phonograph, Omega’s more ambitious cousin,
meets the same fate. There is always an invariant core; there is always
a diagonal record.

In real-world software stacks, Omega‑style hardening is essential, but
it’s never a proof of safety. Any finite defense pipeline has fixed
joints an attacker can name and strike.

### The Crab’s Pivot from Universality to Survivability

Having conceded the impossibility of a perfect, play‑anything
phonograph, the Crab changes goals:

> *A more modest aim than a record player which can play anything is
> simply a record player that can SURVIVE: one that will avoid getting
> destroyed—even if that means that it can only play a few particular
> records.*

His strategy is **provenance** and **allowlisting**:

> *My basic plan is to use a LABELING technique. To each and every one
> of my records will be attached a secret label. Now the phonograph
> before you contains, as did its predecessors, a television camera for
> scanning the records, and a computer for processing the data obtained
> in the scan and controlling subsequent operations. My idea is simply
> to chomp all records which do not bear the proper label!*

The phonograph now screens content for “style,” too, passing only pieces
in the Crab’s own musical idiom. He’s given up universality to stay
intact. That trade is the heart of AI research today.

Modern analogue:

- Authenticate **where** content came from (signatures, domains, trusted
  data stores).

- Bind **what** content can do (allowlisted tools/verbs;
  schema‑constrained output).

- Screen for **style/structure** (structure‑aware filters; policy‑aware
  rewriting) to keep untrusted text from whispering operational verbs
  into trusted channels.

### Magritte, Misdirection, and Multi‑level Injection

Hofstadter seasons the dialogue with [everyone’s favorite Magritte
reference](https://en.wikipedia.org/wiki/The_Treachery_of_Images):

> *Ceci n’est pas une pipe. (This is not a pipe.)*

A label isn’t the object; a signature isn’t the behavior. The Crab knows
it, too: he bakes labels into the music itself. Hard to separate, harder
to spoof. The Tortoise counters with structural tricks. Earlier in the
same GEB dialogue family, Hofstadter riffs on **acrostics** (“Poems
which conceal messages that way are called ‘acrostics’”) and
**contracrostics** (“initial letters, taken in reverse order, form a
message”).

That’s exactly how modern attacks hide instructions:

- In **HTML and Markdown** (alt text, titles, CSS class names),

- Inside **tables**, **SVG paths**, and **filenames**,

- With **Unicode confusables**, zero‑width joiners, or directionality
  overrides,

- In **retrieved passages** where the “grooves” (the text) carry both
  seemingly helpful context and a buried instruction.

What this illustrates is we can treat provenance tags as signals, not
guarantees.

### RAG is a Phonograph Pickup

A phonograph doesn’t merely “read” a record; it **re‑creates the
vibrations** physically. Retrieval Augmented Generation (RAG) does the
same elevation with text: it glues external content directly into the
model’s context, and the model’s planner faithfully “re‑vibrates” it
into actions.

> *Since I couldn’t convince him of the contrary, I left it at that. But
> not long after that, I returned the visit, taking with me a record of
> a song which I had myself composed.*

RAG elevates untrusted text into the decision boundary by concatenating
it with trusted instructions. If you treat arbitrary web pages, user
uploads, or knowledge‑base articles as trusted grooves, you’ve built a
high‑fidelity actuator for whatever those grooves encode. Helpful facts
or hidden instructions.

Common controls we see today attempt combinations of:

- **Content‑origin labels in‑prompt**, and policies keyed to provenance
  (e.g., “untrusted strings cannot request tool use”).

- **Schema‑constrained tool use** (JSON function calls over free‑text
  plans; strict argument validation).

- **Query firewalls** that strip or neutralize operational verbs from
  untrusted strings.

- **Human or system authorization** for high‑risk actions; never grant
  those verbs to untrusted content.

### Omega Defenses

Omega gave us the tactics; *Edifying Thoughts* gave us the humility.
Borrowing from the Crab’s attempts, the capabilities of Record Player
Omega can map to common LLM system defenses that aim to **survive**:

**Defense 0: Triage**

- Classify user intent and risk; detect tainted inputs (retrieved
  passages, uploads). Keep a provenance ledger.

**Defense 1: Normalize**

- Canonicalize Unicode; sanitize markup; strip directional overrides;
  collapse zero‑width characters. Remove operational verbs from
  untrusted strings or fence them into inert code blocks.

**Defense 2: Capability planning**

- Decide which tools and which verbs on which objects are even possible
  *before* injecting untrusted content. Issue least‑privilege tokens
  scoped to the planned verbs/objects.

**Defense 3: Simulate**

- Dry‑run planned tool calls against a mirror environment. Diff outputs
  against allowlisted patterns. Block if effects touch secrets,
  sensitive files, network egress, or privilege boundaries.

**Defense 4: Execute with guards**

- Timeouts, rate limits, per‑tool resource budgets; read/write
  allowlists; network egress rules. All effects logged with provenance.

**Defense 5: Detect and recover**

- Anomaly scoring over token trajectories and tool sequences;
  auto‑revoke tokens; show user‑visible explanations.

Readers with a security background may be tempted to map prompt
injection to SQL injection. The analogy is useful, but only up to a
point.

**Similar instincts:**

- **Normalize input:** SQL defenses sanitize or escape control
  characters; our Defense 1 normalization of Unicode/markup plays the
  same role.

- **Separate structure from data:** Prepared statements pre‑compile the
  query skeleton, then safely bind variables. Our analogue is
  schema‑constrained tool calls and capability planning.

- **Least privilege.** Database best practice avoids root connections;
  our stack insists on scoped tokens and pre‑authorized verbs.

- **Detect anomalies:** SQL firewalls and query monitoring flag
  tautologies like `OR 1=1`; we simulate and score odd tool
  trajectories.

**Where the analogy falls short:**

- **Language closure:** SQL has a bounded grammar; the “bad” patterns
  are finite. Natural language is open‑ended: every new structure is a
  potential contracrostic.

- **Interpreter generality:** SQL engines only interpret SQL. LLMs
  interpret *language itself*, which can fluidly express new forms of
  attack.

- **Surface area:** A DB user can only `SELECT`, `INSERT`, etc. A model
  with tools may touch HTTP, filesystems, APIs, shells. It’s a sprawling
  attack surface.

- **Human‑plausibility:** SQLi payloads look nonsensical to most humans.
  Prompt injection often reads like perfectly ordinary English, making
  detection ambiguous.

SQLi hardened down to a handful of canonical best practices; prepared
statements solved a lot of it. Prompt injection has no such silver
bullet. Survivor stacks are closer to intrusion‑tolerant systems:
layered defenses, provenance, simulation, and recovery.

Such a stack **reduces risk**, it does not promise perfection.
Hofstadter has the Tortoise spell it out:

> *It is simply an inherent fact about record players that they can’t do
> all that you might wish them to be able to do. But if there is a
> defect anywhere, it is not in THEM, but in your expectations of what
> they should be able to do! And the Crab was just full of such
> unrealistic expectations.*

Security is a property of a system‑in‑environment, not an intrinsic
halo. General interpreters plus untrusted instructions yield diagonal
failures. You can bound that risk (languages, tools, contexts); you
cannot engineer it away.

### A Brief Word on Gödel

In *Contracrostipunctus*, the Tortoise teases Achilles: “I don’t suppose
that you know Gödel’s Incompleteness Theorem…” You don’t need the
formalism to get the gist. [Gödel’s
move](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems)
was to construct a statement that **talks about the system** that tries
to prove it: a diagonal step that forces limits.

The moral for anyone deploying AI systems is conceptual, not formal:
whenever you build a powerful, general interpreter of strings, expect
there to be strings that **speak about your interpreter** and route
around your rules. The job is to constrain the language, the
environment, and the effects until the dangerous strings become either
inert or obvious.

### The Goblet and the Silence

*Contracrostipunctus* ends with a fragile image. Achilles gives the
Tortoise a glass goblet; moments later, while the Tortoise plays Bach, a
“shattering sound rudely interrupts his performance.”

> *And then… dead silence.*

Fault-tolerance isn’t a bug in complex systems; it’s a signature. The
work is not to imagine an unshatterable goblet or a perfect phonograph.
The work is to reduce risk, fail gracefully, and recover in ways that
honor the work at hand. Even if that means you now have a lower-fidelity
record player.

And if you haven’t read GEB, you should read GEB.
