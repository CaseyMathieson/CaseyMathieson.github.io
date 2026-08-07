# Repository Guidelines

## Project Structure & Module Organization

This repository is a static professional resume and portfolio site. Keep changes focused and preserve the paired resume outputs.

- `index.html`: primary dark-theme landing page and the resume PDF download link.
- `casey-mathieson-resume.html`: print-oriented resume source.
- `casey-mathieson-resume.pdf`: downloadable resume; regenerate it whenever its HTML source changes.
- `portfolio/`: portfolio index, individual case studies, shared `portfolio.css`, and SVG artwork in `portfolio/assets/`.
- `README.md`: brief public project description.

There is no application source directory, package manifest, test suite, or build system.

## Build, Test, and Development Commands

Serve the repository locally with Python:

```powershell
py -m http.server 8082 --bind 127.0.0.1
```

Open `http://127.0.0.1:8082/` and check the landing page, portfolio links, and PDF download. Use a different unused port when needed. Validate a targeted page with:

```powershell
Invoke-WebRequest http://127.0.0.1:8082/portfolio/ -UseBasicParsing
```

After changing `casey-mathieson-resume.html`, export it to `casey-mathieson-resume.pdf`, then confirm the updated wording appears in the PDF and visually inspect both pages. Do not leave temporary export or preview files in the repository.

## Coding Style & Naming Conventions

Use plain, semantic HTML with two-space indentation. Match existing inline CSS in root pages and the shared styles in `portfolio/portfolio.css`. Use lowercase, hyphenated filenames such as `documentation-migration.html`; place matching illustrations in `portfolio/assets/` with the same basename. Keep copy concise and use accessible headings, descriptive link text, and meaningful `alt` text for new images.

## Testing Guidelines

No automated test or lint command is configured. Before handing off a change, load every modified page locally at desktop and narrow viewport widths, check browser console errors, verify internal links, and confirm layout has no clipping or horizontal overflow. For PDF changes, verify selectable text as well as rendered layout.

## Commit & Pull Request Guidelines

Recent history uses short, imperative subjects, often scoped for portfolio work: `feat(portfolio): update case study copy`. Follow that pattern; keep commits single-purpose. Pull requests should state the user-visible change, list validation performed, link any issue when available, and include screenshots for visual or responsive changes. Do not overwrite unrelated working-tree changes.
