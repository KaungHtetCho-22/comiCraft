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

**Turn your imagination into panels. One prompt at a time.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

[**Features**](#-features) &nbsp;·&nbsp; [**Quick Start**](#-quick-start) &nbsp;·&nbsp; [**How to Use**](#-how-to-use) &nbsp;·&nbsp; [**Architecture**](#-architecture) &nbsp;·&nbsp; [**Studio Guide**](#-mastering-consistency-with-my-studio)

<br/>

<div align="center">

![comiCraft Demo](assets/demo.mp4)

</div>

---

## What is comiCraft?

**comiCraft** is a browser-based creative tool that transforms text prompts into fully-rendered, multi-page comic storyboards — powered by Google Gemini's multimodal generation. It's designed for writers, artists, and storytellers who want to visualize their ideas fast, without sacrificing visual consistency across pages.

The core challenge in generative comics is **character drift** — your hero looks completely different by page 3. comiCraft solves this with **My Studio**, a consistency engine that locks character and environment references into every generation call, keeping your visual universe coherent from panel to panel.

<br/>

## ✨ Features

| | Feature | Description |
|---|---|---|
| 📖 | **Storyboard Generation** | Instantly generate structured, multi-page comic layouts from a single text prompt |
| 🎨 | **Page Rendering** | Render storyboard sketches into finished comic pages across multiple art styles |
| 🎭 | **My Studio** | A consistency engine — save characters and environments as locked reference sheets |
| 🔄 | **Story Continuation** | Append new pages to an existing session, keeping narrative and visual context intact |
| 📚 | **Cover Creator** | Auto-generate a cover page derived from your current story's content |
| 💾 | **Local Sessions** | Stories, Studio data, and settings persist in browser local storage — no account needed |
| 🌐 | **Multilingual** | Generate stories and UI in multiple languages |

<br/>

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- [`uv`](https://github.com/astral-sh/uv) — fast Python package manager
- A **Google Gemini API Key**
- *(Optional)* OpenAI-compatible API endpoint for the alternative text path

### ⚡ One-Command Start

```bash
chmod +x start.sh && ./start.sh
```

This script will:
1. Install all backend dependencies via `uv`
2. Start the **Flask backend** at `http://localhost:5003`
3. Start the **frontend server** at `http://localhost:8000`

Then open **[http://localhost:8000](http://localhost:8000)** in your browser.

### 🛠️ Manual Setup

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

<br/>

## ⚙️ Configuration

Click the **Config** panel inside the app to set:

| Setting | Required | Description |
|---|---|---|
| `Gemini API Key` | ✅ Yes | Your Google Gemini key for text and image generation |
| `Theme` | No | Light or dark mode |
| `UI Language` | No | Interface display language |
| `Story Language` | No | Language for generated comic scripts |
| `Comic Style` | No | Default visual style applied during rendering |

<br/>

## 🕹️ How to Use

### Creating a New Story

```
Write a prompt  →  Set Pages & Style  →  Click Run  →  Render Pages
```

1. Write your story prompt in the main text area
2. Set the number of **Pages** and **Rows per Page**
3. Choose a **Comic Style**
4. Click **Run** — storyboard panels are generated
5. Click **Render Page** or **Render All** to produce the final images

### Continuing an Existing Story

1. After generating a story, adjust the **Pages** slider to your desired extension count
2. Click **Continue +N**
3. comiCraft synthesizes the existing narrative context and appends new pages seamlessly

<br/>

## 🎭 Mastering Consistency with My Studio

Character and environment drift is the hardest problem in multi-page AI comic generation. **My Studio** is built specifically to address this.

```
Save Characters & Styles
        ↓
Toggle Active Items
        ↓
Lock into Reference Sheets  ←─── The consistency layer
        ↓
Inject into Every Generation Call
```

**How it works:**

- **Save** characters with names, descriptions, and reference images
- **Save** art styles / environments the same way
- **Toggle** which items are active for the current generation
- When you render, active items are **merged into two locked reference sheets** — a Character Sheet and an Environment Sheet — which are injected as top-priority inputs into Gemini's image generation call

This significantly reduces panel-to-panel drift without requiring you to re-describe characters on every page.

**Additional controls:**
- **Active/Inactive toggle** — include or exclude individual Studio items per generation
- **Manual reference image** — inject a specific image during a single render for precise control

<br/>

## 🧩 Architecture

```
comiCraft/
├── index.html              # App entry point
├── start.sh                # One-command startup script
├── pyproject.toml          # Root-level Python config
├── uv.lock
│
├── frontend/
│   ├── css/                # Stylesheets
│   └── js/                 # App logic, Studio manager, session handler
│
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── controllers/        # Route handlers (generate, render, cover, validate)
│   ├── services/           # Business logic — Gemini integration, image pipeline
│   └── static/images/      # Generated page images written here
│
└── refer_image/            # Optional built-in style references
    └── <style>/
```

### Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML · Vanilla CSS · Vanilla JavaScript |
| Backend | Python 3.12+ · Flask |
| Text Generation | Google Gemini *(+ optional OpenAI-compatible path)* |
| Image Generation | Google Gemini Imagen |
| Export Utility | `html2canvas` |
| Package Management | `uv` |

### Key API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/generate` | Generate storyboard from prompt |
| `POST` | `/api/generate-image` | Render a storyboard page to image |
| `POST` | `/api/generate-cover` | Generate a comic cover |
| `POST` | `/api/validate` | Validate API key and config |

<br/>

## 📝 Development Notes

- Generated images are stored at `backend/static/images/` — clear periodically to free disk space
- All session data and Studio items live in **browser local storage** — no backend persistence is required
- Missing `refer_image/<style>/` directories are non-fatal; override the path with `COMICCRAFT_REFER_IMAGE_BASE_PATH`
- Chrome may request `/.well-known/appspecific/com.chrome.devtools.json` — the resulting 404 is harmless and unrelated to app behavior

<br/>

