#!/usr/bin/env python3
"""Builds index.html (AM default), am/index.html and ae/index.html from shared sections.
Edit text here, run `python3 build.py`, then commit and push."""
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
    f = "".join(f'<a href="#{i}">{t}</a>' for i, t, d in flow)
    return f"""  <div class="hero">
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="kpis">{k}</div>
    <nav class="section-nav" aria-label="On this page"><p class="nav-label">On this page</p><div class="section-links">{f}</div></nav>
  </div>
</header>
<main class="wrap" id="main">
"""

def sh(id_, step, h2, p=""):
    st = f'<div class="step">{step}</div>' if step else ""
    pp = f"<p>{p}</p>" if p else ""
    return f'<section id="{id_}" aria-labelledby="{id_}-h">\n  <div class="sh">{st}<h2 id="{id_}-h">{h2}</h2>{pp}</div>\n'

# ---------- shared blocks ----------

QUOTA = """<div class="card"><h3>Quota attainment</h3>
<p class="sub">Nitro · quarterly expansion quota · 2026</p>
<table class="results-table"><thead><tr><th scope="col">Period</th><th scope="col">Attainment</th></tr></thead><tbody><tr><th scope="row">Q1 · ramp</th><td>106%</td></tr><tr><th scope="row">Q2 · CRM estimate</th><td>86%</td></tr><tr><th scope="row">Q3</th><td>97%</td></tr></tbody></table>
<p class="note">At TeamViewer, I exceeded my personal annual net-new ARR quota for four years, progressing from Account Executive to Sales Lead. This annual measure is separate from Nitro's quarterly expansion target.</p></div>"""

RAMP = """<div class="card">
      <h3>Ramp at Nitro</h3><p class="sub">Incremental ACV per quarter, US$K, 2026</p>
      <div class="hbars" role="img" aria-label="Q1 36K, Q2 125K, Q3 159K">
        <div class="hb"><span class="t">Q1 (ramp)</span><div><div class="fill" style="--w:22.6%"></div></div><span class="n">36</span></div>
        <div class="hb"><span class="t">Q2</span><div><div class="fill" style="--w:78.6%"></div></div><span class="n">125</span></div>
        <div class="hb hi"><span class="t">Q3</span><div><div class="fill" style="--w:100%"></div></div><span class="n">159</span></div>
      </div>
      <p class="note">First 90 days: 57 deals won, 19 of 26 renewals closed with a price increase, 106% of both Q1 targets.</p>
    </div>"""

SOURCE = """<div class="card">
    <h3>Where 2026 revenue came from</h3><p class="sub">Incremental annual contract value (ACV), approximately US$373K across 342 closed deals, January to October 2026. Components are rounded separately.</p>
    <div class="split" role="img" aria-label="Renewal uplift 205K, 55%; expansion in existing accounts 139K, 37%; new customers 28K, 8%">
      <div style="flex:205;background:var(--accent)">Renewal uplift · 205K</div>
      <div style="flex:139;background:#5b7fd6">Expansion in existing accounts · 139K</div>
      <div style="flex:28;background:#93a9e4;color:var(--ink)">New · 28K</div>
    </div>
    <div class="legend"><span>Renewal uplift: 183 deals</span><span>Expansion (seats, upgrades, cross-sell): 138 deals</span><span>New customers: 12 accounts, 21 deals</span></div>
  </div>"""

DEALS = [
 ("Retail group, New Zealand", "Expansion · US$43K ACV",
  [("Parties", "Customer IT and security, reseller, distributor"), ("Technical", "Single sign-on test that ran to the renewal date"),
   ("What I did", "Briefed the reseller six weeks before a licensing change; found new contacts after every old one had left"), ("Outcome", "Order roughly doubled, with SSO")]),
 ("Aerospace group", "New account · Adobe replaced · 95 seats",
  [("Parties", "Parent group and subsidiaries, reseller"), ("Structure", "Group-wide scope; one company quoted first so the date would hold"),
   ("What I did", "Wrote a dated plan for quote, reseller, PO and licences"), ("Outcome", "PO on the planned day; other subsidiaries working from the same plan")]),
 ("Risk-services firm", "New account · DocuSign replaced · 3-year",
  [("Parties", "Customer team evaluating DocuSign"), ("Technical", "Trial plus a CRM integration"),
   ("What I did", "Reissued a lapsed trial within an hour and agreed a decision date"), ("Outcome", "Three-year Enterprise contract, 7 days after the opportunity opened")]),
 ("Wealth manager", "Renewal · ~40% larger",
  [("Parties", "CFO, reseller"), ("Structure", "Pooled e-signature plan sized from their own usage"),
   ("What I did", "After the CFO rejected the first offer, changed the shape of the deal instead of the price"), ("Outcome", "Closed in 39 days; first e-signature Enterprise purchase")]),
]

