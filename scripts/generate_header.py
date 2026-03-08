"""Generate the terminal header SVG with pixel-art ANMOL text."""

# Each letter defined as a grid of 1s on a 5-col x 7-row matrix
LETTERS = {
    "A": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    "N": [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    "M": [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    "O": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    "L": [
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
}

CELL = 10  # px per cell
GAP = 2    # px gap between cells
LETTER_GAP = 18  # px between letters
WORD = "ANMOL"

SVG_W = 800
SVG_H = 380

# Calculate total width of the word
letter_w = 5 * (CELL + GAP) - GAP
total_w = len(WORD) * letter_w + (len(WORD) - 1) * LETTER_GAP
start_x = (SVG_W - total_w) // 2
start_y = 52

rects = []
for li, ch in enumerate(WORD):
    grid = LETTERS[ch]
    ox = start_x + li * (letter_w + LETTER_GAP)
    for row_i, row in enumerate(grid):
        for col_i, val in enumerate(row):
            if val:
                x = ox + col_i * (CELL + GAP)
                y = start_y + row_i * (CELL + GAP)
                rects.append(f'    <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="1"/>')

pixel_art = "\n".join(rects)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Terminal window -->
  <rect width="{SVG_W}" height="{SVG_H}" rx="10" fill="#0a0a0a"/>

  <!-- Title bar -->
  <rect width="{SVG_W}" height="34" rx="10" fill="#1a1a1a"/>
  <rect y="22" width="{SVG_W}" height="12" fill="#1a1a1a"/>

  <!-- Traffic lights -->
  <circle cx="22" cy="17" r="7" fill="#ff5f57"/>
  <circle cx="44" cy="17" r="7" fill="#febc2e"/>
  <circle cx="66" cy="17" r="7" fill="#28c840"/>

  <!-- Title bar text -->
  <text x="400" y="22" text-anchor="middle" font-family="\'SF Mono\', \'Fira Code\', \'Courier New\', monospace" font-size="12" fill="#555">anmol@mldeep: ~</text>

  <!-- ANMOL pixel art -->
  <g filter="url(#glow)" fill="#00ff41">
{pixel_art}
  </g>

  <!-- Divider -->
  <line x1="40" y1="145" x2="760" y2="145" stroke="#00ff41" stroke-opacity="0.25" stroke-width="1"/>

  <!-- Tagline -->
  <g fill="#00ff41" font-family="\'SF Mono\', \'Fira Code\', \'Courier New\', monospace" font-size="16" opacity="0.85">
    <text x="400" y="178" text-anchor="middle">founder @ mldeep systems</text>
    <text x="400" y="204" text-anchor="middle">ai agent reliability engineering</text>
  </g>

  <!-- Divider 2 -->
  <line x1="40" y1="225" x2="760" y2="225" stroke="#00ff41" stroke-opacity="0.12" stroke-width="1"/>

  <!-- Terminal lines -->
  <g font-family="\'SF Mono\', \'Fira Code\', \'Courier New\', monospace" font-size="13" fill="#00ff41">
    <text x="40" y="258" opacity="0.55">anmol@mldeep:~$</text>
    <text x="200" y="258" opacity="0.9">I diagnose why AI agents break in production</text>

    <text x="40" y="288" opacity="0.55">anmol@mldeep:~$</text>
    <text x="200" y="288" opacity="0.9">7 failure modes. most agents hit at least 3.</text>

    <text x="40" y="318" opacity="0.55">anmol@mldeep:~$</text>
    <text x="200" y="318" opacity="0.9">cat /etc/status</text>
    <text x="40" y="340" opacity="0.65">building in public | open to collabs | shipping daily</text>

    <text x="40" y="365" opacity="0.45">anmol@mldeep:~$</text>
  </g>

  <!-- Blinking cursor -->
  <rect x="200" y="353" width="9" height="16" fill="#00ff41">
    <animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>

  <!-- Border glow -->
  <rect width="{SVG_W}" height="{SVG_H}" rx="10" fill="none" stroke="#00ff41" stroke-opacity="0.08" stroke-width="1"/>
</svg>'''

out = "dist/terminal-header.svg"
with open(out, "w") as f:
    f.write(svg)
print(f"Generated {out} ({len(svg)} bytes)")
