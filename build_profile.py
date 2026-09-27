"""Rebuild the live parts of the Mahimai Labs organization profile (profile/README.md).

Runs in GitHub Actions every six hours (see .github/workflows/build.yml) and on demand. Each
live section of profile/README.md sits between a pair of markers,

    <!-- projects_products starts -->
    ...
    <!-- projects_products ends -->

and only the text between them is rewritten. It also draws the brand banner in profile/assets/.

Every source is fetched on its own. A source that fails keeps its section's previous content
and the rest still update; an empty but successful result replaces stale content.

Standard library only, so the workflow needs no install step. To test without the network,
point README_FIXTURES at a directory of saved responses (org_repos.json, merged.json, feed.xml,
pypi__<name>.json):

    README_FIXTURES=/path/to/fixtures python build_profile.py
"""

from __future__ import annotations

import base64
import json
import math
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = pathlib.Path(__file__).parent.resolve()
README = ROOT / 'profile' / 'README.md'
ASSETS = ROOT / 'profile' / 'assets'
BRAND = ASSETS / 'brand'

ORG = 'mahimailabs'
USER = ORG
FEED_URL = 'https://mahimai.ca/feed.xml'

# The public projects the page lists, by group. Descriptions and stars come from GitHub; a PyPI
# name adds the latest release. A new repository appears once it is added here.
GROUPS = {
    'products': [
        ('voicegateway', 'voicegateway'),
        ('openrtc-runtime', 'openrtc'),
        ('livekit-plugins-voicemem', 'livekit-plugins-voicemem'),
        ('shipvoice', None),
        ('envoic', 'envoic'),
    ],
    'data': [
        ('voice-prices', 'voice-prices'),
        ('voice-ai-skills', None),
        ('voice-latency', 'voice-latency'),
        ('handset-bench', 'handset-bench'),
    ],
    'examples': [
        ('gpt-live-voice-agent', None),
        ('voicemem-demo', None),
        ('voicegateway-examples', None),
    ],
}
# How the page describes each project, in the company's voice. A repository without an entry
# falls back to its GitHub description.
DESCRIPTIONS = {
    'voicegateway': 'Cost tracking, observability and inference routing for voice agents on LiveKit, Pipecat and OpenRTC.',
    'openrtc-runtime': 'Runs many LiveKit voice agents in one Python worker, sharing heavy models instead of loading them per process.',
    'shipvoice': 'Full-stack LiveKit voice agent starter: a Python voice worker, a FastAPI token server and a React frontend, each deployable on its own.',
    'envoic': 'Finds and reports the Python virtual environments on a machine, so they stop piling up.',
    'voice-prices': 'Open price database for voice AI APIs: STT, LLM, TTS, speech-to-speech and VAD.',
    'voicegateway-examples': 'Example projects that run on VoiceGateway.',
}
# Sites some projects publish, shown next to the repository link.
SITES = {
    'voice-prices': 'https://prices.mahimai.ca',
    'voice-ai-skills': 'https://skills.mahimai.ca',
}

THEMES = {
    'dark': {'bg': '#0a0a0a', 'surface': '#141414', 'line': '#262626', 'ink': '#fafafa', 'muted': '#a3a3a3',
             'accent': '#cba6f7', 'accent2': '#86efac', 'blue': '#89b4fa'},
    'light': {'bg': '#fcfcfc', 'surface': '#f3f3f4', 'line': '#e3e3e6', 'ink': '#0a0a0a', 'muted': '#55555c',
              'accent': '#6f3fb0', 'accent2': '#15803d', 'blue': '#1e66f5'},
}
SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

FIXTURES = os.environ.get('README_FIXTURES')
TOKEN = os.environ.get('GITHUB_TOKEN', '')


# --- Fetching -------------------------------------------------------------------------------

