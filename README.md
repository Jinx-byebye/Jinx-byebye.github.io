# Langzhang Liang's homepage

A static academic homepage for GitHub Pages. HTML, CSS, JavaScript, fonts, and paper figures are served directly from this repository; no Jekyll or JavaScript build dependencies are required.

## Update the homepage

- Edit profile text in `scripts/homepage.template.html`.
- Edit publication metadata in `data/publications.json`. Use `published` for published or accepted work and `preprint` for unpublished manuscripts.
- Add original paper figures to `assets/img/papers/`, then set each paper's `image` and `image_alt`. A text treatment is available when no figure is suitable or accessible.
- Update styling in `assets/css/main.css` and interactions in `assets/js/main.js`.
- Regenerate the tracked homepage with `python3 scripts/build.py`.

## Preview

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this directory and open `http://127.0.0.1:8000`. All content and navigation work without JavaScript; JavaScript adds topic filters, theme switching, and figure enlargement.

## Hosting

When ready to make the site available, configure GitHub Pages to serve the `main` branch from the repository root. `.nojekyll` serves the generated HTML directly. Repository visibility and Pages settings are managed separately; changing source files does not enable publication.

Fonts are self-hosted under their SIL Open Font Licenses in `assets/fonts/`. Paper figure provenance is recorded in `data/figure-sources.json`. The previous homepage used the Minimal Light theme; its original MIT license is retained in `LICENSE`.
