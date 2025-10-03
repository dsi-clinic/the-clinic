# Repository Information

This repository hosts a GitHub Pages website for the DSI Clinic.

## Serving the Website Locally

To serve the website locally, use Docker with the provided Makefile:

```bash
make
```

**Important**: Do not use the local environment for serving the page. Always use Docker via the Makefile.

## Recent Issues

### Link Checker Errors

The linkspector GitHub Action has identified the following issues:

1. **Directory read error**: `../students/#finals-week-deliverables` is being treated as a file when it's actually a directory

2. **301 redirects**: Two PDF links in `projects/past/2025_Spring_projects.md` are returning 301 redirects:
   - `https://dsi-clinic.github.io/the-clinic/projects/one-pagers/2025-spring/IDI%20-%20Grievences.pdf` (line 59)
   - `https://dsi-clinic.github.io/the-clinic/projects/one-pagers/2025-spring/Kids%20First%20Chicago.pdf` (line 71)

These are likely caused by spaces in filenames requiring URL encoding.