def deals(order):
    out = []
    for i in order:
        n, tag, rows = DEALS[i]
        dl = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows)
        out.append(f'<div class="deal"><div class="hd"><b>{n}</b><span>{tag}</span></div><dl>{dl}</dl></div>')
    return '<div class="g g-11">' + "".join(out) + "</div>"

FULL_CASE = """<div class="case" style="margin-bottom:10px">
    <h3>TeamViewer · Korean self-service kiosk maker · embedded remote access</h3>
    <p class="sub">Full cycle, owned by me: inbound lead to close, then expansion the next year</p>
    <div class="steps">
      <div><b>Qualify</b>Inbound lead comparing us with other products. They needed remote access built into their meal-ticket and restaurant-booking kiosks.</div>
      <div><b>Demo</b>Product presentation and a meeting on the embedded use case.</div>
      <div><b>Trial</b>Set up a trial and checked progress with them on a regular cadence.</div>
      <div><b>Close and expand</b>Won the first deal, about €7K. The next year they added devices and upgraded.</div>
    </div>
  </div>"""

TV_CASE = """<div class="case">
    <h3>TeamViewer · enterprise manufacturer · augmented-reality platform</h3>
    <p class="sub">€189K opportunity I sourced on a new product line, the largest deal in TeamViewer APAC history</p>
    <div class="steps">
      <div><b>Source</b>Presented the product at SAP Sapphire Seoul to build industrial pipeline. Sourced and qualified the account.</div>
      <div><b>Discovery</b>Ran discovery on the use case and presented the business case to the CFO.</div>
      <div><b>Validate</b>Ran validation with the customer, then handed the technical evaluation to the specialist team.</div>
      <div><b>Close</b>Supported the commercial owner through to purchase order, which became the first APAC win for that product.</div>
    </div>
    <p class="note">I led the early stages. The late technical and commercial stages were run by a specialist team.</p>
  </div>"""

ALLOCATE = """<div class="card">
      <h3>2026 renewals: share of accounts vs share of value</h3><p class="sub">256 renewals in my territory</p>
      <div class="pairs" role="img" aria-label="Renewals over 10K: 16% of accounts, 47% of value. 3K to 10K: 41% of accounts, 37% of value. Under 3K: 43% of accounts, 16% of value">
        <div class="pr"><div class="t"><b>Tier 1 · US$10K+</b>my time, weekly</div><div class="bars"><div class="row"><div class="fill" style="--w:16%"></div><span>16%</span></div><div class="row val"><div class="fill" style="--w:47%"></div><span>47%</span></div></div></div>
        <div class="pr"><div class="t"><b>Tier 2 · US$3–10K</b>sequences I review</div><div class="bars"><div class="row"><div class="fill" style="--w:41%"></div><span>41%</span></div><div class="row val"><div class="fill" style="--w:37%"></div><span>37%</span></div></div></div>
        <div class="pr"><div class="t"><b>Tier 3 · under US$3K</b>largely automated</div><div class="bars"><div class="row"><div class="fill" style="--w:43%"></div><span>43%</span></div><div class="row val"><div class="fill" style="--w:16%"></div><span>16%</span></div></div></div>
      </div>
      <div class="legend"><span><i style="background:var(--context)"></i>Share of accounts</span><span><i style="background:var(--accent)"></i>Share of value</span></div>
    </div>"""