def fetch(url: str, *, data: bytes | None = None, accept: str = 'application/json') -> bytes:
    """GET (or POST) with retries on the transient errors GitHub and PyPI return under load.

    GitHub signals a rate limit with 429, or with 403 plus a Retry-After header, a zero
    remaining quota, or "rate limit" in the body. Those wait as long as GitHub asks (up to
    90 s) and retry. A 401 or 403 that refuses the token itself is retried once without it,
    since every source here is public. Any other error is raised with GitHub's own message.
    """
    headers = {'User-Agent': f'{USER}-profile-readme', 'Accept': accept}
    if TOKEN and url.startswith('https://api.github.com/'):
        headers['Authorization'] = f'Bearer {TOKEN}'
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode(errors='replace')
            retry_after = e.headers.get('Retry-After')
            reset = e.headers.get('X-RateLimit-Reset')
            limited = e.code == 429 or (e.code == 403 and (
                retry_after or e.headers.get('X-RateLimit-Remaining') == '0' or 'rate limit' in body.lower()))
            # Everything read here is public. When an organization refuses the token itself (for
            # example a policy on token lifetime), ask again without it rather than lose the section.
            if e.code in (401, 403) and not limited and 'Authorization' in headers and data is None:
                print(f'  {url.split("?")[0]}: token refused ({body.strip()[:120]}); retrying without it')
                del headers['Authorization']
                continue
            if not (limited or e.code in (500, 502, 503, 504)) or attempt == 3:
                raise RuntimeError(f'HTTP {e.code} from {url.split("?")[0]}: {body.strip()}') from None
            wait = 2 ** attempt
            if retry_after and retry_after.isdigit():
                wait = int(retry_after)
            elif reset and reset.isdigit():
                wait = int(reset) - int(time.time()) + 1
            time.sleep(min(max(wait, 1), 90))
            continue
        except urllib.error.URLError:
            if attempt == 3:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError('unreachable')



def fixture(name: str) -> bytes | None:
    if not FIXTURES:
        return None
    return (pathlib.Path(FIXTURES) / name).read_bytes()


def get_json(url: str, fixture_name: str):
    raw = fixture(fixture_name)
    return json.loads(raw if raw is not None else fetch(url))



# The claw M from the Mahimai logo: three shapes in a 306 x 258 box.

# --- Brand banner ---------------------------------------------------------------------------

CLAW_M = ('<path d="M 0 1 L 153 113 L 306 0 L 306 33 L 174 133 L 227 106 L 306 53 L 306 78 L 254 117 L 250 106 '
          'L 153 180 L 55 104 L 54 215 L 0 257 Z"/><path d="M 252 174 L 306 141 L 306 227 L 253 258 Z"/>'
          '<path d="M 208 170 L 306 97 L 306 121 Z"/>')

def banner_svg() -> str:
    """The brand header, after the Mahimai banner: the claw M, the line, and a signal that runs
    CAPTURE, UNDERSTAND, RESPOND, DELIVER into the panther. One dark card in both themes."""
    t = THEMES['dark']
    panther = base64.b64encode((BRAND / 'panther.jpg').read_bytes()).decode()
    y, x0, x1, cycle = 300, 40, 822, 6.0
    stages = [('CAPTURE', 196, 'circle'), ('UNDERSTAND', 384, 'square'), ('RESPOND', 572, 'triangle'), ('DELIVER', 744, 'dot')]

    def shape(kind: str, x: int) -> str:
        if kind == 'circle':
            return f'<circle cx="{x}" cy="{y}" r="8"/>'
        if kind == 'square':
            return f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16"/>'
        if kind == 'triangle':
            return f'<path d="M {x} {y - 9} L {x + 9} {y + 7} L {x - 9} {y + 7} Z"/>'
        return f'<circle class="solid" cx="{x}" cy="{y}" r="5"/>'

    # Each stage flashes as the pulse reaches it.
    nodes = ''.join(
        f'<g class="node" style="animation-delay:{(x - x0) / (x1 - x0) * cycle:.2f}s">{shape(kind, x)}</g>'
        f'<text class="stage" x="{x}" y="{y - 30}" text-anchor="middle">{label}</text>'
        for label, x, kind in stages)
    # A short burst of speech before CAPTURE: a sine under a bell-shaped envelope.
    pts = ' '.join(f'{70 + i * 1.8:.1f},{y - 24 * math.sin(i * 0.9) * math.exp(-((i - 30) / 16) ** 2):.1f}'
                   for i in range(66))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-label="Mahimai: build voice products that keep working. From prototype to production.">
