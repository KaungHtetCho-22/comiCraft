<div align="center">

<br/>

```
  ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗██████╗  █████╗ ███████╗████████╗
 ██╔════╝██╔═══██╗████╗ ████║██║██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
 ██║     ██║   ██║██╔████╔██║██║██║     ██████╔╝███████║█████╗     ██║
 ██║     ██║   ██║██║╚██╔╝██║██║██║     ██╔══██╗██╔══██║██╔══╝     ██║
 ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╗██║  ██║██║  ██║██║        ██║
  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝
```

### Turn your imagination into panels. One prompt at a time.

<br/>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Powered_by-Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

[**Features**](#-features) &nbsp;·&nbsp;
[**Quick Start**](#-quick-start) &nbsp;·&nbsp;
[**How to Use**](#%EF%B8%8F-how-to-use) &nbsp;·&nbsp;
[**My Studio**](#-my-studio--the-consistency-engine) &nbsp;·&nbsp;
[**Architecture**](#-architecture)

<br/>

<video src="assets/demo.mp4" controls autoplay loop muted width="100%">
  <a href="assets/demo.mp4">Watch the demo</a>
</video>

</div>

<br/>

---

## What is comiCraft?

**comiCraft** is a browser-based creative tool that transforms text prompts into fully-rendered, multi-page comic storyboards — powered by Google Gemini's multimodal AI.

Designed for writers, artists, and storytellers who want to **visualize ideas fast** without sacrificing consistency across pages.

> **The core problem with AI comic generation:** Characters look completely different by page 3.
> **comiCraft's answer:** My Studio — a consistency engine that locks character and environment references into every generation call, keeping your visual universe coherent from panel one to the end.

<br/>

---

## ✨ Features

| | Feature | Description |
|:---:|:---|:---|
| 📖 | **Storyboard Generation** | Generate structured, multi-page comic layouts from a single text prompt |
| 🎨 | **Page Rendering** | Render storyboard sketches into finished pages across multiple art styles |
| 🎭 | **My Studio** | Save characters and environments as locked reference sheets — injected into every render |
| 🔄 | **Story Continuation** | Append new pages to an existing session, keeping narrative and visual context intact |
| 📚 | **Cover Creator** | Auto-generate a cover page derived from your current story's content |
| 💾 | **Local Sessions** | Stories, Studio data, and settings persist in browser local storage — no account needed |
| 🌐 | **Multilingual** | Generate stories and display the UI in multiple languages |

<br/>

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Details |
|:---|:---|
| **Python 3.12+** | Runtime for the backend |
| **[uv](https://github.com/astral-sh/uv)** | Fast Python package manager |
| **Google Gemini API Key** | Powers all text and image generation |
| OpenAI-compatible endpoint *(optional)* | Alternative text generation path |

<br/>

### ⚡ One-Command Start

```bash
chmod +x start.sh && ./start.sh
```

This script will automatically:

1. Install all backend dependencies via `uv`
2. Start the **Flask backend** → `http://localhost:5003`
3. Start the **frontend server** → `http://localhost:8000`

Then open **[http://localhost:8000](http://localhost:8000)** in your browser.

<br/>

### 🛠️ Manual Setup

<details>
<summary>Click to expand</summary>

<br/>

**Terminal 1 — Backend:**
```bash
cd backend
uv sync
uv run app.py
```

**Terminal 2 — Frontend:**
```bash
python3 -m http.server 8000
```

</details>

<br/>

---

## ⚙️ Configuration

Open the **Config** panel inside the app to configure:

| Setting | Required | Description |
|:---|:---:|:---|
| `Gemini API Key` | ✅ | Your Google Gemini key for text and image generation |
| `Theme` | — | Light or dark mode |
| `UI Language` | — | Interface display language |
| `Story Language` | — | Language for generated comic scripts |
| `Comic Style` | — | Default visual style applied during rendering |

<br/>

---

## 🕹️ How to Use

### Creating a New Story

```
 ① Write a prompt   →   ② Set Pages & Style   →   ③ Click Run   →   ④ Render Pages
```

1. Write your story idea in the main text area
2. Set the number of **Pages** and **Rows per Page**
3. Choose a **Comic Style**
4. Click **Run** — storyboard panels are generated instantly
5. Click **Render Page** on any page, or **Render All** to produce all final images

<br/>

### Continuing an Existing Story

```
 ① Adjust the Pages slider   →   ② Click "Continue +N"   →   ③ New pages appended
```

comiCraft synthesizes existing narrative context and extends the story seamlessly — visuals and plot stay coherent.

<br/>

---

## 🎭 My Studio — The Consistency Engine

Character drift is the hardest unsolved problem in multi-page AI comic generation. **My Studio** is built specifically to address it.

### How it works

```
  ┌─────────────────────────────────────────────────────┐
  │                      MY STUDIO                      │
  │                                                     │
  │   👤 Save Characters   +   🌄 Save Environments    │
  │              │                       │              │
  │              └──────────┬────────────┘              │
  │                         ▼                           │
  │            Toggle Active / Inactive                 │
  │                         │                           │
  │                         ▼                           │
  │         Merge into Locked Reference Sheets          │
  │      [ Character Sheet ]   [ Environment Sheet ]    │
  │                         │                           │
  │                         ▼                           │
  │       Injected as top-priority input into           │
  │            every Gemini image generation            │
  └─────────────────────────────────────────────────────┘
```

### Controls

| Control | What it does |
|:---|:---|
| **Save Character / Style** | Add a name, description, and optional reference image |
| **Active / Inactive toggle** | Include or exclude individual Studio items per render |
| **Manual reference image** | Inject a specific image during a single render for precise control |

<br/>

---

## 🧩 Architecture

### Project Structure

```
comiCraft/
├── index.html                  # App entry point
├── start.sh                    # One-command startup script
├── pyproject.toml
├── uv.lock
│
├── frontend/
│   ├── css/                    # Stylesheets
│   └── js/                     # App logic, Studio manager, session handler
│
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── controllers/            # Route handlers (generate, render, cover, validate)
│   ├── services/               # Gemini integration, image pipeline
│   └── static/images/          # Generated page images written here
│
└── refer_image/                # Optional built-in style references
    └── <style>/
```

### Tech Stack

| Layer | Technology |
|:---|:---|
| Frontend | HTML · Vanilla CSS · Vanilla JavaScript |
| Backend | Python 3.12+ · Flask |
| Text Generation | Google Gemini *(+ optional OpenAI-compatible path)* |
| Image Generation | Google Gemini Imagen |
| Export Utility | `html2canvas` |
| Package Management | `uv` |

### API Endpoints

| Method | Endpoint | Purpose |
|:---:|:---|:---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/generate` | Generate storyboard from prompt |
| `POST` | `/api/generate-image` | Render a storyboard page to image |
| `POST` | `/api/generate-cover` | Generate a comic cover |
| `POST` | `/api/validate` | Validate API key and config |

<br/>

---

## 📝 Notes

- Generated images are stored at `backend/static/images/` — clear periodically to free disk space
- All session data and Studio items live in **browser local storage** — no backend persistence required
- Missing `refer_image/<style>/` directories are non-fatal; override the path with `COMICCRAFT_REFER_IMAGE_BASE_PATH`
- Chrome may request `/.well-known/appspecific/com.chrome.devtools.json` — the resulting 404 is harmless

<br/>

---

