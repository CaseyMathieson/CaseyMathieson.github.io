# Repository Guidelines

## Project Structure & Module Organization

This repository is a static professional resume and portfolio site. Keep changes focused and preserve the paired resume outputs.

- `index.html`: canonical résumé content, dark-theme landing page, and PDF download link.
- `casey-mathieson-resume.html`: print-oriented resume source.
- `casey-mathieson-resume.pdf`: downloadable resume; regenerate it whenever its HTML source changes.
- `scripts/check_resume_parity.py`: required résumé-content and PDF parity check.
- `portfolio/`: portfolio index, individual case studies, shared `portfolio.css`, and SVG artwork in `portfolio/assets/`.
- `README.md`: brief public project description.

## Career, Résumé, and Application Context

- Before evaluating a job or internal role, drafting or tailoring a résumé or cover letter, preparing for an interview or manager/recruiter conversation, or advising on career positioning, read `C:\Users\Casey\CloudStorage\Finance\Employment\Canonical\Career Master.md` completely. Treat it as the canonical factual source for Casey's experience and accomplishments.
- Read `C:\Users\Casey\CloudStorage\Finance\Employment\Canonical\Job Search Research Tracker.md` when application history, role status, compensation, commute, travel, preferences, or next-step context matters.
- Read `C:\Users\Casey\CloudStorage\Finance\Employment\Canonical\Source Manifest.md` when reconciling conflicting claims, dates, titles, or résumé artifacts.
- Use only claims recorded in `Career Master.md` or directly confirmed by Casey. Add newly confirmed facts to the career master before reusing them.
- Store role-specific materials under `C:\Users\Casey\CloudStorage\Finance\Employment\Current\Applications\`. Never overwrite previously submitted materials, and keep private employment records out of Git.
- For tailored résumé PDFs, validate page count, HTML/PDF text parity, text bounds, and rendered pages.

## Build, Test, and Development Commands

Serve the repository locally with Python:

```powershell
py -m http.server 8082 --bind 127.0.0.1
```

Open `http://127.0.0.1:8082/` and check the landing page and PDF download. Use a different unused port when needed. Run the required parity check with:

```powershell
py scripts/check_resume_parity.py
```

Treat `index.html` as the wording and factual source of truth. Keep the headline, summary, expertise claims, employers, dates, roles, experience bullets, and credentials aligned with `casey-mathieson-resume.html`. Print-only adaptations may change layout, grouping, separators, and contact presentation; they must not paraphrase, add, or omit substantive content. After either résumé HTML file changes, update the print source, export the PDF, run the parity check, and visually inspect every PDF page. Do not leave temporary export or preview files in the repository.

## Coding Style & Naming Conventions

Use plain, semantic HTML with two-space indentation. Match existing inline CSS in root pages and the shared styles in `portfolio/portfolio.css`. Use lowercase, hyphenated filenames such as `documentation-migration.html`; place matching illustrations in `portfolio/assets/` with the same basename. Keep copy concise and use accessible headings, descriptive link text, and meaningful `alt` text for new images.

## Testing Guidelines

Before handing off résumé changes, require `py scripts/check_resume_parity.py` to pass; it compares canonical content with the print source and confirms every print unit is extractable from the PDF. Also load modified pages locally at desktop and narrow widths, check console errors and links, and confirm there is no clipping or horizontal overflow. For PDF changes, visually inspect all pages in addition to the parity check.

## Commit & Pull Request Guidelines

Recent history uses short, imperative subjects, often scoped for portfolio work: `feat(portfolio): update case study copy`. Follow that pattern; keep commits single-purpose. Pull requests should state the user-visible change, list validation performed, link any issue when available, and include screenshots for visual or responsive changes. Do not overwrite unrelated working-tree changes.