<defs>
  <clipPath id="card"><rect width="1200" height="400" rx="20"/></clipPath>
  <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.28" stop-color="#fff"/></linearGradient>
  <mask id="soft"><rect x="780" y="0" width="420" height="400" fill="url(#fade)"/></mask>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{t['accent']}" stop-opacity="0.9"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  .eyebrow {{ font: 500 15px {MONO}; fill: {t['muted']}; letter-spacing: 1.5px; }}
  .h1 {{ font: 700 50px {SANS}; fill: {t['ink']}; letter-spacing: -1px; }}
  .sub {{ font: 400 24px {SANS}; fill: #8a8a8a; }}
  .stage {{ font: 500 13px {MONO}; fill: {t['muted']}; letter-spacing: 1px; }}
  .grid {{ stroke: #1c1c1c; fill: none; }}
  .wire {{ stroke: {t['accent']}; stroke-width: 1.6; fill: none; opacity: 0.8; }}
  .speech {{ stroke: {t['accent']}; stroke-width: 1.8; fill: none; }}
  .node {{ fill: {t['bg']}; stroke: #d4d4d4; stroke-width: 1.6; animation: hit {cycle}s linear infinite; }}
  .node .solid {{ fill: {t['accent']}; stroke: none; }}
  .pulse {{ animation: run {cycle}s linear infinite; }}
  @keyframes run {{ from {{ transform: translateX(0); }} to {{ transform: translateX({x1 - x0}px); }} }}
  @keyframes hit {{ 0% {{ stroke: {t['accent']}; }} 10% {{ stroke: #d4d4d4; }} 100% {{ stroke: #d4d4d4; }} }}
  @media (prefers-reduced-motion: reduce) {{ .pulse {{ display: none; }} .node {{ animation: none; }} }}
</style>
<g clip-path="url(#card)">
  <rect width="1200" height="400" fill="{t['bg']}"/>
  <circle class="grid" cx="20" cy="330" r="120"/><circle class="grid" cx="1080" cy="150" r="110"/>
  <line class="grid" x1="0" x2="1200" y1="{y + 70}" y2="{y + 70}"/><line class="grid" x1="960" x2="960" y1="0" y2="400"/>
  <image x="784" y="68" width="416" height="400" href="data:image/jpeg;base64,{panther}" xlink:href="data:image/jpeg;base64,{panther}" mask="url(#soft)"/>
  <g transform="translate(64 55) scale(0.078)" fill="{t['ink']}">{CLAW_M}</g>
  <text class="eyebrow" x="100" y="71">MAHIMAI · VOICE AI PRODUCT ENGINEERING</text>
  <text class="h1" x="64" y="140">Build voice products</text>
  <text class="h1" x="64" y="196">that keep working.</text>
  <text class="sub" x="64" y="236">From prototype to production.</text>
  <path class="wire" d="M {x0} {y} H {x1} C {x1 + 10} {y} {x1 + 14} {y - 4} {x1 + 22} {y - 6}"/>
  <polyline class="speech" points="{pts}"/>
  {nodes}
  <g class="pulse"><circle cx="{x0}" cy="{y}" r="16" fill="url(#glow)" opacity="0.6"/><circle cx="{x0}" cy="{y}" r="3.5" fill="#fafafa"/></g>
</g>
<rect x="0.5" y="0.5" width="1199" height="399" rx="20" fill="none" stroke="{t['line']}"/>
</svg>
'''




# --- Markdown helpers -----------------------------------------------------------------------



def replace_chunk(content: str, marker: str, chunk: str, inline: bool = False) -> str:
    pattern = re.compile(rf'<!-- {marker} starts -->.*?<!-- {marker} ends -->', re.DOTALL)
    if not pattern.search(content):
        raise KeyError(f'marker "{marker}" not found in profile/README.md')
    body = chunk if inline else f'\n{chunk}\n'
    return pattern.sub(lambda _: f'<!-- {marker} starts -->{body}<!-- {marker} ends -->', content)



def md_escape(text: str) -> str:
    # Only what would break a link or read as HTML; backticks stay, so code in a PR title renders.
    return re.sub(r'([\[\]<>*])', r'\\\1', text)



def short_date(iso: str) -> str:
    """'2026-09-23' -> 'Sep 2026': short and a steady width, so the lists stay aligned."""
    return datetime.strptime(iso[:10], '%Y-%m-%d').strftime('%b %Y') if iso else ''



def blog_posts(limit: int = 5) -> list[dict]:
    raw = fixture('feed.xml')
    root = ET.fromstring(raw if raw is not None else fetch(FEED_URL, accept='application/rss+xml'))
    posts = []
    for item in root.iter('item'):
        published = datetime.strptime(item.findtext('pubDate', '').strip(), '%a, %d %b %Y %H:%M:%S %Z')
        posts.append({'title': item.findtext('title', '').strip(), 'url': item.findtext('link', '').strip(),
                      'date': published.date().isoformat()})
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts[:limit]





# --- Sources ----------------------------------------------------------------------------------

def org_repos() -> dict[str, dict]:
    """Every public repository in the organization, by name, from one listing call."""
    repos: dict[str, dict] = {}
    for page in range(1, 6):
        url = f'https://api.github.com/orgs/{ORG}/repos?' + urllib.parse.urlencode(
            {'type': 'public', 'per_page': 100, 'page': page})
        batch = get_json(url, 'org_repos.json') if not FIXTURES or page == 1 else []
        for r in batch:
            repos[r['name']] = r
        if len(batch) < 100:
            break
    return repos


def pypi_latest(name: str) -> dict:
    d = get_json(f'https://pypi.org/pypi/{name}/json', f'pypi__{name}.json')
    version = d['info']['version']
    uploads = [f['upload_time_iso_8601'] for f in d['releases'].get(version, [])]
    return {'version': version, 'date': min(uploads)[:10] if uploads else ''}


def projects() -> dict[str, list[dict]]:
    """The listed projects by group, each with GitHub's live description and stars, and its
    latest PyPI release where it publishes one. A release that cannot be read is left blank."""
    repos = org_repos()
    out: dict[str, list[dict]] = {}
    for group, entries in GROUPS.items():
        rows = []
        for name, package in entries:
            r = repos.get(name)
            if not r or r.get('archived') or r.get('private'):
                continue
            release = None
            if package:
                try:
                    release = pypi_latest(package)
                except Exception as e:  # one package's outage should not drop the table
                    print(f'  {package}: PyPI unavailable ({e})')
            description = DESCRIPTIONS.get(name) or (r.get('description') or '').strip()
            rows.append({'name': name, 'url': r['html_url'], 'description': description,
                         'stars': r.get('stargazers_count', 0), 'pushed': r.get('pushed_at', ''),
                         'package': package, 'release': release, 'site': SITES.get(name)})
        out[group] = rows
    return out


def recently_merged(limit: int = 6) -> list[dict]:
    """The latest merged pull requests across the organization's public repositories, newest
    first, leaving out bots."""
    url = 'https://api.github.com/search/issues?' + urllib.parse.urlencode(
        {'q': f'org:{ORG} is:pr is:merged is:public', 'sort': 'updated', 'order': 'desc', 'per_page': 50})
    items = get_json(url, 'merged.json')['items']
    prs = []
    for it in items:
        user = it.get('user') or {}
        if user.get('type') == 'Bot' or user.get('login', '').endswith('[bot]'):
            continue
        merged = (it.get('pull_request') or {}).get('merged_at') or it['closed_at']
        prs.append({'repo': it['repository_url'].rsplit('/', 1)[-1], 'title': it['title'].strip(),
                    'url': it['html_url'], 'date': merged[:10], 'merged_at': merged, 'author': user.get('login', '')})
    prs.sort(key=lambda p: p['merged_at'], reverse=True)
    return prs[:limit]


# --- Rendering --------------------------------------------------------------------------------

def projects_md(rows: list[dict]) -> str:
    out = ['| Project | What it does | Latest | Stars |', '|---|---|---|---|']
    for p in rows:
        name = f'**[{p["name"]}]({p["url"]})**'
        if p['site']:
            name += f'<br><sub><a href="{p["site"]}">{p["site"].removeprefix("https://")}</a></sub>'
        if p['release']:
            latest = f'[{p["release"]["version"]}](https://pypi.org/project/{p["package"]}/)'
            if p['release']['date']:
                latest += f'<br><sub>{short_date(p["release"]["date"])}</sub>'
        else:
            latest = f'<sub>updated {short_date(p["pushed"])}</sub>' if p['pushed'] else ''
        description = md_escape(p['description']).replace('|', '\\|')
        out.append(f'| {name} | {description} | {latest} | ★ {p["stars"]:,} |')
    return '\n'.join(out)


def stats_md(groups: dict[str, list[dict]]) -> str:
    rows = [p for g in groups.values() for p in g]
    stars = sum(p['stars'] for p in rows)
    packages = sum(1 for p in rows if p['release'])
    # HTML, not Markdown: the line opens with a marker comment, which makes GitHub read it as HTML.
    return f'<b>{len(rows)}</b> open-source projects · <b>{stars:,}</b> stars · <b>{packages}</b> packages on PyPI'


def writing_md(posts: list[dict]) -> str:
    return '\n\n'.join(f'[{md_escape(p["title"])}]({p["url"]})<br><sub>{short_date(p["date"])}</sub>' for p in posts)


def merged_md(prs: list[dict]) -> str:
    def line(p):
        by = f' · @{p["author"]}' if p['author'] else ''
        return f'[{md_escape(p["title"])}]({p["url"]})<br><sub>{p["repo"]} · {short_date(p["date"])}{by}</sub>'
    return '\n\n'.join(line(p) for p in prs)


# --- Main -------------------------------------------------------------------------------------

def section(name: str, build):
    """Run one section; on failure, report it and keep what the README already has."""
    try:
        return build()
    except Exception as e:
        print(f'! {name}: {type(e).__name__}: {e} (keeping the previous content)', file=sys.stderr)
        return None


def main() -> None:
    readme = README.read_text()
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / 'banner.svg').write_text(banner_svg())

    groups = section('projects', projects)
    posts = section('writing', blog_posts)
    prs = section('merged', recently_merged)

    # None means the source failed and the section keeps what it had; an empty list is a real
    # answer and replaces stale content.
    if groups is not None:
        for group, rows in groups.items():
            readme = replace_chunk(readme, f'projects_{group}', projects_md(rows))
        readme = replace_chunk(readme, 'stats', stats_md(groups), inline=True)
    if posts is not None:
        readme = replace_chunk(readme, 'writing', writing_md(posts))
    if prs is not None:
        readme = replace_chunk(readme, 'merged', merged_md(prs))

    README.write_text(readme)
    print('Updated:', ', '.join(n for n, v in [('projects', groups), ('writing', posts), ('merged', prs)]
                                if v is not None) or 'nothing')


if __name__ == '__main__':
    main()