TARGETING = """<div class="card">
      <h3>Targeting before outreach</h3>
      <div class="big"><b>170 → 10</b><span>target accounts to qualified opportunities</span></div>
      <p class="t">At Atlassian I researched and mapped about 170 mid-market, enterprise and strategic accounts, and built 10 qualified opportunities in one campaign, second in APJ.</p>
      <div class="big"><b>7</b><span>priority accounts in my 2026 plan</span></div>
      <p class="t">Each with an account map: buyers, partner, contract, expansion path.</p>
    </div>"""

RISK = """<div class="g g-111">
    <div class="card"><h3>Starting earlier</h3><p class="sub">Median first contact before renewal</p>
      <div class="pair"><div><b>9</b><span>days, Q1 2026</span></div><div class="arrow" aria-hidden="true">→</div><div class="hi"><b>63</b><span>days, Q3 2026</span></div></div></div>
    <div class="card"><h3>Renewal win rates by price increase</h3><p class="sub">Renewals won, by size of increase</p>
      <div class="hbars" role="img" aria-label="All renewals 80%, increase 10 to 20% 90%, over 20% 69%">
        <div class="hb"><span class="t">All (215)</span><div><div class="fill" style="--w:80%"></div></div><span class="n">80%</span></div>
        <div class="hb hi"><span class="t">+10 to 20%</span><div><div class="fill" style="--w:90%"></div></div><span class="n">90%</span></div>
        <div class="hb"><span class="t">Over +20%</span><div><div class="fill" style="--w:69%"></div></div><span class="n">69%</span></div>
      </div></div>
    <div class="card"><h3>Rules I changed from my own data</h3>
      <ul><li>Increases over 20% lost more: now capped by how close an account is to list.</li><li>Lost partner-led renewals highlighted gaps in customer contact. I now contact customers directly.</li><li>Low-usage accounts churned: usage check 90 days before every renewal.</li></ul></div>
  </div>"""

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
    <div><h2>Open to Commercial AE and Account Manager roles</h2><p>Australia. English and Korean. References available on request.</p></div>
    <div class="actions"><a class="btn" href="mailto:mickey.yeom@gmail.com?subject=Role%20conversation">mickey.yeom@gmail.com</a><a class="btn ghost" href="https://www.linkedin.com/in/jhyeom" rel="noopener">LinkedIn</a></div>
  </div>
  <p class="fine">Figures are from my own CRM and quota records, in US dollars unless stated and rounded. They describe results and do not prove cause. Customers are not named. <span class="switch"><a href="{other_href}">{other_label}</a></span></p>
</footer>
</body>
</html>
"""

# ---------- AM page ----------

def am(root, other):
    out = HEAD.format(title="Account Manager", desc="Jeonghun Yeom, B2B software account manager in Melbourne. Customer growth, renewals and selected sales cases.", root=root)
    out += top("Account Manager", other, "AE version")
    out += hero("I help software customers renew, expand and switch with confidence.",
        "I manage around 480 customer accounts across ANZ and Southeast Asia at Nitro. My work brings together customer discovery, commercial negotiation and reseller coordination. Previously at TeamViewer and Atlassian; 7+ years in B2B sales.",
        [("US$344K", "incremental annual contract value from existing customers", "Renewal uplift plus expansion, Jan to Oct"),
         ("~480", "customer accounts across ANZ and Southeast Asia", "Nitro · renewals and expansion"),
         ("97%", "of expansion quota in Q3 2026", "Nitro, after 106% in the ramp quarter"),
         ("100%+", "of personal quota every year for four years", "TeamViewer, net-new ARR")],
        [("deals", "Selected deals", ""), ("allocate", "How I work", ""), ("returns", "Track record", "")])
    out += sh("deals", "", "Selected customer deals", "Examples of how I worked through technical requirements, pricing objections and purchasing deadlines.")
    out += deals([0, 3, 1, 2]) + "\n</section>\n"
    out += sh("allocate", "Account management", "How I prioritise a territory of 480 accounts", "I plan account coverage around renewal value. Larger accounts receive weekly attention; smaller accounts follow structured outreach and automated reminders.")
    out += f'<div class="g g-21">{ALLOCATE}{TARGETING}</div>\n</section>\n'
    out += sh("grow", "Revenue growth", "How I grow existing customer revenue", "I review usage with customers to identify additional seats, suitable plans and e-signature needs. E-signature featured in eight of my twelve largest expansions, alongside renewal price increases and competitive replacements.")
    out += SOURCE + "\n</section>\n"
    out += sh("risk", "Retention", "What retention data changed about my approach")
    out += RISK + """
    <div class="card" style="margin-top:24px"><h3>Net revenue retention: 90.5%</h3><p class="sub">165 renewals, April to September 2026, churn included</p>
      <p class="t">My book is mostly small businesses buying through resellers. Most of the lost value sat in two places: renewals under US$10K, and partner-led renewals where no one at Nitro had spoken to the customer directly (26% of lost renewal value). Both are now covered by the rules above: a direct contact 90 days out, and a usage check before every renewal.</p></div>
