# Knight Adventure - Slay the Dragon Lord

An HTML5 Canvas-based action-adventure game featuring a brave knight on a quest to defeat the Dragon Lord!

## Features

### Animated Character System
- **Knight Hero** with full sprite animations:
  - Idle, Walk, Run animations
  - 3-hit attack combo system
  - Defend stance with damage reduction
  - Hurt and death animations
  - Jump animation

### Dragon Lord Boss
- **Fully animated final boss** with:
  - Idle and walk animations
  - Attack animations with area damage
  - Hurt reactions
  - Death animation
  - AI-controlled behavior (chases player, attacks when close)
  - Health bar display

### Multiple Rooms
1. **Starting Chamber** - Tutorial area with collectibles
2. **Dark Dungeon** - Corridor filled with treasures and dangers
3. **Dragon Lord's Lair** - Epic boss battle arena

### Interactive Elements
- **Collectible Coins** - Gold and blue coins to gather
- **Health Potions** - 6 different types to restore HP
- **Dungeon Decorations** - Torches, structures, and environmental objects
- **Animated Environment** - Stone floors, dungeon sets, and atmospheric elements

### Game Systems
- **Health System** - Take damage, heal with potions, defend to reduce damage
- **Combat System** - Combo attacks, hitboxes, invulnerability frames
- **Camera System** - Smooth scrolling that follows the player
- **Room Transitions** - Move between different areas via doors
- **Collision Detection** - Interact with objects and enemies

## Controls

| Key | Action |
|-----|--------|
| **W / Arrow Up** | Move Up (in menus) |
| **A / Arrow Left** | Move Left |
| **S / Arrow Down** | Move Down (in menus) |
| **D / Arrow Right** | Move Right |
| **SPACE** | Attack (3-hit combo) |
| **SHIFT** | Run / Defend |
| **E** | Interact with doors / Use potion |

## How to Play

1. **Open `index.html`** in a modern web browser (Chrome, Firefox, Edge, Safari)
2. **Explore the rooms** and collect coins and potions
3. **Fight your way** through the dungeon to reach the Dragon Lord
4. **Defeat the Dragon Lord** to win the game!

### Tips
- Collect potions before facing the Dragon Lord
- Use the Defend stance (SHIFT) to reduce incoming damage
- Time your attacks carefully - the 3-hit combo deals more damage
- The Dragon Lord is tough - use hit-and-run tactics!
- Press E when you have potions to heal (when not near a door)

## Game Structure

```
├── index.html          # Main HTML file
├── styles.css          # Game styling and UI
├── game.js            # Complete game engine
├── Sprites/           # Knight character sprite sheets
├── END_USER_DRAGON_LORD_BASIC/ # Dragon Lord boss sprites
├── Dungeon Gathering Free Version/ # Environment and items
└── environment/       # Ground tiles and backgrounds
```

## Technical Details

- **Engine**: Custom HTML5 Canvas game engine
- **Animation System**: Sprite sheet animation with configurable FPS
- **Resolution**: 1200x700 pixels
- **Art Style**: Pixel art with outline
- **Performance**: Optimized delta-time game loop

## Credits

All sprite assets and artwork are used with proper licensing from their respective creators.

---

**Have fun slaying the Dragon Lord!** 🗡️🐉
