# AGENTS.md

## Repository Overview

This repository hosts a **Jekyll-based GitHub Pages website** for the University of Chicago Data Science Clinic at `https://clinic.ds.uchicago.edu`.

The repo has two main parts:
- The website content itself: markdown pages, layouts, includes, assets, and downloadable files
- A Python data pipeline under `projects/` that validates YAML data and regenerates the projects index page

## How the Site Runs

### Tech Stack
- **Static site generator**: Jekyll with the `pages-themes/minimal` remote theme
- **Hosting**: GitHub Pages, deployed from `.github/workflows/jekyll.yml`
- **Local development**: Docker image defined by `Dockerfile`
- **Ruby environment**: `github-pages` gem via Bundler
- **Python environment**: `uv` with dependencies from `pyproject.toml`
- **Data pipeline**: Pydantic + PyYAML scripts in `projects/`

### Local Development

Always use Docker via the Makefile. Do not rely on the host machine for serving the site.

```bash
make build       # Build the Docker image
make serve       # Serve the site locally on port 4000
make trace       # Serve with Jekyll trace output
make interactive # Open a shell in the container
make validate    # Validate project YAML data
make projects    # Regenerate projects/index.md from YAML
make clean       # Remove Docker resources used by this repo
make rebuild     # Clean, rebuild, and serve
make sitemap     # Intended sitemap generation target; currently broken
```

Important notes:
- Running plain `make` currently executes the first Makefile target, `build`. It does **not** start the site.
- `make serve` runs `bundle exec jekyll serve --safe --livereload --host 0.0.0.0`.
- `make projects` depends on `make validate`.

### Build Flow

1. Docker builds an image with Ruby 3.1, Python, Node, Graphviz, and `uv`
2. Bundler installs the GitHub Pages gem set
3. `uv sync` installs Python dependencies for the project scripts
4. Jekyll serves the site on port 4000 from inside Docker
5. On pushes to `main`, GitHub Actions builds and deploys to GitHub Pages

## Key Files

- `_config.yml` — Jekyll configuration, plugins, site metadata, sitemap settings
- `Dockerfile` — Local runtime used for Jekyll and Python tasks
- `Makefile` — Standard entry points for build, serve, validation, and regeneration
- `Gemfile` / `Gemfile.lock` — Ruby dependencies for GitHub Pages compatibility
- `pyproject.toml` / `uv.lock` — Python dependencies and lockfile
- `.github/workflows/jekyll.yml` — Production deploy workflow
- `.github/workflows/action.yml` — PR link-check workflow
- `.linkspector.yml` — Linkspector configuration
- `claude.md` — Additional repo notes, including known link-check issues

## Content Map

### Site Content
| Path | Purpose |
|------|---------|
| `README.md` | Landing page rendered as the site homepage |
| `students/` | Resources for enrolled students |
| `prospective-students/` | Application information and FAQ entry points |
| `mentor-ta/` | Mentor and TA guidance |
| `syllabus/` | Syllabus, dates, and weekly plan |
| `rubrics/` | Rubrics for clinic deliverables |
| `templates/` | Markdown, Word, and slide templates |
| `coding-standards/` | Coding guidance and examples |
| `tutorials/` | How-to guides for common clinic tooling/workflows |
| `presentations/` | Shared presentation assets |
| `admin/` | Internal/admin-facing documents |
| `faq/` | FAQ content |

### Layout and Assets
| Path | Purpose |
|------|---------|
| `_layouts/default.html` | Main site layout |
| `_includes/application.html` | Reusable application callout |
| `_includes/info_session.html` | Reusable info-session callout |
| `assets/css/style.scss` | Site styling overrides |
| `assets/js/scale.fix.js` | Theme JS |
| `assets/images/` | Logos, favicons, and sitemap images |

### Project Data Pipeline
| Path | Purpose |
|------|---------|
| `projects/data/projects/*.yaml` | Per-quarter project definitions |
| `projects/data/students/*.yaml` | Per-quarter student mappings |
| `projects/data/mentors_tas.yaml` | Mentor and TA registry |
| `projects/data_models.py` | Pydantic data models |
| `projects/yaml_utils.py` | YAML loading and validation helpers |
| `projects/validate_data.py` | Validation entry point |
| `projects/generate_index_md.py` | Regenerates `projects/index.md` |
| `projects/index.md` | Generated projects listing page |
| `projects/past/` | Archived quarter-specific markdown pages |
| `projects/one-pagers/` | Quarter-organized one-pager PDFs |
| `projects/pitchbooks/` | Quarter pitchbook PDFs |

