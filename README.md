# comiCraft

comiCraft is a browser-based comic storyboard and image generation tool.
It generates multi-page comic scripts, renders finished comic pages, keeps custom
characters and art styles in a reusable Studio, and can continue an existing
story without restarting the whole prompt.

## What It Does

- Generate multi-page comic storyboards from a prompt
- Render final comic page images from storyboard layouts
- Save custom characters and art styles in `My Studio`
- Build locked character sheets and locked environment sheets from Studio items
- Reuse those locked references to improve page-to-page consistency
- Continue an existing story by appending new pages to the current session
- Generate comic covers from existing story pages
- Save multiple local sessions in browser storage

## Current Workflow

1. Enter a prompt.
2. Set `Pages`, `Rows per Page`, `Comic Style`, and language.
3. Click `Run` to generate storyboard pages.
4. Click `Render Page` or `Render All` to create final comic images.
5. Use `My Studio` to store reusable characters and art styles.
6. Set `Pages` to how many pages to add and click `Continue +N` to extend the story.

## Studio Features

The Studio is the main consistency system in the app.

- Characters: save reusable character references with name, description, and image
- Art Styles: save reusable environment/style references with name, description, and image
- Active toggle: only active Studio items participate in generation
- Locked sheets: active Studio items are combined into:
  - a locked character sheet
  - a locked environment sheet

Those locked sheets are injected as top-priority references during comic image generation.

## Tech Stack

- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Flask
- Text generation: Google Gemini and optional OpenAI-compatible flow
- Image generation: Google Gemini image generation
- Export/render helpers: `html2canvas`

## Project Layout

```text
comic-alpha/
├── refer_image/ (optional, local built-in references)
│   └── <style>/
├── backend/
│   ├── app.py
│   ├── comic_generator.py
│   ├── controllers/
│   ├── services/
│   ├── static/
│   │   └── images/
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── css/
│   └── js/
├── index.html
├── start.sh
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.12+
- `uv`
- A Gemini API key

Optional:

- OpenAI-compatible API access if you use the OpenAI text path

## Quick Start

### Start With the Script

```bash
chmod +x start.sh
./start.sh
```

This script:

- installs backend dependencies with `uv`
- starts the Flask backend on `http://localhost:5003`
- starts a simple frontend server on `http://localhost:8000`

### Manual Start

Backend:

```bash
cd backend
uv sync
uv run app.py
```

Frontend:

```bash
python3 -m http.server 8000
```

Then open:

- Frontend: `http://localhost:8000`
- Backend API: `http://localhost:5003`

## Configuration

Open the config panel in the app and set:

- `Gemini API Key`: required for generation
- Theme
- UI language
- Story language
- Comic style

## Story Generation

### New Story

- Write the prompt
- Set `Pages`
- Click `Run`

### Continue Story

- Generate a story first
- Set `Pages` to how many pages to append
- Click `Continue +N`

The app sends the latest story context to the backend and appends the new pages
to the current session.

## Image Generation

When rendering final comic pages, the app uses:

- the current page layout sketch
- locked Studio character sheet
- locked Studio environment sheet
- active Studio item references
- optional manual reference image
- prior generated pages

This is the main consistency stack for keeping later pages aligned with saved
characters and environments.

## Sessions

Sessions are stored in browser local storage and keep:

- prompt
- generated storyboard pages
- generated page images
- current page index
- selected style/language/rows
- active Studio usage metadata

## Key API Endpoints

- `GET /api/health`
- `POST /api/generate`
- `POST /api/generate-image`
- `POST /api/generate-cover`
- `POST /api/validate`

## Notes

- Generated page images are written under `backend/static/images/`
- Studio data and sessions live in browser local storage
- Missing built-in reference directories under `refer_image/<style>/` are not fatal (set `COMICCRAFT_REFER_IMAGE_BASE_PATH` to override)
- Chrome may request `/.well-known/appspecific/com.chrome.devtools.json`; a 404 there is unrelated to app behavior

## Development Notes

Current notable product features:

- Studio active/inactive toggles
- Locked Studio sheets for stronger consistency
- Continuation flow that appends pages
- Cover generation from current story pages
