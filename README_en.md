# Generating Slides v2 — Projection-Grade HTML Deck Generator

[简体中文](README.md) ｜ **English**

> A skill package for Claude Code. It generates a **1920×1080 single-file HTML deck** under three hard layout constraints — *fill ratio → type scale → visual order* — plus a focal-emphasis judgment layer, with built-in editing / annotation / presenter interactions, an animation library, and two PDF export paths. Nothing ships until it passes mechanical verification.
>
> **The executable rules live in [SKILL.md](SKILL.md).** This file is installation and overview only — deliberately so, to keep the two from drifting apart.
>
> **Provenance:** this is a derivative work of Zara Zhang's [Frontend Slides](https://github.com/zarazhangrui/frontend-slides) (MIT License), not an original work. The layout chassis and workflow are original to this package. Distributed under MIT; upstream notices are in [LICENSE](LICENSE) and in the *Sources & License* section at the end of [SKILL.md](SKILL.md).

## What it does

Say "make me a deck about X" and the skill walks a **seven-stage** flow: read the project `CLAUDE.md` (skip if absent) → configure → prepare material → optimize content (silent) → outline → choose style → generate (with an inline verification pass) → deliver. **Every stage confirmation is a hard stop** — the skill waits for an answer rather than assuming one.

The output is one HTML file with all CSS and JS inlined. No CDN, no build tool, no dependencies. Double-click to present: it scales proportionally from a 1920×1080 stage, so it never distorts on any screen.

It accepts three entry modes: generate from scratch, restructure an existing `.docx` / `.pptx`, or surgically edit a named page.

## Core conventions (the v2 paradigm)

| Layer | Governs | Hard limits |
|---|---|---|
| Chassis · fill ratio | Does the page hold the canvas? | Dense layout ≥60% area and ≥80% width / two-column ≥45% / single-focus hero block ≥60% of the text column |
| Reading · type scale | Once it holds, can it be read? | Body floor 22px (1/50 of screen height) / assertion-style headings locked at 84px / ceremonial positions 110–140px |
| Order · grouping, alignment, spacing | Once readable, is it tidy? | Three spacing tiers that follow the hierarchy tree / container ladder card > rule > whitespace / one left axis per page |
| Focus · emphasis judgment | Emphasize what, how, and how much | Focus serves the argument / visual weight is conserved (no padding blocks under a hero) / a scarcity quota for color / prefer isomorphic cards |

- **One chassis, assembled:** `assets/chassis-v2.html` is the only chassis and is a **build artifact — never hand-edit it**. Sources live in `assets/chassis/` (frozen) plus `assets/modules/` (feature pieces). Rebuild with `node scripts/build-chassis.mjs`.
- **Density tiers decided up front:** low ≤40 / medium 40–120 / high 120–200 / over >200 → cut copy and cut pages. Cut, never compress.
- **Slot decision tree:** content logic determines the slot; slots are never invented on the fly.
- **Automatic animation routing:** content emphasis × mood → a preset package. Restrained by default; the user is not interrogated per animation.

## Install

Install into Claude Code's skills directory. **The directory must be named `generating-slides`**, matching `name` in SKILL.md.

Clone straight into place:

```bash
git clone https://github.com/whq217/generating-slides.git ~/.claude/skills/generating-slides
```

Update later with a pull:

```bash
git -C ~/.claude/skills/generating-slides pull
```

Windows PowerShell:

```powershell
git clone https://github.com/whq217/generating-slides.git "$env:USERPROFILE\.claude\skills\generating-slides"
```

A ZIP download works too — just make sure the extracted folder is renamed to `generating-slides`:

```bash
cp -r generating-slides ~/.claude/skills/generating-slides
```

> **Do not let your editor convert line endings.** `samples/patches.json` stores byte-exact SHA-256 hashes for the verification fixtures. A CRLF conversion will make `verify-all` fail wholesale. `.gitattributes` pins everything to LF; keep it.

## Keyboard controls (built into the chassis)