Supported quarters in the current YAML-backed pipeline:
- Winter 2026
- Autumn 2022
- Winter 2023
- Spring 2023
- Autumn 2023
- Winter 2024
- Spring 2024
- Autumn 2024
- Winter 2025
- Spring 2025
- Autumn 2025

## CI/CD

- `.github/workflows/jekyll.yml` builds and deploys the site to GitHub Pages on pushes to `main`
- `.github/workflows/action.yml` runs Linkspector on pull requests and on manual dispatch

## Conventions

- **YAML naming**: Quarter files use `season_year.yaml`, for example `spring_2025.yaml`
- **Quarter path naming**: One-pager directories use `{year}-{season}`, for example `2025-spring`
- **Mentor/TA keys**: Use full names in `projects/data/mentors_tas.yaml`, and use those same full-name keys in quarter project YAML files
- **Generated projects page**: Do not edit `projects/index.md` directly; regenerate it from YAML
- **Markdown content**: Most site sections are hand-authored markdown and should be edited in place
- **Local serving**: Prefer `make serve` over ad hoc Jekyll or Python commands

## Adding A Quarter

When adding a new quarter's projects, follow this workflow:

1. Gather the quarter source materials.
   - The project roster / matching workbook is the source of truth for the project set, team assignments, mentor assignments, TA assignments, repo links, and expected team sizes.
   - The quarter pitchbook is the source of truth for the short project descriptions used in `projects/data/projects/<season>_<year>.yaml`.
   - One-pager PDFs must end up in `projects/one-pagers/<year>-<season>/` with filenames that match each `org_name` exactly, for example `projects/one-pagers/2026-winter/Accountability Counsel.pdf`.

2. Update the mentor/TA registry first.
   - Add any new mentors or TAs to `projects/data/mentors_tas.yaml`.
   - Use full names as the YAML keys.
   - Keep `display_name` aligned with the full-name key unless there is a strong reason not to.
   - Every `mentor` and `ta` value referenced by quarter project YAML must exist in this file or validation will fail.

3. Create the quarter project YAML.
   - Add `projects/data/projects/<season>_<year>.yaml`.
   - Required top-level fields are `quarter`, `year`, `name_map`, and `projects`.
   - Each project entry should include:
     - `org_name`
     - `description`
     - `project_url`
     - `mentor`
     - `ta`
     - `github_link`
     - `is_private_repo`
     - `has_one_pager`
     - `external_mentor_info`
     - `project_url_valid`
     - `is_11th_hour`
   - If the display name and the one-pager filename should differ, use `name_map` to map the PDF filename key to the display name shown on the site.

4. Create the quarter student YAML.
   - Add `projects/data/students/<season>_<year>.yaml`.
   - Required top-level fields are `quarter`, `year`, and `students`.
   - Each student entry should include:
     - `project_name`
     - `student_name`
     - `github_info`
   - `project_name` must exactly match an `org_name` in the corresponding quarter project YAML.

5. Add the quarter one-pagers.
   - Create `projects/one-pagers/<year>-<season>/` if it does not already exist.
   - Rename/copy PDFs so the final filenames match the project `org_name` values exactly.
   - If a project does not have a one-pager, set `has_one_pager: false` and do not add a PDF.

6. Update the supported-quarter lists in code.
   - Add the new quarter to `ALL_QUARTERS` in `projects/generate_index_md.py`.
   - Add the new quarter to `quarters_data` in `projects/validate_data.py`.

7. Validate and regenerate.
   - Run `make validate`.
   - Run `make projects`.
   - This regenerates `projects/index.md`; do not hand-edit that file.

8. Review the generated output.
   - Confirm the quarter appears in `projects/index.md`.
   - Check that one-pager links resolve to the expected files.
   - Check that mentors, TAs, and students render correctly.

## Known Repo Caveats

- `make sitemap` references `generate_sitemap.py`, but that script is not present in the repository
- `_site/` is generated site output and should generally not be edited directly
- The repo currently contains local/generated artifacts such as `.venv/`, `_site/`, and cache directories; treat them as derived state unless a task explicitly targets them
