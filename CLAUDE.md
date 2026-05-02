# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flaney Associates is a static single-page marketing website for a materials engineering consultancy. It is deployed via GitHub Pages at **https://jotaigbe2026.github.io/Flaney_Associates**.

There is no build system, bundler, or package manager. The site is pure HTML/CSS/JS.

## Running Locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

This is required (rather than opening index.html directly) because the gated PDF download system uses `fetch()`, which is blocked by browsers on `file://` URLs.

## Generating Article Files

All 12 blog articles exist in both PDF and DOCX format inside `articles/`.

| Script | Purpose |
|---|---|
| `generate_pdfs.py` | Original 6 PDFs (Round 1) |
| `generate_pdfs_v2.py` | New 6 PDFs (Round 2) |
| `generate_docx.py` | All 12 DOCX files |

```bash
# Regenerate all PDFs (Round 1)
python3 generate_pdfs.py

# Regenerate all PDFs (Round 2)
python3 generate_pdfs_v2.py

# Regenerate all DOCX files
python3 generate_docx.py
```

Dependencies: `reportlab` (PDF), `python-docx` (DOCX).
```bash
pip3 install reportlab python-docx
```

## Deploying

```bash
git add -A
git commit -m "your message"
git push origin main
```

GitHub Pages serves from the `main` branch root. Changes are live within ~60 seconds of push.

## Architecture

### Single-Page Layout (`index.html`)
All content lives in one HTML file. Sections in order: `#navbar → #hero → .trust-bar → #services → #expertise → #process → #industries → #about → #testimonials → #blog → #contact → footer → #downloadModal`.

### Lead Capture System (`script.js`)
Two lead capture paths both funnel to `sendToFormsubmit()`, which POSTs to `https://formsubmit.co/ajax/info@flaneyassociates.com`:
- **Contact form** (`#contactForm`) — consultation requests, submits name/email/company/service/message.
- **PDF download modal** (`#downloadModal`) — gated downloads; captures name/email/company and the article title before triggering the download.

Captured lead data is persisted in `localStorage` under the key `flaney_lead`. On subsequent visits, returning leads bypass the modal and download PDFs directly.

Email validation (`validateEmail()`) blocks disposable domains (hardcoded list at top of `script.js`) and runs on both forms with 400ms debounce + immediate blur validation.

### Styling (`styles.css`)
CSS custom properties defined in `:root` control the entire colour palette and spacing. Primary brand colours: `--primary: #1a3a5c` (navy), `--accent: #2d8cf0` (blue). Responsive breakpoints at 768px and 480px.

Scroll-triggered fade-in animations are applied via `IntersectionObserver` in `script.js` to all `.service-card`, `.expertise-card`, `.industry-card`, `.testimonial-card`, `.process-step`, and `.blog-card` elements.

### Article Generation Scripts
All three Python scripts share the same brand colour constants (`PRIMARY`, `ACCENT`, etc.) and helper pattern. Each article is a standalone function that receives `story` (reportlab) or `doc` (python-docx) and appends content. A shared `add_contact_footer()` / `footer_block()` is appended to every article.

When adding a new article:
1. Add an article function to the relevant Python script.
2. Register it in the `articles` list in `if __name__ == "__main__"`.
3. Add a corresponding `<article class="blog-card">` block in `index.html` inside the `.blog-grid` div in the `#blog` section, using `data-pdf` and `data-title` attributes on the `.gated-download` button.

## Brand & Contact Details

- **Email:** info@flaneyassociates.com
- **Phone:** +1 (601) 402-7282
- **LinkedIn:** https://www.linkedin.com/in/joshua-otaigbe-ceng-fimmm-faeng-22751322
- **Author credit on articles:** Joshua U. Otaigbe, PhD
- **Form submissions go to:** formsubmit.co → info@flaneyassociates.com
