# Slay the Dragon

A 2D platformer built in Python with the cmu_graphics library. Explore 9 connected rooms, collect coins, buy upgrades from a shop, and take on a dragon boss.

## Demo
https://www.youtube.com/watch?v=Ki1LRtSlPo0 

## Gameplay
- Explore 9 interconnected rooms with unique platform layouts, spikes, and hazards.
- Collect 20 coins scattered across the map.
- Spend coins on 4 upgrades in the shop (max HP, damage, speed, attack speed).
- Fight a dragon boss with a multi-phase attack pattern, then watch the victory sequence.

## Controls
| Key | Action |
|-----|--------|
| A / D | Move left / right |
| Space | Jump |
| I | Attack 1 |
| O | Attack 2 |
| E | Enter / exit the shop door |
| F | Open the shopkeeper menu |
| Arrow keys + Enter | Navigate and buy upgrades |
| R | Restart after death or victory |

## How to play
Start in the center room and explore using A/D and Space. Collect coins in the left, right, and bottom rooms, then head far left and enter the shop (E near the door, then F by the shopkeeper). Buy upgrades, then go to the top room to trigger the boss fight. Use I and O to attack; press R to restart after winning or dying.

## Debug shortcuts
| Key | Effect |
|-----|--------|
| 1 | Set dragon HP to 2 (boss room only) |
| 2 | Give 40 coins |
| 3 | Teleport to the shop |
| 4 | Jump to the boss with all upgrades |

## Technical notes
- **Animation system** — sprite-based, with 7 knight states (idle, walk, jump, two attacks, hurt, death) and 5 dragon states. Frames cycle on a timer with state-based transitions, and sprites are flipped for left/right facing.
- **Physics** — custom gravity and jump arc, with platform collision handling for landing, head bumps, and side walls.
- **Boss fight** — the dragon patrols, throws projectiles on specific attack frames, and only attacks when facing the player. Includes player invulnerability frames and knockback on hit.
- **Rooms** — each room defines its own platforms, spikes, and coins; transitions trigger at screen edges.

## Built with
Python · cmu_graphics

## Notes
A good chunk of the work was learning the sprite pipeline: downloading sprite sheets, extracting them from zip/rar archives, slicing individual frames, flipping them for directional facing, and managing the upload of correctly-sized assets to a separate media repo.