| Key | Action |
|---|---|
| → / ↓ / PageDown / Space / click right half | Next slide |
| ← / ↑ / PageUp / click left half | Previous slide |
| **E** | Edit mode (exit with Done — downloads the edited HTML, which becomes the file) |
| **D** | Pen (right-click clears, advances clear automatically) |
| **S** | Presenter mode (separate window, synced across displays, notes card for prompting) |
| **P** | Print / PDF (print CSS locks 16:9, one slide per page) |

PDF is a second delivery path: the skill asks whether a PDF is wanted, then `chrome --headless --print-to-pdf` produces one with zero dependencies.

## Repository layout

```
generating-slides/
├── SKILL.md                    # Main file: paradigm, seven stages, slot tree, file map
├── README.md / README_en.md    # Installation and overview (zh / en)
├── references/                 # 17 method files, read on trigger per stage or page type
│   ├── layout-rules-v2.md      # Full three-layer rules (required before generation)
│   ├── focus-judgment.md       # Focal emphasis judgment layer
│   ├── presets-index.md        # Index of 22 presets + 2×2 pool routing
│   ├── style-presets.md        # Full specs for all 22 presets
│   ├── decoration-vocab.md     # Decoration vocabulary: two iron rules, entries, pitfalls
│   ├── content-preparation.md  # Material extraction: docx/pptx commands, encoding traps
│   ├── content-optimization.md # Content optimization principles
│   ├── title-copy-types.md     # Title copy typing and size adjudication
│   ├── number-typography.md    # Number typography R1–R6
│   ├── chart-recipes.md        # Six chart families: hand-written SVG first, ECharts inline
│   ├── diagram-patterns.md     # Nine structural diagram recipes (G-01…G-09)
│   ├── animation-routing.md    # Type × mood → animation package, three-layer convergence
│   ├── anim-recipes.md         # Code-animation gates, quotas, five recipes
│   ├── image-handling.md       # Images only ever go on the cover
│   ├── speaker-mode.md         # Presenter window behavior
│   ├── iterative-edit.md       # Iterative revision: back up → surgical edit → regression
│   └── offline-export.md       # PDF and offline
├── assets/
│   ├── chassis-v2.html         # The one chassis (build artifact, never hand-edit)
│   ├── chassis/                # Frozen sources: core.css / core.js / template.html
│   ├── modules/                # Feature pieces: interactions / print / effects / anim-runtime
│   └── diagram-gallery.html    # Runnable reference for the nine recipes
├── scripts/
│   ├── build-chassis.mjs       # Rebuild chassis-v2.html after touching sources
│   ├── measure-layout.js       # Fill-ratio and under-fill probe (headless Chrome, no npm)
│   ├── crowd-probe.py          # Crowding probe: dead gaps, overlaps, bad line height (playwright; SKIP if absent)
│   ├── check-deck.py           # Four output assertions: hero-num units, SVG tinting, text overflow, type scale
│   ├── verify-consistency.py   # Static consistency check (pure Python)
│   ├── verify-all.py           # The single gate: build parity + fixture gate + zero legacy terms
│   └── extract-pptx.py         # .pptx extraction (needs python-pptx)
├── samples/
│   ├── good/chassis.html       # Positive fixture (must be green on both checkers) + patch base
│   ├── patches.json            # Line-level patches for 25 negative fixtures, with per-file SHA-256
│   ├── build_samples.py        # Materializes negatives into a temp dir, self-verifying by hash
│   ├── gen_patches.py          # Recompute patches.json after changing the base or a fixture
│   ├── _base/                  # Standalone fixtures that cannot derive from the base
│   └── expected.json           # Expected exit code and keywords per fixture
├── LICENSE                     # MIT text + upstream and third-party notices
├── .gitattributes              # LF pinned — the verification chain depends on it
└── .gitignore
```

## Verification

Generating is not delivering — the scripts have to pass first. When a limit is missed, only whitelisted remedies are allowed: switch to a vertical layout, raise the type size, use a lighter container, merge or cut pages. **Never add filler to inflate the fill ratio.**