""" + "\n</section>\n"
    out += sh("returns", "Performance", "Performance against target")
    out += f'<div class="g g-11">{QUOTA}{RAMP}</div>\n</section>\n'
    out += sh("people", "", "How I work with people") + PEOPLE + "\n</section>\n"
    out += sh("career", "", "Selected experience", "Full history on my CV and LinkedIn.") + CAREER + "\n</section>\n"
    return out + foot(root, other, "View the AE version")

# ---------- AE page ----------

def ae(root, other):
    out = HEAD.format(title="Account Executive", desc="Jeonghun Yeom, B2B software Account Executive in Melbourne. New business, competitive wins and territory management, shown in numbers.", root=root)
    out += top("Account Executive", other, "AM version")
    out += hero("I open new accounts, then grow them.",
        "Four years carrying a net-new ARR quota, then competitive wins and expansion across a territory of about 480 accounts. 7+ years in B2B sales, including TeamViewer, Atlassian and Nitro.",
        [("100%+", "of personal net-new ARR quota every year for four years", "TeamViewer, 2020 to 2024"),
         ("€189K", "enterprise opportunity I sourced and led to validation", "TeamViewer, new product line"),
         ("2", "competitive replacements: Adobe and DocuSign", "Nitro, 2026, both new accounts"),
         ("97%", "of expansion quota in Q3 2026", "Nitro, after 106% in the ramp quarter")],
        [("new", "How I work", ""), ("case", "Selected deals", ""), ("territory", "Track record", "")])
    out += sh("new", "1 · New business", "How I win new business", "I research the account, establish a customer need and agree the next decision with the buyer.")
    out += f"""<div class="g g-111">
    <div class="card"><h3>Net-new quota</h3><div class="big"><b>4 yrs</b><span>above 100%, AE to Sales Lead</span></div><p class="t">TeamViewer net-new ARR, closing my own deals up to €25K with IT managers, engineers and procurement. Top five in APAC in my first year.</p></div>
    <div class="card"><h3>Targeting</h3><div class="big"><b>170 → 10</b><span>accounts to qualified opportunities</span></div><p class="t">Atlassian outbound campaign: researched and mapped each account, second in APJ.</p></div>
    <div class="card"><h3>New customers at Nitro</h3><div class="big"><b>12</b><span>new accounts in 2026</span></div><p class="t">In a role measured on the installed base, including the Adobe and DocuSign replacements and accounts I prospected myself.</p></div>
  </div>
</section>
"""
    out += sh("case", "2 · Two cases", "A full-cycle sale and an enterprise opportunity", "A small new customer I took from first call to renewal growth, and a large enterprise opportunity I sourced.") + FULL_CASE + TV_CASE + "\n</section>\n"
    out += sh("deals", "3 · Deals", "Selected customer deals", "My role, the people involved and the outcome of each deal.")
    out += deals([1, 2, 0, 3]) + "\n</section>\n"
    out += sh("territory", "4 · Territory", "Results, and where my time goes")
    out += f'<div class="g g-11">{QUOTA}{ALLOCATE}</div>\n' + '<div style="margin-top:24px">' + SOURCE + "</div>\n</section>\n"
    out += sh("people", "", "How I work with people") + PEOPLE + "\n</section>\n"
    out += sh("career", "", "Selected experience", "Full history on my CV and LinkedIn.") + CAREER + "\n</section>\n"
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


