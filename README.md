# Chunkbased
Chunkbased (https://github.com/ZodiacHide/Chunkbased) by https://github.com/ZodiacHide is a gamemode inspired by https://www.youtube.com/@Settledrs and his Old School RuneScape series *Tileman* featuring McTile as the protagonist.
The game mode restricts the player to one chunk, a 16 by 16 block area, at a time and only allows the player to move to a new chunk after a condition set by the player has been met.

This ``Python`` project is not meant to physically restrict the player's movement in the game, but instead give the player a clear framework for which they can play the gamemode.

## Chunkbased is currently in development
### Planned features
- A method to keep track of locked and unlocked chunks
- A method to unlock chunks
- Minimap window showing player's position, locked and unlocked chunks
- A visual or auditory warning telling the player they are inside a locked chunk

#### If possible
- A method to keep track of player's progress to unlock a new chunk

## Known issues
- Incompatible with most game window resolution and aspect ratios different from 2576x1426, equivelant to playing the largest windowed size for a 2560x1440 monitor
- Incorrect player position
- Slow player position updates
