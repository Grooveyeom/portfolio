#!/usr/bin/env python3
"""Builds index.html (AM default), am/index.html and ae/index.html from shared sections.
Edit text here, run `python3 build.py`, then commit and push.
Copy rules: short, precise sentences; every number that matters is shown as a chart or a big figure."""
import os

HEAD = """<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Jeonghun Yeom, {title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def top(role_label, other_href, other_label):
    return f"""<header class="wrap">
  <div class="top">
    <div class="name">Jeonghun Yeom <span>· {role_label} · Melbourne</span></div>
    <div class="actions">
      <a class="btn" href="mailto:mickey.yeom@gmail.com?subject=Role%20conversation">Email me</a>
      <a class="btn ghost" href="https://www.linkedin.com/in/jhyeom" rel="noopener">LinkedIn</a>
    </div>
  </div>
"""

def hero(h1, sub, kpis, flow):
    k = "".join(f'<div class="kpi"><b>{b}</b><span>{s}</span><em>{e}</em></div>' for b, s, e in kpis)
    f = "".join(f'<a href="#{i}"><i>{n:02d}</i><b>{t}</b><span>{d}</span></a>' for n, (i, t, d) in enumerate(flow, 1))
    return f"""  <div class="hero">
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="kpis">{k}</div>
    <nav class="toc" aria-label="On this page"><p class="toc-label">On this page</p><div class="flow" style="grid-template-columns:repeat({len(flow)},1fr)">{f}</div></nav>
  </div>
