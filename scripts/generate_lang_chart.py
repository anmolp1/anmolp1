#!/usr/bin/env python3
"""Fetch language stats from all GitHub repos and generate an SVG bar chart."""

import json
import os
import urllib.request
import urllib.error

USERNAME = "anmolp1"
TOKEN = os.environ.get("GH_TOKEN", "")

# Language colors (matches GitHub's language colors)
LANG_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B",
    "Java": "#b07219",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "R": "#198CE7",
    "Scala": "#c22d40",
    "Lua": "#000080",
    "SQL": "#e38c00",
    "PLSQL": "#dad8d8",
    "HCL": "#844FBA",
    "Dockerfile": "#384d54",
    "Makefile": "#427819",
    "Svelte": "#ff3e00",
    "Vue": "#41b883",
    "SCSS": "#c6538c",
    "Sass": "#a53b70",
    "Less": "#1d365d",
    "Nix": "#7e7eff",
    "Zig": "#ec915c",
    "Elixir": "#6e4a7e",
    "Haskell": "#5e5086",
    "OCaml": "#3be133",
    "Perl": "#0298c3",
    "PowerShell": "#012456",
    "Batchfile": "#C1F12E",
    "MATLAB": "#e16737",
    "Jinja": "#a52a22",
    "Smarty": "#f0c040",
    "Mako": "#7e858d",
    "EJS": "#a91e50",
    "MDX": "#fcb32c",
    "Astro": "#ff5a03",
}
DEFAULT_COLOR = "#8b8b8b"

# Approximate bytes-per-line by language for a rough LOC estimate
BYTES_PER_LINE = {
    "Python": 30,
    "JavaScript": 28,
    "TypeScript": 30,
    "HTML": 45,
    "CSS": 25,
    "SCSS": 25,
    "Shell": 25,
    "Jupyter Notebook": 50,
    "Java": 32,
    "C": 28,
    "C++": 30,
    "C#": 32,
    "Go": 28,
    "Rust": 30,
    "Ruby": 25,
    "PHP": 30,
    "SQL": 35,
    "Svelte": 35,
    "Vue": 35,
    "Dockerfile": 30,
    "Makefile": 25,
    "R": 30,
    "Dart": 30,
    "Kotlin": 30,
    "Swift": 30,
    "HCL": 28,
}
DEFAULT_BPL = 30


def gh_api(path, accept=None):
    """Make a GitHub API request."""
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", accept or "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def find_contributed_repos():
    """Find all repos the user has committed to via the commit search API."""
    repo_names = set()
    page = 1
    # The search API returns max 1000 results; we just need unique repos
    while page <= 10:
        try:
            data = gh_api(
                f"/search/commits?q=author:{USERNAME}&per_page=100&page={page}&sort=author-date&order=desc",
                accept="application/vnd.github.cloak-preview+json",
            )
        except urllib.error.HTTPError as e:
            print(f"  Search API error on page {page}: {e.code}")
            break
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            repo = item.get("repository", {}).get("full_name")
            if repo:
                repo_names.add(repo)
        print(f"  Search page {page}: found {len(items)} commits, {len(repo_names)} unique repos so far")
        if len(items) < 100:
            break
        page += 1
    return repo_names


def fetch_owned_repos():
    """Fetch all repos owned by the user (paginated)."""
    repo_names = set()
    page = 1
    while True:
        data = gh_api(f"/users/{USERNAME}/repos?per_page=100&page={page}")
        if not data:
            break
        for repo in data:
            repo_names.add(repo["full_name"])
        if len(data) < 100:
            break
        page += 1
    return repo_names


