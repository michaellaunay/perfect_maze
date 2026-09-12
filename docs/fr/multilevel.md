# Labyrinthes multi-niveaux (conception)

!!! note "Statut"
    Cette page est une **proposition de conception**. Rien de ce qui est
    décrit ici n'est encore implémenté ; elle existe pour que la conception
    soit relue avant d'écrire la moindre ligne de code.

## Objectif

Construire une *tour* de labyrinthes empilés :

- chaque niveau est un labyrinthe 2D **parfait** ordinaire, construit
  indépendamment, et les niveaux peuvent avoir des **tailles différentes** ;
- chaque niveau est **placé librement** au-dessus du précédent : son coin
  supérieur gauche est décalé de `(dx, dy)` cellules par rapport au coin du
  niveau inférieur ;
- un nombre choisi de cellules de chaque niveau communiquent avec le niveau
  inférieur par des **escaliers**, de sorte que toute la tour se parcourt
  d'un niveau à n'importe quel autre ;
- les paramètres (nombre de niveaux, taille, décalage et nombre d'escaliers
  de chaque niveau) sont demandés **avant** la génération, puis chaque
  niveau est affiché avec ses cellules d'escalier marquées `U` (*up*, vers
  le haut), `D` (*down*, vers le bas) ou `B` (*both*, les deux).

## Vocabulaire

| Terme | Signification |
| --- | --- |
| **Niveau** | Un labyrinthe 2D parfait. Les niveaux sont numérotés à partir de `0` (rez-de-chaussée) en montant. Chaque niveau a une largeur, une hauteur et une **origine**. |
| **Décalage** | `(dx, dy)` : position du coin supérieur gauche du niveau `i` par rapport au coin supérieur gauche du niveau `i − 1`. Peut être négatif. Le niveau `0` n'a pas de décalage. |
| **Origine** | Position absolue du coin supérieur gauche d'un niveau dans la tour : somme des décalages des niveaux jusqu'à lui. Le niveau `0` est en `(0, 0)`. |
| **Coordonnées de tour** | Coordonnées absolues `(X, Y)` d'une cellule. La cellule `(x, y)` du niveau `i` d'origine `(ox, oy)` est en `(X, Y) = (ox + x, oy + y)`. |
| **Recouvrement** | Les cellules de deux niveaux consécutifs qui ont les mêmes coordonnées de tour : l'intersection des deux rectangles. Les escaliers ne peuvent être placés que là. |
| **Escalier** | Un passage entre la cellule du niveau `i` et la cellule du niveau `i + 1` qui partagent les coordonnées de tour `(X, Y)`. |
| **Tour** | La liste des niveaux plus la liste des escaliers. |

## Paramètres et invites

La session interactive demande, dans l'ordre :

1. le nombre de niveaux `n ≥ 1` ;
2. pour le niveau `0` : sa largeur et sa hauteur ;
3. pour chaque niveau `i ≥ 1` : sa largeur, sa hauteur, son décalage
   `dx, dy` par rapport au niveau inférieur, puis le nombre d'escaliers
   `k_i` entre le niveau `i` et le niveau `i − 1`.

La validation se fait à la saisie de chaque valeur, avec nouvelle invite en
cas d'erreur :

- largeurs et hauteurs sont des entiers `≥ 1` ;
- `dx, dy` sont deux entiers, éventuellement négatifs, séparés par une
  virgule ou un espace ; le recouvrement résultant avec le niveau inférieur
  doit contenir au moins une cellule, sinon le décalage est refusé en
  indiquant la plage autorisée ;
- `k_i` est un entier tel que `1 ≤ k_i ≤ recouvrement(i − 1, i)` ; l'invite
  affiche le maximum, p. ex. `Escaliers vers le niveau 0 (1-15) [1] :`.

Une valeur par défaut est proposée entre crochets (`0, 0` pour le décalage)
et acceptée par une ligne vide : une tour peut se créer en appuyant sur
Entrée à répétition. La tour n'est générée et affichée qu'une fois toutes
les valeurs connues.

