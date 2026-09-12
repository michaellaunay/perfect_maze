# Développement

--8<-- "README.fr.md:development"

## Documentation

Le site est écrit en Markdown dans `docs/` et construit avec
[Zensical](https://zensical.org/) ; les pages d'API sont générées depuis les
docstrings par [mkdocstrings](https://mkdocstrings.github.io/). La
documentation existe en deux langues : `docs/en/` et `docs/fr/`.

Les pages *Utilisation* et *Développement* incluent des sections du
`README.md` (anglais) ou du `README.fr.md` (français), et les pages *Journal
des modifications* incluent `CHANGELOG.md` : ces trois fichiers sont la
source unique de vérité, les pages du site n'en sont que l'assemblage. Toute
modification de l'un des README doit être reportée dans l'autre.

```shell
zensical serve            # aperçu à http://127.0.0.1:8000
zensical build --strict   # ce que lance l'intégration continue
```

Chaque push sur `main` déploie le site sur GitHub Pages.

## Publication d'une version

1. Mettre à jour `CHANGELOG.md` : déplacer les entrées *Unreleased* sous un
   nouveau titre de version et ajouter le lien de comparaison en bas.
2. Incrémenter `__version__` dans `src/perfect_maze/_version.py`.
3. Committer, poser l'étiquette `vX.Y.Z` et la pousser.
4. Construire et publier : `python -m build && twine upload dist/*`.