| Script | What it checks | Depends on |
|---|---|---|
| `measure-layout.js` | Fill-ratio measurement plus under-fill bands, with animation-defeating probes forced visible and marginal notes excluded | Local Chrome |
| `verify-consistency.py` | Static consistency, single-report mode. **[Severe]** (exit 1 = reject signal) covers skeleton integrity, orphan component classes (baseline auto-extracted from the chassis CSS registry), excessive emphasis containers, missing highlight cards, inline sizes below 11.5px, too many gap values, glow color bugs, dangling size variables, cover size overrides, chart and diagram conformance, and parser self-evidence (quotes handled both ways; a zero base reports a parse anomaly). **[Hint]** covers hardcoded colors, accent tone, single-column stacking, and node-count limits — no exit-code impact | Pure Python |
| `crowd-probe.py` | Dead gaps within groups, text overlap, abnormal line height | playwright (SKIP if absent) |
| `check-deck.py` | Four output assertions: hero-number unit tinting, SVG tinting, text y-overflow, type scale (interval plus floor) | Pure Python |
| `verify-all.py` | The single gate: byte-exact build parity, all positive fixtures green, every negative fixture compared against `expected.json` (negatives materialized from `patches.json` and hash-verified, single-quote variants included), zero legacy terminology | Pure Python (node for the build step; SKIP if absent) |

**On playwright:** it is optional. The package does not need it to generate or deliver a deck — without it, the crowding probe simply prints `[SKIP]` and exits 0. Install it only if you want that extra check: `pip install playwright`.

## Relation to v1

v1 (Reveal.js, 1200×700 stage, 19 themes, 30 layouts) was retired from this package on 2026-10-20. It is no longer distributed, but it is not lost:

> **GitHub archive:** the complete v1 source is preserved in the tag [v1.0-revealjs](https://github.com/whq217/generating-slides/tree/v1.0-revealjs).
> Retrieve it with `git checkout v1.0-revealjs`. The `master` branch carries v2 only.
> The two are incompatible: v1 depends on Reveal.js, uses six stages, and is named `slides`; v2 has zero dependencies, uses seven stages, and is named `generating-slides`.

## Changelog

- **2026-10-24 (v1.1.1)** — ① **Maintenance history removed from the runtime prompt.** 17 inline annotations in SKILL.md (dated decisions such as "established on…", "signed off on…", "removed on…") were stripped down to their behavioral rationale, with the dated record moved into this README. History is for humans; it should not occupy agent context. ② **Attribution restored.** The MIT credit for *女娲·Skill造人术 (nuwa-skill)* referenced at stage 3 was present in 1.0.0 and lost in 1.1.0; it is back in both SKILL.md and this README. Attribution does not regress. ③ **Fixtures converted to patches.** The 25 negative fixtures were previously full 1089-line copies of the chassis with a single defect injected each. They are now derived on demand from the base plus `patches.json`, hash-verified per file; the package shrank roughly 70%. Verified with `verify-all` 54/54.
- **2026-10-24** — BroadcastChannel echo loop fixed: with the same deck open in multiple tabs, one side advancing would broadcast, the other would follow and re-broadcast, and both would livelock. Fixed by splitting `go` / `__goto` so received broadcasts jump without rebroadcasting.
- **2026-10-24** — Pen panel (`N`) removed. The main window is what the audience sees, so a prompting panel is visible to them; prompting now belongs to the presenter window's notes card. Interactions are E / D / S.
- **2026-10-24** — `crowd-probe.py` now degrades gracefully: prints `[SKIP]` and exits 0 when playwright is missing, instead of crashing.

## Acknowledgements

Built on [Frontend Slides](https://github.com/zarazhangrui/frontend-slides) by @zarazhangrui (MIT). The v2 paradigm was restructured by Hongqing W. Stage 3 content optimization references the Steve Jobs perspective skill from [女娲·Skill造人术 (nuwa-skill)](https://github.com/alchaincyf/nuwa-skill) (MIT).

## License

MIT. The binding text is in [LICENSE](LICENSE), which carries the upstream Frontend Slides notice and the third-party nuwa-skill notice; the in-document statement is in the *Sources & License* section at the end of [SKILL.md](SKILL.md).

---

Maintained and published by 庆哥聊AI. Free to use.