Les mêmes paramètres peuvent être passés en ligne de commande pour les
scripts et les tests, un niveau par argument, sous la forme
`LARGEURxHAUTEUR[@DX,DY][:ESCALIERS]` :

```shell
perfect-maze levels 8x5 6x4@1,1:2 4x3@-1,2:1 --seed 7
```

## Structure et propriétés

Chaque niveau est généré par le [`build_maze`][perfect_maze.maze.build_maze]
existant : c'est donc un labyrinthe parfait à lui seul, avec `w·h − 1`
passages, connexe et sans boucle. Les escaliers sont ensuite ajoutés sans
modifier aucun mur.

**Avec exactement un escalier par paire de niveaux, la tour entière est
elle-même un labyrinthe parfait** (un arbre relié à un arbre par une seule
arête est un arbre).

**Avec `k ≥ 2` escaliers entre deux niveaux, la tour contient des boucles** :
deux arbres joints par `k` arêtes ont `k − 1` cycles indépendants. Chaque
niveau reste parfait en 2D, ce qui est demandé, mais un chemin entre deux
cellules de la tour n'est plus unique. C'est un choix délibéré ; une future
option `--globally-perfect` pourrait rétablir l'unicité en fermant un mur 2D
par escalier supplémentaire, au prix de la perfection 2D d'un niveau, et ne
fait donc pas partie de cette conception.

Les escaliers sont tirés uniformément au hasard parmi les cellules du
recouvrement de la paire, sans remise, et stockés en coordonnées de tour.
Une cellule peut être le haut d'un escalier vers le niveau inférieur *et* le
bas d'un escalier vers le niveau supérieur ; elle est alors marquée `B`.

La génération est reproductible avec `--seed`, et l'enregistrement
(`--output`) stocke, pour chaque niveau, sa taille, son décalage et ses
`open_walls`, plus la liste des escaliers, de sorte qu'une tour se
reconstruit à l'identique.

## Rendu

Le rendu compact des labyrinthes 2D donne à chaque cellule deux colonnes et
une ligne : un glyphe de coin et le mur nord de la cellule. Les murs
verticaux sont portés par les glyphes de coin, si bien qu'**il n'y a aucun
caractère libre par cellule** où placer un marqueur. Les tours utilisent
donc un style *large* : deux lignes par cellule, l'une pour les murs nord et
les coins, l'autre pour les murs ouest et l'intérieur de la cellule.
L'intérieur fait trois colonnes pour que les cellules paraissent à peu près
carrées en police à chasse fixe, et le marqueur est au centre.

Les glyphes de coin viennent de la même table à 16 entrées que le rendu
compact, les deux styles sont donc cohérents, et le style large sera aussi
proposé pour les labyrinthes 2D (`--style wide`).

Marqueurs : `U` — un escalier monte vers le niveau `i + 1` ; `D` — un
escalier descend vers le niveau `i − 1` ; `B` — les deux.

Les niveaux sont affichés du rez-de-chaussée vers le haut, chacun avec un
titre donnant son indice, sa taille, son décalage par rapport au niveau
inférieur et son nombre d'escaliers. Les niveaux étant décalés, chaque
dessin est **décalé à l'écran selon son origine** (quatre colonnes par
cellule horizontalement, deux lignes par cellule verticalement, par rapport
à l'origine la plus à gauche et la plus haute de la tour), de sorte qu'un
`U` et le `D` qui lui fait face sont imprimés dans la même colonne et à la
même distance du haut de leur dessin. Les escaliers s'apparient ainsi à
l'œil ; une option `--no-align` affiche chaque niveau au ras de la marge.

Exemple, graine 7, `8x5 6x4@1,1:2 4x3@-1,2:1` :

