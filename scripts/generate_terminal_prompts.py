"""Generate matrix-green terminal prompt SVGs for README sections."""

import os

PROMPTS = {
    "prompt-whoami": "whoami",
    "prompt-cat-mission": "cat mission.txt",
    "prompt-ls-projects": "ls -la projects/",
    "prompt-cat-stack": "cat /etc/stack.conf",
    "prompt-wc": "wc -l **/*.{py,js,ts,sql,sh} | sort -rn | head",
    "prompt-git-snake": "git log --graph --oneline --all | snake",
    "prompt-ssh-config": "cat ~/.ssh/config",
    "prompt-exit": "exit",
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="32" viewBox="0 0 {width} 32">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="0.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="{width}" height="32" rx="4" fill="#0a0a0a"/>
  <g filter="url(#glow)">
    <text x="12" y="21" font-family="'JetBrains Mono', 'SF Mono', 'Fira Code', monospace" font-size="14" fill="#00ff41" opacity="0.7">anmol@mldeep:~$</text>
    <text x="190" y="21" font-family="'JetBrains Mono', 'SF Mono', 'Fira Code', monospace" font-size="14" fill="#00ff41">{cmd}</text>
  </g>
  <rect x="{cursor_x}" y="8" width="8" height="16" fill="#00ff41" opacity="0.8">
    <animate attributeName="opacity" values="0.8;0;0.8" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>"""

dist_dir = os.path.join(os.path.dirname(__file__), "..", "dist")

for filename, cmd in PROMPTS.items():
    char_width = 9.2
    prompt_len = len("anmol@mldeep:~$ ") + len(cmd)
    width = max(int(prompt_len * char_width) + 50, 300)
    cursor_x = 190 + int(len(cmd) * char_width) + 8
    svg = TEMPLATE.format(width=width, cmd=cmd, cursor_x=cursor_x)
    path = os.path.join(dist_dir, f"{filename}.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"Generated {path}")
