# CATBench Documentation

This directory contains the documentation for CATBench, hosted on GitHub Pages.

## Local Development

To run the documentation locally:

```bash
# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve --baseurl=""

# Visit http://localhost:4000
```

## Documentation Structure

- `index.md` - Main landing page
- `getting-started.md` - Installation and quick start guide
- `benchmarks.md` - Available benchmarks and their parameters
- `api-reference.md` - Detailed API documentation
- `examples.md` - Code examples and tutorials
- `deployment.md` - Hardware setup and cluster configuration
- `contributing.md` - Contribution guidelines
- `_config.yml` - Jekyll configuration for GitHub Pages

## Adding New Pages

1. Create a new `.md` file in the `docs/` directory
2. Add front matter at the top:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   ---
   ```
3. Update `_config.yml` navigation if needed
4. Commit and push to trigger deployment

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/docs.yml`.

Access the live documentation at: https://odgaard.github.io/catbench/

## Note on GitHub Pages

Since the main odgaard.github.io is used for a personal website, this documentation will be available at the `/catbench` subpath. GitHub Pages automatically serves project documentation this way when:
1. The repository is public
2. GitHub Pages is enabled in repository settings
3. The documentation is built to the `gh-pages` branch or from the `docs/` folder