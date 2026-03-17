# Repository instructions

## Build, test, and lint

- No repository-local build, test, or lint commands are checked in. There is no `Gemfile`, `package.json`, `Makefile`, or GitHub Actions workflow in this repo.
- Single-test execution is not applicable here because there is no checked-in test harness.
- Do not invent local validation commands. For documentation changes, validate by checking:
  - Jekyll front matter consistency
  - `docs/_data/navigation.yaml` alignment with added or moved pages
  - Internal link and asset path consistency

## High-level architecture

- This repository is a **documentation site** for the Fourier-GRX-M4 SDK, not the SDK implementation itself. The docs repeatedly point to runtime files under `$HOME/fourier-grx/...` and to example code in the external `Wiki-GRx-Deploy` repository, usually on the `FourierM4` branch.
- The site is a Jekyll docs site configured in `_config.yaml` with the `just-the-docs` remote theme and plugins such as `jekyll-relative-links`, `jekyll-remote-theme`, and `jekyll-seo-tag`.
- `index.md` is the landing page. The left-side documentation structure is defined in `docs/_data/navigation.yaml`, while individual pages also carry their own front matter for title, ordering, and hierarchy.
- Content is organized around the product workflow:
  - `docs/quickstart*` for robot bring-up and environment setup
  - `docs/examples*` for runnable User/Developer examples
  - `docs/reference*` for API, config, run mode, resource, and CLI details
  - `docs/tasks*` for task/module semantics and per-task reference pages
  - `docs/usage.md`, `docs/faq.md`, `docs/update.md`, `docs/changelog.md` for operations and maintenance
- The core conceptual split across the docs is:
  - **User API**: high-level control over Zenoh topics like `fourier-grx/dynalink_interface/{comm|robot|task|grx|rehab}/{server|client}`
  - **Developer API**: lower-level Python access via `fourier_core` and `fourier_grx`, intended to run on the robot controller
- Task documentation connects multiple surfaces: physical controller input, keyboard input, User API task/component updates, and Developer API task/component calls. When editing task docs, keep those mappings consistent across `docs/tasks.md`, per-task pages, and relevant reference pages.

## Key conventions

- Most pages use YAML front matter with `layout: default`, `title`, and `nav_order`. Child pages also use `parent`. Pages either use `toc: true` with explicit min/max settings or `has_toc: true` plus `{:toc}` in the body; follow the pattern already used by nearby pages.
- Internal links and assets are usually written as absolute site paths rooted at `/fourier-grx-M4/...`. Keep new links in that form unless the surrounding file clearly uses another pattern.
- The documentation language is primarily Chinese. Keep headings, navigation labels, and prose aligned with the surrounding Chinese terminology instead of introducing mixed-language sections.
- Command examples are product commands, not repo-maintenance commands. The most important recurring commands are `fourier-grx start`, `fourier-grx config`, `fourier-grx list`, `fourier-grx install`, `fourier-grx enable_service`, `fourier-grx disable_service`, and `fourier-grx setup_conda`.
- Example commands assume a Conda environment named `fourier-grx` and filesystem paths such as `$HOME/fourier-grx/...` and `$HOME/Wiki-GRx-Deploy/...`. Keep those path conventions intact when editing example snippets.
- The examples docs distinguish where code runs:
  - User examples can run on the robot controller or another machine on the same LAN
  - Developer examples must run on the robot controller for real-time access
- Task detail pages under `docs/tasks/` follow a repeated template: task info, module info, interface info, and update log. Preserve that structure when adding or normalizing task pages.
- Startup/configuration docs assume `~/fourier-grx/run.sh` selects the active config using `robot_type`, `robot_version`, and `run_type`. Changes to config-related docs should stay consistent with that flow.
- Watch for stale copy-paste references to `N1`, `FourierN1`, or `/fourier-grx-N1/...` inside M4 docs. When touching those sections, prefer M4-specific names, links, and branches unless the page is intentionally cross-product.