```text
Niveau 0 (8x5) — rez-de-chaussée
┌───────────────┬───┬───────────┐
│               │   │           │
│   ╶───┐   ╷   │   ╵   ┌───────┤
│       │ U │   │       │       │
│   ╷   ├───┘   ├───╴   ╵   ┌───┤
│   │   │       │           │   │
├───┴───┘   ┌───┤   ╶───┐   │   │
│         U │   │       │   │   │
│   ╶───┐   ╵   ╵   ╷   └───┘   │
│       │           │           │
└───────┴───────────┴───────────┘

Niveau 1 (6x4) — décalage (+1, +1) par rapport au niveau 0, 2 escalier(s) vers le bas


    ┌───────────────┬───────┐
    │     D         │       │
    │   ┌───────┬───┘   ╶───┤
    │   │       │           │
    │   ╵   ╶───┘   ╷   ╷   │
    │     D   U     │   │   │
    │   ╶───┐   ╷   ├───┘   │
    │       │   │   │       │
    └───────┴───┴───┴───────┘

Niveau 2 (4x3) — décalage (-1, +2) par rapport au niveau 1, 1 escalier(s) vers le bas






┌───────────────┐
│             D │
│   ╷   ╶───┬───┤
│   │       │   │
│   ├───╴   ╵   │
│   │           │
└───┴───────────┘
```

Le niveau 1 est décalé d'une cellule à droite et d'une vers le bas par
rapport au niveau 0 ; le niveau 2 est d'une cellule à gauche et de deux vers
le bas par rapport au niveau 1, donc de retour en colonne 0 et trois
cellules sous le rez-de-chaussée. Le `D` en haut à droite du niveau 2 fait
face au `U` du niveau 1 juste au-dessus à l'écran.

## Esquisse d'API

```python
from perfect_maze import Cell, Maze


class LevelCell(Cell):
    """Une cellule pouvant porter un escalier."""

    __slots__ = ("up", "down")
    up: bool  # escalier vers le niveau supérieur
    down: bool  # escalier vers le niveau inférieur


@dataclass(frozen=True)
class LevelSpec:
    width: int
    height: int
    offset: tuple[int, int] = (
        0,
        0,
    )  # par rapport au niveau inférieur ; ignoré au niveau 0
    stairs: int = 0  # vers le niveau inférieur ; ignoré au niveau 0


@dataclass
class Tower:
    levels: list[Maze]  # les cellules sont des LevelCell
    origins: tuple[tuple[int, int], ...]  # origine absolue de chaque niveau
    stairs: tuple[
        tuple[int, int, int], ...
    ]  # (niveau inférieur, X, Y) en coordonnées de tour

    def __getitem__(self, lxy: tuple[int, int, int]) -> LevelCell: ...
    def overlap(self, lower: int) -> list[tuple[int, int]]: ...
    def neighbours(self, level, cell) -> Iterator[tuple[int, LevelCell]]: ...


def build_tower(
    specs: Sequence[LevelSpec],
    *,
    randrange=random.randrange,
    stairs: Sequence[tuple[int, int, int]] | None = None,
    open_walls: Sequence[Sequence[OpenWall]] | None = None,
) -> Tower: ...


def printable_tower(
    tower: Tower, *, cell_width: int = 3, align: bool = True
) -> str: ...
def printable_maze(
    maze,
    *,
    style: Literal["compact", "wide"] = "compact",
    cell_char: Callable[[Cell], str] | None = None,
) -> str: ...
```

`build_tower` tire, par le même `randrange` que les niveaux, les positions
des escaliers comme des indices dans la liste du recouvrement : une tour
avec graine est reproductible et le mécanisme d'enregistrement/rejeu
s'étend naturellement.

## Ligne de commande

Le générateur 2D garde son interface actuelle ; les tours ont une
sous-commande :

