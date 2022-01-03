# perfect_maze
A simple python script to create perfect maze (a maze without dead cells and with all connected cells).
Create maze wich can be print in utf-8, for exemple :
┌─┬───────┬───┬─────┬─────────────────────┬───┬───┬─────┬─┬─────────┬───────┬───┬───┬─┬─┬─────┬───┬───────┬─────────┬───┐
│ └─────┐ ╵ ╶─┘ ╷ ┌─┴─┐ ╷ ┌─┐ ┌─╴ ╷ ╶─┬───┘ ╷ ╵ ╷ ╵ ╶─┐ ╵ └─╴ ┌─┬─┬─┘ ┌─╴ ╶─┼─╴ ├─┐ ╵ │ ├─┐ ┌─┤ ╷ └─┬─╴ ╶─┤ ╶─┬───┐ │ ╶─┤
├───╴ ╷ ╵ ╶─┬─╴ └─┴─╴ │ │ ╵ ├─┼───┴───┼─┐ ╶─┼───┴─┬───┘ ╷ ┌─╴ │ ╵ ╵ ╷ ├───┬─┘ ╶─┤ │ ╷ ╵ ╵ ╵ ╵ ├─┘ ╶─┼─┐ ╶─┼───┘ ╶─┘ ╵ ╷ │
├─┐ ┌─┤ ╶─┬─┴─┐ ╶─┬─┐ ╵ │ ╶─┤ ├─╴ ╶─┬─┘ └─┬─┼─╴ ╶─┘ ╶─┬─┴─┤ ╷ ├─────┤ ╵ ╶─┴───╴ ╵ ├─┤ ╶───┬─╴ ╵ ╷ ╷ │ └─╴ └─┐ ┌─┐ ╶─┐ │ │
│ ├─┘ ╵ ┌─┘ ╷ └───┘ ╵ ┌─┤ ╶─┤ └───╴ ╵ ╷ ╶─┘ │ ┌─╴ ╶─┐ │ ╶─┤ │ ╵ ╶─┐ └─┬─╴ ╶─┬─┐ ┌─┘ │ ╷ ╶─┤ ┌─╴ └─┼─┘ ╷ ╷ ┌─┤ ╵ └───┤ │ │
│ └─┐ ╷ ├─┬─┴─╴ ╶─┬───┤ ├─╴ ╵ ╶─┬───╴ │ ╷ ╷ ├─┴───┬─┴─┴─╴ ├─┴─╴ ┌─┤ ╶─┘ ┌───┤ ╵ │ ╷ │ ├─╴ └─┼─┐ ╷ │ ╷ │ └─┤ ╵ ╷ ┌─╴ └─┴─┤
│ ╶─┤ └─┤ └─╴ ╷ ╶─┤ ╶─┘ └─┐ ╷ ╶─┤ ╷ ╶─┼─┴─┤ ├─┬─╴ ╵ ╷ ╶───┘ ┌───┘ ├─┬─╴ ├─╴ ╵ ╷ │ └─┴─┤ ╶─┐ │ ╵ └─┼─┤ │ ╶─┤ ╷ ├─┘ ╷ ┌───┤
│ ╷ ╵ ┌─┼─┐ ╶─┴─┐ │ ╷ ╷ ╷ ╵ ├─╴ ├─┘ ╷ │ ╷ ├─┤ ├─╴ ╶─┤ ┌───┬─┤ ╷ ╶─┘ ├─╴ ├─────┴─┴───╴ ╵ ╷ └─┤ ┌─╴ ╵ │ ├─╴ ╵ │ ├─┐ ├─┘ ╷ │
├─┘ ┌─┤ ╵ ╵ ╶───┼─┘ ├─┘ └─┬─┘ ╷ ├─╴ ├─┘ │ │ ╵ └─╴ ╷ ├─┴─╴ │ └─┘ ╷ ┌─┘ ┌─┘ ┌─╴ ╷ ╷ ╷ ┌───┴───┤ │ ┌─╴ └─┤ ┌───┼─┘ ╵ ├─┬─┘ │
│ ╶─┤ ├─┐ ╷ ┌─╴ ├───┼─┐ ╷ ├─╴ ├─┴─┬─┼─╴ ├─┼───┬─╴ │ └───╴ │ ┌─┬─┴─┤ ╶─┼─┬─┘ ╷ ├─┴─┤ ├───┬─╴ └─┘ └─┬─╴ ├─┤ ┌─┴─╴ ┌─┘ ├─┐ │
│ ╷ │ │ ╵ ├─┴─┐ ├─╴ ╵ │ └─┴─┬─┼─╴ ╵ ╵ ╶─┘ └─╴ ╵ ┌─┘ ┌─┐ ╶─┘ ╵ │ ╷ │ ┌─┘ ╵ ┌─┼─┴─┐ └─┘ ╷ ╵ ╶───┬─┬─┴─┬─┘ │ ├─╴ ┌─┼─┐ ╵ ╵ │
│ │ │ └─┬─┤ ╷ │ ├─╴ ╷ └─┐ ╶─┤ ╵ ╶─┐ ┌─┐ ┌─┬─┬─┐ │ ╷ ╵ └─┐ ┌─╴ │ └─┼─┘ ╷ ╶─┤ ╵ ╷ ├─╴ ┌─┘ ┌───┐ ╵ ╵ ╷ │ ╶─┘ ╵ ╷ │ ╵ ├───╴ │
├─┼─┴─╴ │ │ ├─┘ ├───┘ ┌─┼───┤ ╷ ┌─┼─┘ │ │ ╵ │ ╵ ├─┴─╴ ┌─┼─┴─╴ └─┐ │ ╷ ├─╴ ╵ ╶─┼─┴───┤ ┌─┘ ╶─┘ ╷ ┌─┘ ╵ ╶─┐ ╷ └─┘ ╶─┤ ╶─┐ │
│ ╵ ╷ ╷ │ ╵ ╵ ╷ ╵ ┌─╴ │ ╵ ╷ ├─┘ ╵ │ ╷ │ ├─╴ │ ╶─┤ ┌─┐ │ ├─┐ ╷ ╷ ╵ └─┤ └─┬─╴ ┌─┴─┐ ╶─┴─┘ ┌─╴ ╷ ├─┘ ┌───╴ └─┼─╴ ╶─┬─┤ ┌─┤ │
│ ╶─┤ └─┼─┐ ┌─┴─┐ ├───┴───┘ ├─╴ ╷ ╵ ├─┤ ├─╴ └───┼─┘ ╵ ╵ ╵ ├─┴─┤ ╷ ╷ │ ┌─┴─┬─┼─╴ ╵ ╶─┬─┬─┘ ╶─┼─┴─┬─┼───╴ ╶─┤ ╷ ╷ ╵ │ ╵ │ │
├───┤ ╶─┘ ╵ ╵ ╶─┼─┼─╴ ╶─┬───┼─┐ └───┤ ├─┘ ╷ ╶─┬─┼─┬───┐ ╶─┤ ╶─┼─┴─┤ │ │ ╶─┘ │ ┌─╴ ┌─┤ ╵ ┌─┐ └─╴ ╵ └─┬─┐ ╷ └─┴─┴─┐ └─╴ ├─┤
│ ╷ └───┐ ╶─────┘ └─╴ ┌─┴─╴ ╵ ├─╴ ╷ │ └───┘ ╶─┘ ╵ └─╴ ├─┬─┘ ┌─┤ ╶─┘ ╵ ╵ ┌─╴ │ ├─┬─┘ ├───┤ └─╴ ┌─╴ ╶─┘ ├─┴─┐ ╶─┐ └───┐ ╵ │
├─┼─┐ ╷ │ ╶─┐ ┌─┬─╴ ┌─┤ ╶───┬─┘ ╶─┼─┴─╴ ╶─────┬─┬─╴ ╶─┤ └─╴ ╵ ├───╴ ┌───┴───┴─┤ │ ╷ ├─┐ ╵ ╶─┬─┴─╴ ┌───┤ ╶─┴─╴ ├─────┴───┤
│ ╵ └─┤ └─┐ └─┘ ├─╴ │ │ ╷ ╶─┴─┐ ╶─┘ ╷ ┌─╴ ┌─╴ │ └─╴ ┌─┼─────╴ └─╴ ┌─┘ ┌─┬─╴ ┌─┘ ╵ ├─┤ ╵ ╶─┐ ├───┬─┤ ╶─┼─┐ ╶───┤ ┌─┐ ╶─┐ │
│ ┌─┐ │ ╶─┼─┐ ╶─┤ ╷ ╵ ╵ │ ╶───┼───╴ └─┼─╴ │ ┌─┴─┐ ╷ │ │ ╷ ╷ ┌─┬─╴ │ ╶─┤ ╵ ╷ │ ╶─┐ │ └───┬─┤ ╵ ┌─┘ ╵ ╷ ╵ ╵ ╶─┐ ╵ │ └─┬─┤ │
├─┘ │ └─┐ ╵ ╵ ╷ ├─┴───┐ ├─┐ ╷ │ ╶─┐ ╶─┼───┼─┴─┐ └─┤ ╵ └─┴─┼─┤ ├───┘ ╷ ├─╴ │ ├───┘ ╵ ╷ ┌─┘ │ ╶─┤ ╷ ┌─┼─┬─╴ ╷ └─┐ ╵ ╶─┘ │ │
│ ╶─┴─╴ │ ╶─┬─┘ │ ┌─╴ └─┘ ╵ │ ╵ ╷ └─┬─┴─╴ ╵ ╷ │ ╶─┤ ┌─┐ ╷ ╵ ╵ ├─╴ ┌─┤ └─┐ │ ├───╴ ┌─┤ ╵ ╶─┴───┼─┤ │ ╵ └─╴ └───┤ ┌───╴ └─┤
│ ╷ ╷ ╶─┴─╴ ├─┐ │ └─┐ ╶─┐ ╶─┴───┼─╴ │ ┌─╴ ╷ └─┤ ╶─┘ │ ├─┼─╴ ╷ ╵ ╶─┘ └─┬─┤ ├─┼─╴ ╶─┘ │ ╶───┬───┘ ├─┴─┐ ┌─┐ ╶───┴─┼─────┐ │
├─┴─┤ ╷ ╷ ╷ ╵ │ │ ╶─┴─┬─┴─┬─╴ ╷ └───┤ │ ╷ │ ┌─┴───╴ ╵ │ ╵ ╷ └───┐ ╶─┐ │ ├─┘ │ ╷ ╶─┐ └─────┴─┬─┐ │ ╷ └─┤ ╵ ╷ ╶───┼─╴ ╷ ╵ │
│ ┌─┤ └─┴─┤ ╷ │ │ ┌───┴─┐ └─┐ │ ╷ ╶─┼─┼─┘ └─┘ ┌─────╴ ├─┬─┴─╴ ┌─┘ ╷ ├─┘ │ ╷ └─┴───┘ ╶─┬─╴ ╷ │ ╵ └─┘ ┌─┼─╴ ├───┐ └───┴───┤
│ ╵ ╵ ┌─╴ │ ├─┴─┼─┘ ╶─┬─┤ ╶─┴─┘ ├─┐ │ ╵ ╷ ╷ ╶─┼───╴ ╶─┤ ╵ ╶───┤ ╶─┴─┴─┐ ╵ ├─┐ ╶───┬─┐ ├─┐ │ ├─╴ ┌─╴ ╵ │ ╶─┘ ┌─┘ ┌───╴ ╷ │
├───╴ │ ╷ ├─┴─╴ │ ╷ ┌─┘ ╵ ┌─╴ ╷ ╵ ├─┴───┤ ├───┤ ╶───┬─┘ ┌─┬─┐ │ ┌───┐ │ ┌─┘ └─╴ ╶─┘ │ ╵ │ │ └─╴ ├─╴ ╶─┴───┐ │ ╷ └─┐ ┌─┘ │
├─┐ ╶─┤ ├─┼─╴ ╷ ╵ │ └─────┴─┬─┴─┐ │ ╷ ╶─┘ │ ┌─┤ ┌─┬─┤ ┌─┤ ╵ ╵ └─┘ ╷ └─┴─┼─╴ ╷ ╶─┐ ╶─┴─┐ └─┴─┐ ╶─┴─┐ ╷ ╷ ╶─┼─┤ └───┤ └─┐ │
│ ╵ ╶─┴─┤ │ ┌─┼─┐ │ ┌─┐ ┌───┤ ╷ │ │ ├─╴ ╶─┘ ╵ ├─┤ ╵ ╵ ╵ ├─╴ ╷ ╶─┬─┘ ╶─┬─┼─╴ ├─╴ │ ╷ ╶─┤ ╶─┐ │ ╶───┼─┴─┴─┬─┘ ╵ ┌─╴ ├───┴─┤
│ ╷ ╶─┐ │ ╵ │ ╵ └─┼─┘ ├─┘ ╶─┘ ├─┤ └─┤ ┌───╴ ╶─┤ │ ╶─┬─╴ │ ╶─┼───┴───┐ ╵ ├─┬─┼─┐ │ ├───┴─┬─┤ ├───┐ ╵ ╶───┴─┬─┬─┘ ╶─┼─┬─╴ │
│ │ ┌─┼─┘ ╷ ╵ ┌───┘ ╷ ├─┐ ╶───┤ │ ╷ └─┤ ╷ ╶─┬─┘ ├───┘ ╶─┼───┴─┐ ╷ ╶─┴─┐ ╵ │ ╵ └─┼─┘ ┌─┐ ╵ └─┘ ╷ ├───┬─┐ ╶─┘ │ ╶─┬─┘ ╵ ╶─┤
├─┘ │ ├─┬─┼─┐ ╵ ╷ ┌─┴─┤ ╵ ┌─╴ ╵ ├─┴───┴─┼───┘ ╶─┴─────╴ │ ╷ ╶─┴─┴─╴ ╶─┤ ╶─┴─┐ ╷ ╵ ┌─┘ ╵ ╶─┐ ╶─┼─┘ ╷ ╵ └─╴ ┌─┴─┐ ╵ ╶───┬─┤
├─╴ ╵ ╵ │ │ ╵ ╶─┼─┘ ╷ ├───┴─╴ ╶─┤ ╶─┬───┘ ┌─┬─╴ ┌───┐ ╶─┘ │ ┌─┬─┬───┐ ├─┐ ╷ ├─┘ ╶─┴─┬───┬─┤ ╷ │ ╷ │ ╷ ╷ ╷ └─╴ ╵ ╶───┬─┤ │
│ ╶─┐ ╷ ╵ ╵ ╶─┬─┘ ╶─┤ ├─╴ ╶─┬─┐ │ ┌─┴─┬─┐ │ ╵ ╶─┤ ╷ ├─┐ ╶─┤ │ ╵ └─╴ ╵ ╵ ├─┼─┼─┐ ╷ ╶─┴─┐ │ │ └─┴─┴─┼─┴─┘ ├─┐ ╷ ╶─┐ ╷ │ ╵ │
│ ╷ ├─┴─╴ ╶─┬─┤ ┌───┴─┴─╴ ╷ │ │ ╵ └─╴ │ │ └─┬───┼─┘ │ ╵ ╶─┼─┼─┐ ┌───╴ ╷ ╵ │ ╵ ╵ │ ╷ ┌─┘ ╵ ├─╴ ┌───┴─╴ ╶─┤ └─┴─┬─┘ │ ╵ ╷ │
├─┘ │ ╷ ╷ ╶─┤ ╵ ╵ ╶─┐ ┌───┼─┤ ╵ ╷ ╷ ╷ ╵ │ ╷ ╵ ┌─┘ ┌─┤ ╶─┬─┘ ╵ ├─┤ ┌───┤ ╶─┴─┬─╴ │ │ ├─┬─╴ ╵ ╶─┤ ┌─┬───╴ │ ╷ ╶─┼─┐ ├─╴ └─┤
│ ╶─┼─┴─┴─╴ ╵ ╷ ╶───┤ │ ┌─┘ ├───┴─┴─┤ ┌─┤ └─┐ ╵ ╶─┤ └─┐ │ ╷ ┌─┤ ╵ ╵ ╶─┤ ╷ ╶─┤ ╷ ├─┘ │ └───╴ ┌─┘ │ └─┐ ╷ ╵ │ ╶─┘ │ ├───╴ │
│ ┌─┘ ╶─┐ ╷ ╷ ├─╴ ┌─┴─┘ └─╴ │ ╶─┬─╴ ╵ │ ╵ ┌─┘ ┌───┘ ╷ └─┤ │ ╵ └─╴ ┌───┴─┘ ┌─┴─┴─┘ ╷ ├───┬─┐ └─╴ └─┐ ╵ └───┤ ╷ ┌─┴─┤ ╶───┤
├─┘ ┌───┴─┼─┴─┘ ╷ ╵ ┌───╴ ╷ └─┬─┼───╴ ├─╴ ├─╴ ├─┐ ┌─┴─╴ ├─┴─┐ ╶─┬─┴─╴ ╷ ╷ ├───╴ ╶─┴─┘ ╷ ╵ ├─┬─────┼─╴ ╶─┐ ├─┴─┼─╴ │ ╶─┬─┤
│ ╶─┘ ┌───┴─╴ ╶─┴─┬─┘ ╷ ┌─┴───┘ ╵ ╷ ╶─┤ ┌─┴─╴ │ ╵ │ ╶─┐ └─╴ └─╴ │ ╶─┐ │ ├─┘ ╶───┐ ╷ ╷ │ ╶─┘ ╵ ╶─┐ │ ╷ ╶─┴─┤ ╷ ╵ ╶─┘ ╶─┘ │
└─────┴───────────┴───┴─┴─────────┴───┴─┴─────┴───┴───┴─────────┴───┴─┴─┴───────┴─┴─┴─┴─────────┴─┴─┴─────┴─┴───────────┘
