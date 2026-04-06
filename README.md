# PPA Attestation Visualizer

[![Bounty](https://img.shields.io/badge/bounty-RustChain%20%232148-blue)](https://github.com/Scottcjn/Rustchain/issues/2148)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> 🎯 **Bounty Project**: Visual Hardware Identity Cards for RustChain PPA Fingerprints

Transform raw PPA (Physical Presence Attestation) fingerprint data into beautiful, informative visual hardware identity cards. Perfect for fleet management, hardware verification, and attestation reporting.

![Demo](demo-screenshot.png)

## ✨ Features

- **📡 Radar Chart** — Spider chart visualization of all 7 PPA channel scores
- **〰️ Oscilloscope Waveform** — Clock drift data as a real-time style waveform
- **🔥 Cache Latency Heatmap** — 4x4 color-coded heatmap (blue=cold to red=hot)
- **⭐ Jitter Constellation** — Star map of instruction jitter patterns
- **🎨 Architecture-Aware** — Visually distinct for x86, ARM, PowerPC, etc.
- **📱 SVG Output** — Scalable vector graphics for crisp rendering at any size
- **🚀 Zero Dependencies** — Uses only Python standard library

## 🚀 Quick Start

### CLI Usage

```bash
# Generate hardware identity card from fingerprint JSON
python3 ppa_visualizer.py sample-fingerprint.json output.svg

# View the generated SVG
open output.svg  # macOS
xdg-open output.svg  # Linux
```

### Python API

```python
from ppa_visualizer import PPAVisualizer
import json

# Load fingerprint data
with open('fingerprint.json') as f:
    data = json.load(f)

# Generate visualization
viz = PPAVisualizer(data)
svg_output = viz.generate_svg()

# Save to file
with open('identity.svg', 'w') as f:
    f.write(svg_output)
```

## 📊 Input Format

The visualizer expects JSON output from `fingerprint_checks.py`:

```json
{
  "timestamp": "2026-04-06T18:30:00Z",
  "hardware_id": "g4_mac_mini_1.42ghz",
  "architecture": "PowerPC G4",
  "channels": {
    "clock_drift": {
      "score": 0.87,
      "waveform": [0.82, 0.85, 0.87, 0.89, 0.86, 0.84, 0.88, 0.87, 0.85, 0.86]
    },
    "cache_timing": {
      "score": 0.92,
      "heatmap": [[45, 42, 48, 44], [46, 43, 47, 45], [44, 46, 45, 43], [47, 44, 46, 45]]
    },
    "simd_identity": { "score": 0.78 },
    "thermal_drift": { "score": 0.65 },
    "instruction_jitter": {
      "score": 0.71,
      "constellation": [{"x": 0.72, "y": 0.69}, {"x": 0.71, "y": 0.73}, ...]
    },
    "anti_emulation": { "score": 0.95 },
    "fleet_detection": { "score": 0.88 }
  },
  "overall_score": 0.82,
  "ppa_compliant": true
}
```

## 🎨 Visual Elements

### Hardware Identity Card Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    PPA HARDWARE IDENTITY                     │
│                      PowerPC G4                              │
│                   g4_mac_mini_1.42ghz                        │
│                                                             │
│    ┌─────────┐         ┌──────────────────────┐            │
│    │  Radar  │         │   Clock Drift        │     82%    │
│    │  Chart  │         │   Waveform           │   [score]  │
│    │         │         │                      │            │
│    └─────────┘         └──────────────────────┘            │
│                                                             │
│    ┌─────────┐         ┌──────────────────────┐            │
│    │  Jitter │         │   Cache Heatmap      │            │
│    │  Star   │         │   [blue → red]       │            │
│    │  Map    │         │                      │            │
│    └─────────┘         └──────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Color Coding

- **Score Badge**: 🟢 Green (≥80%), 🟡 Yellow (60-79%), 🔴 Red (<60%)
- **Heatmap**: 🔵 Blue (low latency) → 🔴 Red (high latency)
- **Constellation**: ⭐ Gold stars with connecting lines

## 📁 Files

| File | Description |
|------|-------------|
| `ppa_visualizer.py` | Main visualizer module (pure Python) |
| `sample-fingerprint.json` | Example PowerPC G4 fingerprint data |
| `hardware_identity.svg` | Sample generated output |
| `demo.html` | Interactive demo page |
| `README.md` | This file |

## 🎯 Bounty Details

- **Issue**: [RustChain #2148](https://github.com/Scottcjn/Rustchain/issues/2148)
- **Reward**: 75 RTC
- **Status**: ✅ Complete

### Requirements Met

- [x] Radar/spider chart of all 7 channel scores
- [x] Oscilloscope waveform for clock drift
- [x] Heatmap for cache latency profiles
- [x] Jitter constellation (star map of instruction jitter)
- [x] Combined badge — visual hash like GitHub identicons
- [x] Input: JSON from fingerprint_checks.py
- [x] Output: SVG (scalable, web-friendly)
- [x] Visually distinct for different architectures
- [x] Pure Python implementation

## 🛠️ Development

```bash
# Clone the repo
git clone https://github.com/rmartinppa/ppa-attestation-visualizer.git
cd ppa-attestation-visualizer

# Run tests with sample data
python3 ppa_visualizer.py sample-fingerprint.json test-output.svg

# View demo page
open demo.html
```

## 📄 License

MIT License — see LICENSE file for details.

## 🤝 Contributing

This project was built for the RustChain ecosystem. Contributions welcome!

## 🔗 Links

- [Live Demo](https://rmartinppa.github.io/ppa-attestation-visualizer/demo.html)
- [Bounty Issue](https://github.com/Scottcjn/Rustchain/issues/2148)
- [RustChain Project](https://github.com/Scottcjn/Rustchain)

---

Built with 💙 for the RustChain ecosystem