```text
$ perfect-maze levels
Number of levels [2]: 3
Level 0 width [6]: 8
Level 0 height [4]: 5
Level 1 width [6]: 6
Level 1 height [4]: 4
Level 1 offset from level 0 (dx, dy) [0, 0]: 1, 1
Stairs down to level 0 (1-15) [1]: 2
Level 2 width [6]: 4
Level 2 height [4]: 3
Level 2 offset from level 1 (dx, dy) [0, 0]: -1, 2
Stairs down to level 1 (1-8) [1]:

Level 0 (8x5) — ground
...
```

Les invites de l'outil sont en anglais, comme le reste de l'interface en
ligne de commande. Options : `--seed N`, `--output PATH` (enregistrement),
`--quiet`, `--no-align`, et les spécifications positionnelles
`LARGEURxHAUTEUR[@DX,DY][:ESCALIERS]` qui court-circuitent les invites.
Quand l'entrée standard n'est pas un terminal et qu'aucune spécification
n'est donnée, la commande échoue avec une erreur d'usage plutôt que
d'attendre une saisie.

## Tests

- Chaque niveau d'une tour générée est parfait (réutilisation du test de
  propriétés 2D).
- Les origines sont les sommes cumulées des décalages ; `overlap()` est
  l'intersection exacte des rectangles, y compris avec des décalages
  négatifs et un niveau entièrement inclus dans le précédent ou plus grand
  que lui.
- Exactement `k_i` escaliers entre les niveaux `i − 1` et `i`, tous dans le
  recouvrement, sans doublon ; un décalage sans recouvrement est refusé.
- Les drapeaux `up`/`down` correspondent à la liste des escaliers ; une
  cellule `B` a les deux.
- Une tour dont tous les `k_i = 1` est globalement parfaite (BFS à travers
  les niveaux, `n − 1` passages au total) ; une tour avec des `k_i ≥ 2` est
  connexe et a exactement `Σ (k_i − 1)` passages supplémentaires.
- Même graine ⇒ même tour ; une tour enregistrée se reconstruit à
  l'identique.
- Rendu large : dimensions `(cell_width + 1)·w + 1` colonnes sur `2h + 1`
  lignes, marqueurs aux positions attendues, fixtures d'une petite tour.
- Rendu aligné : un `U` et son `D` sont sur la même colonne et à la même
  distance du haut de leur niveau, pour des décalages positifs et négatifs.
- Analyse des spécifications (`8x5`, `6x4@1,1:2`, `4x3@-1,2`, erreurs) et
  invites pilotées par un `input()` scripté, y compris la nouvelle invite
  sur valeur invalide, sur décalage sans recouvrement, et la borne
  supérieure de `k`.

## Plan de patchs

1. `feat(render)` : style large et crochet `cell_char` de `printable_maze`,
   avec fixtures. Indépendant des tours, utilisable seul.
2. `feat(tower)` : `LevelCell`, `LevelSpec` (avec décalage), `Tower` avec
   origines et `overlap()`, `build_tower`, tests de structure et de
   reproductibilité.
3. `feat(render)` : `printable_tower`, sortie alignée et au ras de la marge.
4. `feat(cli)` : sous-commande `perfect-maze levels`, invites (dont le
   décalage), analyse des spécifications, enregistrement.
5. `docs` : transformer cette page en documentation utilisateur ; changelog
   `1.1.0`.

## Questions ouvertes

1. Ordre d'affichage : rez-de-chaussée en premier (comme ci-dessus) ou
   dernier niveau en premier ?
2. Une cellule d'escalier peut-elle être `B`, ou les deux paires
   doivent-elles tirer dans des cellules disjointes ? (`B` est autorisé dans
   cette conception.)
3. Largeur intérieure du style large : 3 colonnes (proposé) ou 1 pour les
   très grands niveaux ?
4. Les décalages sont relatifs au niveau inférieur, comme demandé. Le
   fichier d'enregistrement doit-il aussi stocker les origines absolues par
   commodité ?
5. Vocabulaire : *tour*, *niveaux* et *escaliers* sont utilisés ici ;
   *étages* et *échelles* sont des alternatives.