</header>
<main class="wrap" id="main">
"""

def sh(id_, step, h2, p=""):
    st = f'<div class="step">{step}</div>' if step else ""
    pp = f"<p>{p}</p>" if p else ""
    return f'<section id="{id_}" aria-labelledby="{id_}-h">\n  <div class="sh">{st}<h2 id="{id_}-h">{h2}</h2>{pp}</div>\n'

# ---------- shared blocks ----------

QUOTA = """<div class="card">
      <h3>Quota attainment</h3><p class="sub">Dashed line = 100% · blue = at or above</p>
      <div class="plot" role="img" aria-label="TeamViewer 2020 to 2024 above 100% every year; Nitro Q1 2026 106%, Q2 86%, Q3 97%">
        <div class="ref" style="bottom:80%"></div>
        <div class="b hi" style="--h:88%;flex:1.6"><span>100%+ every year</span></div>
        <div class="b hi" style="--h:84.8%"><span>106%</span></div>
        <div class="b" style="--h:68.8%"><span>86%</span></div>
        <div class="b" style="--h:77.6%"><span>97%</span></div>
      </div>
      <div class="xrow"><span style="flex:1.6">TeamViewer<br>2020–24</span><span>Nitro Q1<br>ramp</span><span>Nitro<br>Q2</span><span>Nitro<br>Q3</span></div>
      <p class="note">TeamViewer: personal net-new ARR quota. Nitro: quarterly expansion quota; Q2 is a CRM estimate.</p>
    </div>"""

RAMP = """<div class="card">
      <h3>Ramp at Nitro</h3><p class="sub">Incremental ACV per quarter, US$K, 2026</p>
      <div class="hbars" role="img" aria-label="Q1 36K, Q2 125K, Q3 159K">
        <div class="hb"><span class="t">Q1 (ramp)</span><div><div class="fill" style="--w:22.6%"></div></div><span class="n">36</span></div>
        <div class="hb"><span class="t">Q2</span><div><div class="fill" style="--w:78.6%"></div></div><span class="n">125</span></div>
        <div class="hb hi"><span class="t">Q3</span><div><div class="fill" style="--w:100%"></div></div><span class="n">159</span></div>
      </div>
      <div class="big"><b>4.4×</b><span>Q3 vs Q1 incremental ACV</span></div>
      <p class="note">First 90 days: 57 deals won; 19 of 26 renewals closed with a price increase.</p>
    </div>"""

SOURCE = """<div class="card">
    <h3>Where 2026 revenue came from</h3><p class="sub">Incremental ACV, US$373K, 342 closed deals, Jan–Oct 2026 (rounded)</p>
    <div class="split" role="img" aria-label="Renewal uplift 205K, 55%; expansion in existing accounts 139K, 37%; new customers 28K, 8%">
      <div style="flex:205;background:var(--accent)">Renewal uplift · 205K</div>
      <div style="flex:139;background:#5b7fd6">Expansion · 139K</div>
      <div style="flex:28;background:#93a9e4;color:var(--ink)">28K</div>
    </div>
    <div class="legend"><span>Renewal uplift: 183 deals</span><span>Expansion: 138 deals</span><span>New customers · 28K: 12 accounts</span></div>
  </div>"""

ESIGN = """<div class="card">
    <h3>E-signature cross-sell</h3><p class="sub">My 12 largest expansions, 2026</p>
    <div class="dots" role="img" aria-label="8 of 12 largest expansions included e-signature">""" + '<i class="on"></i>' * 8 + "<i></i>" * 4 + """</div>
    <div class="big"><b>8 of 12</b><span>included e-signature</span></div>
  </div>"""

DEALS = [
 ("Retail group, New Zealand", "Expansion · US$43K ACV",
  [("Challenge", "SSO test running up to the renewal date; every original contact had left"),
   ("What I did", "Briefed the reseller six weeks before a licensing change; rebuilt the contact map"),
   ("Result", "Order roughly doubled, with SSO")]),
 ("Aerospace group", "New account · Adobe replaced · 95 seats",
  [("Challenge", "Group-wide scope across subsidiaries and a reseller"),
   ("What I did", "Quoted one company first, with a dated plan for quote, PO and licences"),
   ("Result", "PO on the planned day; other subsidiaries following the same plan")]),
 ("Risk-services firm", "New account · DocuSign replaced · 3-year",
  [("Challenge", "Evaluating DocuSign; needed a CRM integration"),
   ("What I did", "Reissued a lapsed trial within an hour and agreed a decision date"),
   ("Result", "3-year Enterprise contract, 7 days after the opportunity opened")]),
 ("Wealth manager", "Renewal · ~40% larger",
  [("Challenge", "CFO rejected the first offer"),
   ("What I did", "Changed the deal shape, not the price: a pooled e-signature plan sized from their usage"),
   ("Result", "Closed in 39 days; first e-signature Enterprise purchase")]),
]

def deals(order):
    out = []
    for i in order:
        n, tag, rows = DEALS[i]
        dl = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows)
        out.append(f'<div class="deal"><div class="hd"><b>{n}</b><span>{tag}</span></div><dl>{dl}</dl></div>')
    return '<div class="g g-11">' + "".join(out) + "</div>"

FULL_CASE = """<div class="case">
    <h3>TeamViewer · self-service kiosk maker, Korea</h3>
    <p class="sub">Inbound lead to close, then expansion the next year · all stages mine</p>
    <div class="steps">
      <div><b>Qualify</b>Comparing products; needed remote access inside meal-ticket and booking kiosks.</div>
      <div><b>Demo</b>Presented the embedded use case.</div>
      <div><b>Trial</b>Ran the trial with regular check-ins.</div>
      <div><b>Close and expand</b>First deal about €7K. Added devices and upgraded the next year.</div>
    </div>
  </div>"""

TV_CASE = """<div class="case" style="margin-top:var(--gap)">
    <h3>TeamViewer · enterprise manufacturer · augmented reality</h3>
    <p class="sub">€189K opportunity I sourced · largest deal in TeamViewer APAC history</p>
    <div class="steps">
      <div><b>Source</b>Presented at SAP Sapphire Seoul; sourced and qualified the account.</div>
      <div><b>Discovery</b>Ran discovery; presented the business case to the CFO.</div>
      <div><b>Validate</b>Ran validation, then handed the technical evaluation to specialists.</div>
      <div><b>Close</b>Supported the commercial owner to PO: first APAC win for the product.</div>
    </div>
    <p class="note">I led the early stages; a specialist team ran the late stages.</p>
  </div>"""

ALLOCATE = """<div class="card">
      <h3>2026 renewals by contract size</h3><p class="sub">256 renewals in my territory</p>
      <div class="s100" role="img" aria-label="Accounts over US$10K: 16% of accounts and 47% of renewal revenue. All other accounts: 84% of accounts and 53% of revenue">
        <div><p class="lab">Number of accounts</p><div class="bar"><div class="t1" style="flex:16">16%</div><div class="rest" style="flex:84">84%</div></div></div>
        <div><p class="lab">Renewal revenue</p><div class="bar"><div class="t1" style="flex:47">47%</div><div class="rest" style="flex:53">53%</div></div></div>
      </div>
      <div class="legend"><span><i style="background:var(--accent)"></i>Accounts over US$10K: my time, weekly</span><span><i style="background:var(--context)"></i>All other accounts</span></div>
    </div>"""

TARGETING = """<div class="card">
      <h3>Targeting before outreach</h3>
      <div class="big"><b>170 → 10</b><span>accounts researched → qualified opportunities</span></div>
      <p class="t">Atlassian, one campaign. #2 in APJ.</p>
      <div class="big"><b>7</b><span>priority accounts in my 2026 plan</span></div>
      <p class="t">Each mapped: buyers, partner, contract, expansion path.</p>
    </div>"""

RISK = """<div class="g g-111">
    <div class="card"><h3>First contact before renewal</h3><p class="sub">Median days before renewal date</p>
      <div class="hbars" role="img" aria-label="Q1 2026 9 days, Q3 2026 63 days">
        <div class="hb"><span class="t">Q1 2026</span><div><div class="fill" style="--w:14.3%"></div></div><span class="n">9</span></div>
        <div class="hb hi"><span class="t">Q3 2026</span><div><div class="fill" style="--w:100%"></div></div><span class="n">63</span></div>
      </div></div>
    <div class="card"><h3>Win rate by price increase</h3><p class="sub">Share of renewals won</p>
      <div class="hbars" role="img" aria-label="All renewals 80%, increase 10 to 20% 90%, over 20% 69%">
        <div class="hb"><span class="t">All (215)</span><div><div class="fill" style="--w:80%"></div></div><span class="n">80%</span></div>
        <div class="hb hi"><span class="t">+10 to 20%</span><div><div class="fill" style="--w:90%"></div></div><span class="n">90%</span></div>
        <div class="hb"><span class="t">Over +20%</span><div><div class="fill" style="--w:69%"></div></div><span class="n">69%</span></div>
      </div></div>
    <div class="card"><h3>Rules from my data</h3>
      <ul><li>Increases over 20%: capped by distance from list price.</li><li>Partner-led renewals: I contact the customer directly.</li><li>Low usage: usage check 90 days before renewal.</li></ul></div>
  </div>
  <div class="card" style="margin-top:var(--gap)"><h3>Net revenue retention: 90.5%</h3><p class="sub">165 renewals, Apr–Sep 2026, churn included</p>
    <p class="t">26% of lost value came from partner-led renewals with no direct Nitro contact. I now contact those customers directly.</p></div>"""

PEOPLE = """<div class="g g-111">
    <div class="card"><h3>Partners and other teams</h3><div class="mini"><div><b>Resellers and distributors</b>Briefed before the customer; PO chased with the partner</div><div><b>Solutions engineers</b>Trials, SSO and integration scoping, with a decision date</div></div></div>
    <div class="card"><h3>Peers and leadership</h3><div class="mini"><div><b>Led a team of five</b>1:1s, pipeline and performance reviews, hiring panels</div><div><b>Mentored 15 colleagues</b>on deal execution</div></div></div>
    <div class="card"><h3>Operating rhythm</h3><div class="mini"><div><b>Weekly</b>Tier review, forecast with my director, one status email per distributor</div><div><b>Own tools</b>10+ scheduled AI agents on Claude, Salesforce and Slack</div></div></div>
  </div>"""

CAREER = """<div class="tl">
    <div class="r"><span class="y">2026–now</span><div class="w"><b>Nitro · Customer Account Executive, APAC</b><span>~480 accounts across ANZ and Southeast Asia, mostly through partners</span></div><span class="k">97% Q3</span></div>
    <div class="r"><span class="y">2025</span><div class="w"><b>Atlassian · Enterprise Development Rep, APAC</b><span>10 qualified opportunities from about 170 accounts</span></div><span class="k">#2 APJ</span></div>
    <div class="r"><span class="y">2020–24</span><div class="w"><b>TeamViewer · Account Executive → Senior Account Executive → Sales Lead (Player-Coach, APAC)</b><span>Personal net-new ARR quota above 100% every year; promoted twice; led five</span></div><span class="k">100%+</span></div>
    <div class="r"><span class="y">2018–20</span><div class="w"><b>Posway · Business Development Manager, Sydney</b><span>Cold calling, outbound and channel sales to SMB retail</span></div><span class="k"></span></div>
  </div>"""

def foot(root, other_href, other_label):
    return f"""</main>
