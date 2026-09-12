# Development

--8<-- "README.md:development"

## Documentation

The site is written in Markdown under `docs/` and built with
[Zensical](https://zensical.org/); the API pages are generated from the
docstrings by [mkdocstrings](https://mkdocstrings.github.io/). The
`docs/usage.md` and `docs/development.md` pages include sections of the
project `README.md`, and `docs/changelog.md` includes `CHANGELOG.md`, so
those two files are the single source of truth.

```shell
zensical serve            # live preview at http://127.0.0.1:8000
zensical build --strict   # what the CI runs
```

Every push to `main` deploys the site to GitHub Pages.

## Releasing

1. Update `CHANGELOG.md`: move the *Unreleased* entries under a new version
   heading and add the comparison link at the bottom.
2. Bump `__version__` in `src/perfect_maze/_version.py`.
3. Commit, tag `vX.Y.Z` and push the tag.
4. Build and publish: `python -m build && twine upload dist/*`.
