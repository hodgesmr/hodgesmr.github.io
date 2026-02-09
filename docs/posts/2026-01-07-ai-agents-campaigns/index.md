# Campaigns Are Knowledge Workers and the Tools Just Caught Up
Matt Hodges
2026-01-07

Over the past few weeks, something shifted in the AI conversation.
Claude Code, which had been available for the better part of 2025,
gained the [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
model, and developers lost their minds. Andrej Karpathy posted, [“I’ve
never felt this much behind as a
programmer”](https://xcancel.com/karpathy/status/2004607146781278521).
Google engineers [reported recreating months of work in
hours](https://xcancel.com/rakyll/status/2007239758158975130). It’s
difficult to talk about this shift without sounding like an AI
influencer-grifter, but the reaction was near-universal: this is
different.

If your day job involves persuading voters, building coalitions, and
running campaigns, it’s tempting to shrug. *Cool. The engineers have new
toys.*

That shrug is going to age poorly.

Because the important development isn’t “AI can code.” The important
development is: AI can use code to do work. And most campaign work
happens through software. The question isn’t “is this a coding task?”
The question is: **can this be done on a computer?**

If yes, you’re looking at tools that can handle the mechanical work that
eats up campaign staff energy: searching, summarizing, transforming,
moving information across systems. Not the judgment calls. Not the
relationship-building. Not the strategy. But the tedious, repetitive,
soul-crushing work that keeps smart people from doing what they’re
actually good at. These tools can do that work at scale, in the messy
reality of modern campaign operations.

To be clear: this isn’t about AI-generated content. The political AI
conversation has been dominated by slop: cheaply generated images,
robotic fundraising emails, uncanny video ads. That’s a real problem
that’s eroding social trust, but it’s not what I’m talking about.
Agentic AI isn’t about producing more stuff. It’s about operating the
systems that produce, organize, and move information. The difference
matters.

This isn’t a developer story. It’s a campaign knowledge story.

### The Misleading Word in “Coding Agent”

When most people hear “coding,” they picture a specialist skill for a
specialist domain. A software engineer building software. Most campaigns
don’t have a software engineer.

But code is not sacred. Code is just instructions, it’s a language we
use to tell computers to do things. If an AI can reliably write and
execute those instructions, then the boundary of what it can do isn’t
“software engineering.”

It’s your laptop.

- Spreadsheets are code, with a friendlier UI.
- CRMs are code, behind an admin panel.
- Compliance tooling is code, wrapped in forms and rules.
- Digital ad platforms are code, with budgets and knobs.
- Analytics pipelines are code, and they influence every decision you
  make.

Successful campaigns don’t run on vibes. They run on systems: databases,
tools, dashboards, inboxes, calendars, shared drives, web UIs held
together by rituals and institutional memory.

A tool that can *operate those systems*, not just chat about them, isn’t
a better chatbot. It’s a new kind of capacity.

### Campaigns Are Mostly Knowledge Workers

Here’s what political people know but rarely say out loud: campaigns are
giant, deadline-driven startups of knowledge work.

Not “knowledge work” in the TED Talk sense. Knowledge work in the gritty
sense:

- reading and extracting
- comparing and reconciling
- drafting and reformatting
- triaging and escalating
- cleaning and validating
- coordinating and scheduling
- assembling packets, briefs, memos, scripts, cutlists, talking points,
  call time prep
- turning raw inputs into something a decision-maker can act on

A frightening amount of campaign labor is the same pattern repeated:
take a messy pile of inputs, turn it into something legible, then turn
that into action.

That is exactly the pattern these agentic tools are getting good at. And
campaigns have endless [messy piles of
inputs](https://en.wikipedia.org/wiki/The_American_Voter).

### We’ve Seen This Movie Before

In 2020, while leading the Biden campaign’s engineering team, [we built
early versions of what these tools now do out of the
box.](https://danveloper.medium.com/artificial-intelligence-on-the-biden-campaign-e704a656d956)
We had automatic speech-to-text with real-time speaker diarization so
our research team could dig into debate transcripts the moment they
happened. We built semantic search across web, video, and podcast media
so digital staff could find the exact clip they needed. We pushed
browser automation to move data between the clunky legacy systems that
every campaign inherits. [Nobody thinks of this stuff as “AI”
today](https://en.wikipedia.org/wiki/AI_effect#Definition), but our
piles of TensorFlow weirdware felt cutting-edge back then.

The capability existed in pieces. Integration was the hard part.

Getting each component working took real engineering. Wiring them into
reliable, repeatable workflows took even more. And adoption was uneven
because access was uneven. Teams with technical know-how used these
tools constantly; teams without barely touched them.

Then the campaign ended, and all of it evaporated.

That’s the campaign technology pattern I’ve watched repeat for over a
decade: brilliant, bespoke solutions built under pressure, then
abandoned when the cycle ends. The institutional knowledge walks out the
door. The next cycle starts from scratch.

What’s different now is generality. These agents don’t just generate
code for engineers to review. They *use* code to accomplish tasks like
navigating browsers, manipulating files, moving between systems. The
integration problem doesn’t disappear, but the barrier drops
dramatically.

The lesson I learned the hard way: capabilities arrive in fragments, and
integration is the hard part. That’s still true. But the fragments are
bigger now, and they snap together faster.

### What This Actually Looks Like

Let’s be concrete about where this lands in campaign work.

**Comms and rapid response** is where the ROI hits first. A lot of rapid
response isn’t writing, it’s everything around writing. Pull the
relevant clips from a debate transcript. Find the prior quote from six
years ago, plus the local angle. Summarize what’s actually going viral,
not what you wish was going viral. Draft three variants: statement,
social copy, surrogate bullets. Generate a briefing doc with links and
provenance so the comms director trusts it. Cut a “creator-ready”
packet: 30-second version, caption variants, context notes.

If you’ve ever watched a comms team lose an hour hunting for the same
receipts they hunted for last week, you know how these gains compound.

**Finance and fundraising** is where the leverage is hiding in plain
sight. The digital program alone generates endless grunt work: writing
seventeen variants of the same end-of-quarter email to test subject
lines, building SMS flows that branch based on giving history,
reconciling ActBlue exports against your CRM at 11pm, figuring out why
your recurring donor retention rate cratered last month. Then there’s
the stewardship nobody has time for: the thank-you sequences that should
feel personal but don’t, the post-event follow-ups that slip through the
cracks, the lapsed-donor reactivation campaigns you keep meaning to
build. An agent that can draft copy variants, analyze which segments are
actually responding to which asks, and flag the recurring donors who
just fell out of your latest filing isn’t replacing your finance team,
it’s giving them back the hours they’re currently spending in
spreadsheet hell.

Call time still matters, of course. The research-to-call-sheet pipeline
is a natural fit: pull giving history, find recent board memberships,
draft personalized ask language, log the notes afterward. But the real
volume is in the grassroots program, and that’s where the gains
compound. If your Digital Fundraising Director can test twice as many
donation page variants, or your Finance Associate can actually build
that monthly donor upgrade sequence instead of just talking about it,
you’re not just saving time, you’re raising more money. In a cycle where
small-dollar fundraising will matter more than ever, that’s the game.

**Listening at scale** is the one that might matter most. Field teams
drown in qualitative data: canvass notes, house party feedback,
volunteer debriefs, open-ended survey responses, social comments from
community groups. The tragedy is that we collect a ton of signal and
then fail to convert it into shared understanding.

Agents are increasingly good at:

- clustering themes without flattening everything into mush
- surfacing what changed since last week
- producing reviewable summaries with links back to the raw text

This is what “listening at scale” should mean: not replacing organizers,
but amplifying their ability to hear patterns early and translate what
they hear into narratives that feel true in people’s lives.

**Research** is half insight and half mechanics. The mechanics are
brutal: monitor media across dozens of geographies and channels, [track
filings](https://matthodges.com/posts/2025-12-19-ai-agent-fec/) and
records, keep a living dossier updated as new facts drop. A good agent
doesn’t need to be a genius researcher. It needs to be a relentless one.

### The Two-Tier Risk

Here’s what worries me.

Right now, there’s a meaningful barrier to entry for these tools. You
need to be comfortable with a terminal window and a handful of basic
commands. This isn’t hard, but it’s intimidating enough to create a
split: the people who learn the workflows compound their productivity
quickly, and everyone else hears about it in annoying LinkedIn posts,
wondering why they feel behind.

For Democratic political staff, this is an acute risk. Our coalition
depends on down-ballot races, state parties, and grassroots
organizations that have never had the technical resources of
presidential campaigns. If agentic AI remains “for engineers only,” the
productivity gap between well-resourced and under-resourced campaigns
will widen dramatically, and it’ll widen fastest in exactly the races
where we can least afford it.

The good news is that accessibility is a UX problem, and UX problems get
solved. We’re already seeing agent capabilities land in
[spreadsheets](https://claude.com/claude-in-excel),
[browsers](https://code.claude.com/docs/en/chrome), and [familiar
interfaces](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server).
But in the window before it becomes seamless, early adopters will pull
away.

If every well-funded campaign builds bespoke mini-machines while
everyone else waits for permission, we don’t get a movement capability.
We get a handful of fragile miracles and a much longer tail of campaigns
[stuck in the last
cycle](https://campaignsandelections.com/voices/democrats-still-arent-ready-for-2026/).
The path forward runs through the organizations that don’t shut down in
November: party committees, major vendors, funders who take
infrastructure seriously, and the handful of political tech orgs
building for the long haul.

### The Shadow AI Trap

There’s an obvious failure mode here: everyone quietly experimenting,
pasting sensitive data into whatever tool is easiest, building brittle
automations with no discernible schema, accidentally recreating the
worst parts of shadow IT but with higher stakes.

Agentic tools reach across systems: files, browsers, inboxes, CRMs. That
means governance can’t be an afterthought or a scolding memo. It has to
be defaults: what data is allowed where, what gets automated, what
requires approval, what runs in a sandbox.

The goal is not to slow people down. The goal is to prevent the
inevitable [“we moved fast and broke
trust”](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
moment that causes a backlash and sets adoption back a cycle. Campaigns
can’t hold institutional memory about what went wrong because they
dissolve. The enduring organizations have to own governance, because
they’re the ones who’ll still be around to learn from the mistakes.

### What to Do Now

Individual experimentation is fine, but it’s not sufficient. If the last
decade of Democratic technology has taught us anything, it’s that
innovation without infrastructure just produces a graveyard of one-off
solutions. The work that matters now is building shared, composable
capacity that outlasts any single campaign.

That means the institutional actors have to lead.

**Party committees** need to treat agentic AI as core infrastructure,
not innovation theater. That means dedicated technical staff evaluating
tools, building reusable workflows, and making them available to
down-ballot campaigns that will never have their own AI strategy.
National committees should be standing up these shared services, not
just issuing guidance memos.

**Vendors and tool-builders** should be building agent capabilities into
the platforms campaigns already use. The goal isn’t a new AI product to
sell; it’s making the existing stack smarter. If you build campaign
tech, the question is: what mechanical work can agents automate so your
users can focus on judgment and relationships?

**Major funders** need to back infrastructure, not just applications,
and definitely not just ad mills. That means supporting the unsexy work:
integration layers, shared tooling, governance frameworks, training
programs. It means backing organizations that will maintain and improve
these capabilities across cycles, not just campaigns that will use them
once and disappear.

**Tech-forward political organizations** that persist between elections
should be the R&D layer for the movement. Test workflows, document what
works, publish patterns that others can adopt. Build the institutional
memory that campaigns can’t.

For those experimenting now, two principles:

**Bias toward real workflows.** Not “build the future of AI.” Pick the
task you do every week that makes you groan. Start there. High-frequency
tasks where saved time compounds.

**Design for review, not autonomy.** Have the agent produce outputs a
human can verify: citations, diffs, structured summaries, highlighted
uncertainties. The goal is human-in-the-loop, not human-out-of-the-way.
Judgment stays with people, because political work is still inherently
about people.

None of this requires believing in AGI fantasies. It requires noticing
what’s in front of us: campaign staff are buried in mechanical knowledge
work. Scarce energy is spent on tedious, repetitive tasks that crowd out
strategic thinking. And the tools that can handle a lot that work are
finally here and improving rapidly. The organizations that treat this as
a real infrastructure priority will free their people to do what humans
are actually good at: building relationships, making judgment calls,
being an authentic voice, and persuading voters.

Not louder machines. Better listeners. Faster integrators. Teams with
room to think.

Agentic AI will transform knowledge work this year. The only question is
whether we build the shared capacity to make it Democrats’ advantage, or
explain after the fact why we let another cycle of innovation pass.
