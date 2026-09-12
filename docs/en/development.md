# Development

--8<-- "README.md:development"

## Documentation

The site is written in Markdown under `docs/` and built with
[Zensical](https://zensical.org/); the API pages are generated from the
docstrings by [mkdocstrings](https://mkdocstrings.github.io/). The
documentation exists in two languages: `docs/en/` and `docs/fr/`.

The *Usage* and *Development* pages include sections of `README.md`
(English) or `README.fr.md` (French), and the *Changelog* pages include
`CHANGELOG.md`, so these three files are the single source of truth; the
site pages only assemble them. Any change to one README must be mirrored in
the other.

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
