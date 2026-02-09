# Quick DataViz With Claude Code
Matt Hodges
2026-01-20

I previously wrote about how you can [use VisiData to quickly scrape
HTML tabular data](https://matthodges.com/posts/2025-09-30-visidata/).
Claude Code with Opus 4.5 is another excellent data exploration
sidekick. This is what ‘agentic’ looks like in practice.

Using the same Federal Reserve [list of the largest commercial
banks](https://www.federalreserve.gov/releases/lbr/current/), I started
a Claude Code session and prompted:

> Can you go to the page at
> https://www.federalreserve.gov/releases/lbr/current/ and discover the
> table of large commercial banks; then give me a bar graph of the top
> 10 by Consol Assets. Use uv for any dependencies you need. You
> probably want to use pandas read_html() to get the tables and then
> matplotlib with nice styling to create the viz

It spun for a bit and then produced [some
Python](https://gist.github.com/hodgesmr/e24559c17b979dffa452851373500292).
Sometimes agents will try to run this kind of thing as a tidy [here
document](https://en.wikipedia.org/wiki/Here_document), but not always.
So I like to do this sort of thing in a scratch directory that it can
toss files in. This time, it tossed a `bank_chart.py`, which it ran
itself like this:

``` sh
uv run \
  --with pandas \
  --with matplotlib \
  --with lxml \
  --with html5lib \
  --with requests \
  python bank_chart.py
```

On first run, it realized the Fed has opinions about the `User-Agent`
header (VisiData also hit this issue), so it did the thing everyone does
when scripting HTTP calls and made it look like a browser:

> The Fed website is blocking the pandas request. I need to use a proper
> user agent header to fetch the content. Let me use requests to
> download the HTML first, then parse it with pandas.

``` diff
--- a/bank_chart.py
+++ b/bank_chart.py
@@ -1,6 +1,15 @@
 import pandas as pd
 import matplotlib.pyplot as plt
+import requests
+from io import StringIO
 
-# Fetch the table from the Federal Reserve page
+# Fetch the table from the Federal Reserve page with proper headers
 url = "https://www.federalreserve.gov/releases/lbr/current/"
-tables = pd.read_html(url)
+headers = {
+    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
+}
+response = requests.get(url, headers=headers)
+response.raise_for_status()
+
+tables = pd.read_html(StringIO(response.text))
```

It then ran again, successfully, and produced the following graph, both
as a PNG and PDF:

![Top 10 Large Commercial Banks by Consolidated Assets (Federal Reserve
Data, September 2025)](top10_banks.png)

The whole thing took about two minutes from prompt to viz.

I think a lot of people still view tools like Claude Code as AI that
builds software for people who sell software. But we need to think about
them as [general purpose agents that help us get work
done](https://matthodges.com/posts/2026-01-07-ai-agents-campaigns/).

Not bad for a single prompt.
