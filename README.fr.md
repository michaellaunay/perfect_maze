# perfect_maze

*[English version](README.md)*

<!-- --8<-- [start:intro] -->
Une petite bibliothèque Python sans dépendance, avec un outil en ligne de
commande, qui génère des **labyrinthes parfaits** et les affiche avec les
caractères de tracé de cadres UTF-8.

Un labyrinthe parfait n'a ni cellule isolée ni boucle : chaque cellule est
reliée à chaque autre par exactement un chemin. Structurellement, c'est un
arbre couvrant du graphe-grille.

```text
┌─────┬─┬─┬─────┬───┬───┐
│ ╷ ╶─┘ │ └─┐ ╷ ╵ ╷ ╵ ┌─┤
│ ├─┬─╴ │ ╶─┘ ├─╴ └─┐ ╵ │
│ │ └─╴ └─╴ ╶─┼─┐ ╷ │ ╶─┤
│ ├───╴ ╶─────┘ │ │ │ ╶─┤
└─┴─────────────┴─┴─┴───┘
```

Nécessite Python 3.12 ou plus récent.
<!-- --8<-- [end:intro] -->

<!-- --8<-- [start:usage] -->
## Installation

```shell
pip install perfect-maze          # depuis PyPI, une fois publié
pip install git+https://github.com/michaellaunay/perfect_maze.git
```

## Ligne de commande

```shell
perfect-maze                       # labyrinthe 6x4 sur la sortie standard
perfect-maze -w 40 -H 20           # 40 colonnes sur 20 lignes
perfect-maze -w 12 -H 5 --seed 42  # labyrinthe reproductible
perfect-maze -w 8 -H 8 -o maze.py  # enregistre aussi les tirages dans maze.py
python -m perfect_maze --help      # même outil, sans le script console
```

| Option | Description |
| --- | --- |
| `-w`, `--width N` | nombre de cellules par ligne (6 par défaut) |
| `-H`, `--height N` | nombre de lignes (4 par défaut) |
| `-s`, `--seed N` | graine du générateur aléatoire |
| `-o`, `--output PATH` | écrit la séquence des tirages, `open_walls` et le dessin dans `PATH` |
| `-q`, `--quiet` | n'affiche pas le labyrinthe |
| `-V`, `--version` | affiche la version |

Le fichier produit par `--output` est du Python valide. Sa structure est
celle des fixtures de test : un labyrinthe intéressant peut être collé tel
quel dans `tests/fixtures.py` comme cas de non-régression.

## Bibliothèque

```python
from perfect_maze import build_maze, printable_maze

maze = build_maze(60, 40)
print(printable_maze(maze))  # ou simplement print(maze)
```

Génération reproductible et aller-retour :

```python
import random
from perfect_maze import build_maze, printable_maze

maze = build_maze(10, 8, randrange=random.Random(42).randrange)

# open_walls est la liste des passages ouverts pendant la génération, dans
# l'ordre. La réinjecter reconstruit exactement le même labyrinthe sans
# aucun aléa.
again = build_maze(10, 8, open_walls=maze.open_walls)
assert printable_maze(again) == printable_maze(maze)
```

Parcourir le labyrinthe :

```python
from perfect_maze import Direction

cell = maze[0, 0]  # cellule en (x=0, y=0)
for direction, neighbour in cell.neighbours():
    if cell.is_open(direction):
        print(f"on peut aller vers {direction.name}, cellule {neighbour.index}")
```

Attachez vos propres données aux cellules en dérivant `Cell` et en passant
`cell_type=` :

```python
from perfect_maze import Cell, build_maze


class Room(Cell):
    __slots__ = ("visited",)

    def __init__(self, index: int = -1) -> None:
        super().__init__(index)
        self.visited = False


maze = build_maze(5, 5, cell_type=Room)
```

<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:algorithm] -->
## Fonctionnement

La grille démarre avec tous ses murs construits. Des murs sont ensuite tirés
au hasard et supprimés dès qu'ils séparent deux cellules pas encore reliées,
une structure Union-Find suivant la connexité. La boucle s'arrête après la
suppression de `width * height - 1` murs, exactement le nombre d'arêtes d'un
arbre couvrant.

<!-- --8<-- [end:algorithm] -->

<!-- --8<-- [start:development] -->
## Développement

```shell
git clone https://github.com/michaellaunay/perfect_maze.git
cd perfect_maze
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,docs]"

ruff format . && ruff check .      # formatage et analyse statique
pytest --cov                       # tests avec couverture
zensical serve                     # documentation avec rechargement à chaud
```

Documentation : <https://michaellaunay.github.io/perfect_maze/>

<!-- --8<-- [end:development] -->

## Journal des modifications

Voir [CHANGELOG.md](CHANGELOG.md) (en anglais).

## Licence

GNU Affero General Public License v3.0 ou ultérieure — voir [LICENSE](LICENSE).