def fetch_language_stats():
    """Aggregate language bytes across all repos the user has contributed to."""
    print("  Finding repos via commit search...")
    contributed = find_contributed_repos()
    print("  Finding owned repos...")
    owned = fetch_owned_repos()
    all_repos = contributed | owned
    print(f"  Total unique repos to scan: {len(all_repos)}")

    totals = {}
    for name in sorted(all_repos):
        try:
            langs = gh_api(f"/repos/{name}/languages")
        except urllib.error.HTTPError:
            print(f"  Skipping {name} (no access)")
            continue
        if langs:
            print(f"  {name}: {', '.join(langs.keys())}")
        for lang, bytes_count in langs.items():
            totals[lang] = totals.get(lang, 0) + bytes_count
    return totals


def bytes_to_lines(lang, byte_count):
    """Rough estimate of lines of code from bytes."""
    bpl = BYTES_PER_LINE.get(lang, DEFAULT_BPL)
    return byte_count // bpl


def format_number(n):
    """Format number with K/M suffix."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def generate_svg(lang_lines, output_path):
    """Generate a horizontal bar chart SVG."""
    # Sort by lines descending, take top 15
    sorted_langs = sorted(lang_lines.items(), key=lambda x: x[1], reverse=True)[:15]

    if not sorted_langs:
        return

    max_lines = sorted_langs[0][1]

    # Dimensions
    bar_height = 28
    bar_gap = 8
    label_width = 150
    value_width = 60
    chart_width = 400
    padding = 20
    total_width = label_width + chart_width + value_width + padding * 2
    header_height = 40
    total_height = header_height + len(sorted_langs) * (bar_height + bar_gap) + padding * 2

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}">')

    # Background with rounded corners
    lines.append(f'  <rect width="{total_width}" height="{total_height}" rx="12" fill="#0d1117" />')
    lines.append(f'  <rect x="1" y="1" width="{total_width - 2}" height="{total_height - 2}" rx="11" fill="none" stroke="#30363d" stroke-width="1" />')

    # Title
    lines.append(f'  <text x="{total_width / 2}" y="{padding + 14}" fill="#e6edf3" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" font-weight="600" text-anchor="middle">Lines of Code by Language</text>')

    y_start = header_height + padding

    for i, (lang, loc) in enumerate(sorted_langs):
        y = y_start + i * (bar_height + bar_gap)
        bar_w = max((loc / max_lines) * chart_width, 2)
        color = LANG_COLORS.get(lang, DEFAULT_COLOR)
        loc_str = format_number(loc)

        # Language label
        lines.append(f'  <text x="{padding + label_width - 10}" y="{y + bar_height / 2 + 5}" fill="#e6edf3" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" text-anchor="end">{lang}</text>')

        # Bar background
        lines.append(f'  <rect x="{padding + label_width}" y="{y}" width="{chart_width}" height="{bar_height}" rx="6" fill="#161b22" />')

        # Bar fill with animation
        lines.append(f'  <rect x="{padding + label_width}" y="{y}" width="{bar_w:.1f}" height="{bar_height}" rx="6" fill="{color}" opacity="0.85">')
        lines.append(f'    <animate attributeName="width" from="0" to="{bar_w:.1f}" dur="0.6s" fill="freeze" begin="{i * 0.05:.2f}s" />')
        lines.append(f'  </rect>')

        # Value label
        lines.append(f'  <text x="{padding + label_width + chart_width + 10}" y="{y + bar_height / 2 + 5}" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="11">{loc_str}</text>')

    lines.append('</svg>')

    svg_content = "\n".join(lines)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(svg_content)
    print(f"Generated {output_path} with {len(sorted_langs)} languages")


def main():
    print(f"Fetching repos for {USERNAME}...")
    lang_bytes = fetch_language_stats()
    print(f"Found {len(lang_bytes)} languages across repos")

    lang_lines = {}
    for lang, byte_count in lang_bytes.items():
        loc = bytes_to_lines(lang, byte_count)
        if loc > 0:
            lang_lines[lang] = loc

    output = os.path.join(os.path.dirname(__file__), "..", "dist", "lang-chart.svg")
    output = os.path.normpath(output)
    generate_svg(lang_lines, output)


if __name__ == "__main__":
    main()
