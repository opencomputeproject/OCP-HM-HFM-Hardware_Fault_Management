# OCP Hardware Fault Management Specifications (Source + Published)

This repository hosts **specification sources** (Markdown/inputs) and **published artifacts** (PDFs) for fault-management-related work under the OCP Hardware Management umbrella.

> **Public repository note:** Do **not** submit confidential information. OCP project materials are published publicly in accordance with OCP policies.
## Repository layout (source vs published)

This repo is intentionally split into:
- **`specs/`** — *canonical sources* (reviewed via PRs)
- **`docpubs/`** — *published outputs* (rendered PDFs, and optionally HTML)

### Top-level
- `.github/workflows/` — CI/build automation (e.g., rendering/publishing)
- `templates/` — shared templates and style guidance
- `specs/` — sources for each specification area
- `docpubs/` — rendered artifacts for each specification area

### Per-spec folder convention

For each spec area `<SpecName>` (examples in this repo: `System-Debug`, `RAS_API`, `Fleet_Memory_Fault_Management`, etc.):

**Sources**
- `specs/<SpecName>/src/` — Markdown (or spec-tool input files) and chapter content
- `specs/<SpecName>/figures/` — images/diagrams referenced by the spec
- `specs/<SpecName>/tables/` — CSV/JSON tables referenced by the spec

**Published outputs**
- `docpubs/<SpecName>/pdf/` — published PDF(s)
- `docpubs/<SpecName>/releases/` — optional bundles/checksums/“release” packaging

## Contributing content (how to create a Pull Request)

OCP software/spec repositories commonly use **GitHub Issues** to track work and accept changes via **GitHub Pull Requests (PRs)**. 

### Start with an Issue (recommended)
- Create a GitHub Issue (or find an existing one) for the change you’re making. 
- Link the Issue in your PR description so discussion stays connected. 
- 
### Decide: branch vs fork
- **If you have write permission** to this repository: create a **branch** in this repo and open a PR from that branch. 
- **If you do not have write permission**: create a **fork** and open a PR back to this repo. 
- 
### Make your change in `specs/`
- Update the canonical source content under `specs/<SpecName>/...` (e.g., `src/`, `figures/`, `tables/`).

### Render your spec locally (required before submitting the PR)
Before opening the PR, **render the spec** to confirm there are no formatting/rendering errors.

See instructions for the rendering process

OCP provides a Docker-based renderer in `opencomputeproject/ocp-spec-tools`. The README shows how to set up an `ocp_render` alias and render both PDF and HTML; it also notes you must run the command from the directory containing the input file. 

Example (from `ocp-spec-tools` usage):
- Render PDF: `ocp_render --pdf spec.pdf spec.ocp`
- Render HTML: `ocp_render --html spec.html spec.ocp` 
- 
> Store published outputs under `docpubs/<SpecName>/pdf/` only when you intend to publish/version outputs; otherwise keep the PR focused on source changes.

### Push your branch and open the PR on GitHub
On GitHub:
- Open a Pull Request from your **head** branch into the target **base** branch (typically `main`). 
- Fill in the PR title/body and follow any PR template if present. 
### What to include in the PR description
- **What / Why:** summary of the change and motivation
- **Scope:** what’s included (and what’s intentionally out of scope)
- **Links:** the related Issue and any relevant public references
- **Render proof:** mention the command you ran (PDF and/or HTML) and whether it succeeded

### After you open the PR
- Respond to review comments and push updates to the same branch (the PR updates automatically). 

## Rendering / Building PDFs locally

OCP provides an open-source rendering toolchain in **`opencomputeproject/ocp-spec-tools`**, including:
- scripts to render specs locally (Docker-based)
- a reusable GitHub workflow for publishing to GitHub Pages 

### Install the renderer (one-time)
Follow the “How to run locally” instructions in the `ocp-spec-tools` repo:
- OCP spec tools: https://github.com/opencomputeproject/ocp-spec-tools 
The `ocp-spec-tools` README shows example commands to render a PDF and HTML locally. 

### Render a spec from this repo
At a high level:
1. `cd` into the directory containing the spec input file(s)
2. run the renderer to generate a PDF into `docpubs/<SpecName>/pdf/`

> The exact command line depends on how each spec’s `src/` is organized (single-file vs multi-file aggregation).  
> Use the `ocp-spec-tools` “How to run locally” section as the reference for the supported CLI flags and usage. 

## Publishing (GitHub Actions / GitHub Pages)

`opencomputeproject/ocp-spec-tools` provides a **reusable GitHub workflow** to render specifications and publish outputs. 
There are two useful references:
- `ocp-spec-tools` GitHub Pages guide (`GITHUB_PAGES.md`) 

## Adding a new specification area

To add a new spec area named `<NewSpec>`:
1. Create the source folders:
   - `specs/<NewSpec>/src`
   - `specs/<NewSpec>/figures`
   - `specs/<NewSpec>/tables`
2. Create the published folders:
   - `docpubs/<NewSpec>/pdf`
   - `docpubs/<NewSpec>/releases`
3. Add initial content under `specs/<NewSpec>/src`
4. If CI publishing is enabled, add `<NewSpec>` to the workflow’s render input list (see the OCP spec-tools GitHub Pages guidance and examples).

## Contribution model

OCP software/spec repositories typically use GitHub Issues to track work and accept changes via pull requests. 
If you are contributing:
- Prefer small, reviewable PRs
- Keep source edits under `specs/`
- Place rendered PDFs under `docpubs/` only when publishing/versioning outputs

## License

This repository is MIT-licensed (see `LICENSE`). 