<footer class="wrap">
  <div class="contact">
    <div><h2>Open to Commercial AE and Account Manager roles</h2><p>Australia · References available on request</p><p class="lang">Bilingual: English and Korean (native)</p></div>
    <div class="actions"><a class="btn" href="mailto:mickey.yeom@gmail.com?subject=Role%20conversation">mickey.yeom@gmail.com</a><a class="btn ghost" href="https://www.linkedin.com/in/jhyeom" rel="noopener">LinkedIn</a></div>
  </div>
  <p class="fine">Figures are from my own CRM and quota records, in US dollars unless stated and rounded. They describe results and do not prove cause. Customers are not named. <span class="switch"><a href="{other_href}">{other_label}</a></span></p>
</footer>
</body>
</html>
"""

# ---------- AM page ----------

def am(root, other):
    out = HEAD.format(title="Account Manager", desc="Jeonghun Yeom, B2B software account manager in Melbourne. Renewals, expansion and quota results, shown in numbers.", root=root)
    out += top("Account Manager", other, "AE version")
    out += hero("I grow renewal and expansion revenue across 480 software accounts.",
        "Nitro, ANZ and Southeast Asia. 7+ years in B2B sales at TeamViewer, Atlassian and Nitro.",
        [("US$344K", "added from existing customers", "Renewals and expansion, Jan–Oct 2026"),
         ("8 of 12", "largest expansions included e‑signature cross-sell", "Nitro, 2026"),
         ("97%", "of expansion quota, Q3 2026", "Nitro, after 106% in the ramp quarter"),
         ("100%+", "of personal quota, four years running", "TeamViewer, net-new ARR")],
        [("allocate", "Prioritise", "256 renewals by value"), ("grow", "Grow", "Where US$373K came from"),
         ("risk", "Retain", "Win rates and NRR"), ("returns", "Results", "Quota and ramp"),
         ("deals", "Deals", "Four customer deals")])
    out += sh("allocate", "1 · Prioritise", "I spend my time on the 16% of accounts that hold 47% of renewal revenue")
    out += f'<div class="g g-21">{ALLOCATE}{TARGETING}</div>\n</section>\n'
    out += sh("grow", "2 · Grow", "US$373K added across 342 deals in 2026")
    out += f'<div class="g g-21">{SOURCE}{ESIGN}</div>\n</section>\n'
    out += sh("risk", "3 · Retain", "Earlier contact, capped price increases")
    out += RISK + "\n</section>\n"
    out += sh("returns", "4 · Results", "Above quota four years running; 97% in Q3 at Nitro")
    out += f'<div class="g g-11">{QUOTA}{RAMP}</div>\n</section>\n'
    out += sh("deals", "5 · Deals", "Four deals: what I did and the result")
    out += deals([0, 3, 1, 2]) + "\n</section>\n"
    out += sh("people", "Working style", "How I work with people") + PEOPLE + "\n</section>\n"
    out += sh("career", "Experience", "Selected experience", "Full history on my CV and LinkedIn.") + CAREER + "\n</section>\n"
    return out + foot(root, other, "View the AE version")

# ---------- AE page ----------

def ae(root, other):
    out = HEAD.format(title="Account Executive", desc="Jeonghun Yeom, B2B software Account Executive in Melbourne. New business, competitive wins and territory management, shown in numbers.", root=root)
    out += top("Account Executive", other, "AM version")
    out += hero("I open new accounts, then grow them.",
        "Four years above net-new ARR quota at TeamViewer. Adobe and DocuSign replacements at Nitro. 7+ years in B2B sales.",
        [("100%+", "of net-new ARR quota, four years running", "TeamViewer, 2020–2024"),
         ("€189K", "enterprise opportunity I sourced", "TeamViewer, new product line"),
         ("2", "competitive replacements: Adobe, DocuSign", "Nitro, 2026, both new accounts"),
         ("97%", "of expansion quota, Q3 2026", "Nitro, after 106% in the ramp quarter")],
        [("new", "New business", "Quota and targeting"), ("case", "Cases", "Two sales, step by step"),
         ("deals", "Deals", "Four customer deals"), ("territory", "Results", "Quota and ramp")])
    out += sh("new", "1 · New business", "Four years above net-new quota",
        "Research the account, find the need, agree the next decision date.")
    out += f"""<div class="g g-111">
    <div class="card"><h3>Net-new quota</h3><div class="big"><b>4 yrs</b><span>above 100%, AE to Sales Lead</span></div><p class="t">TeamViewer net-new ARR. Own deals up to €25K. Top five in APAC in year one.</p></div>
    <div class="card"><h3>Targeting</h3><div class="big"><b>170 → 10</b><span>accounts researched → qualified opportunities</span></div><p class="t">Atlassian, one campaign. #2 in APJ.</p></div>
    <div class="card"><h3>New customers at Nitro</h3><div class="big"><b>12</b><span>new accounts in 2026</span></div><p class="t">In an installed-base role. Includes the Adobe and DocuSign replacements.</p></div>
  </div>
</section>
"""
    out += sh("case", "2 · Cases", "One sale end to end, one enterprise deal sourced") + FULL_CASE + TV_CASE + "\n</section>\n"
    out += sh("deals", "3 · Deals", "Four deals: what I did and the result")
    out += deals([1, 2, 0, 3]) + "\n</section>\n"
    out += sh("territory", "4 · Results", "Above quota four years running; 97% in Q3 at Nitro")
    out += f'<div class="g g-11">{QUOTA}{RAMP}</div>\n' + '<div style="margin-top:var(--gap)">' + SOURCE + "</div>\n</section>\n"
    out += sh("people", "Working style", "How I work with people") + PEOPLE + "\n</section>\n"
    out += sh("career", "Experience", "Selected experience", "Full history on my CV and LinkedIn.") + CAREER + "\n</section>\n"
    return out + foot(root, other, "View the AM version")

def write(path, html):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(html)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    write(os.path.join(here, "index.html"), am("", "ae/"))
    write(os.path.join(here, "am", "index.html"), am("../", "../ae/"))
    write(os.path.join(here, "ae", "index.html"), ae("../", "../am/"))
    print("built index.html, am/index.html, ae/index.html")
