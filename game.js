// Game Configuration
const CONFIG = {
    canvas: null,
    ctx: null,
    width: 1200,
    height: 700,
    tileSize: 32,
    playerSpeed: 3,
    playerRunSpeed: 5,
    gravity: 0.8,
    jumpForce: 15
};

// Game State
const gameState = {
    currentRoom: 'start',
    playerHealth: 100,
    maxHealth: 100,
    coins: 0,
    potions: 0,
    gameOver: false,
    victory: false,
    camera: { x: 0, y: 0 }
};

// Input Handler
const keys = {};
const input = {
    left: false,
    right: false,
    up: false,
    down: false,
    attack: false,
    defend: false,
    interact: false,
    run: false
};

// Sprite Animation System
class SpriteAnimation {
    constructor(imagePath, frameWidth, frameHeight, frameCount, fps = 10) {
        this.image = new Image();
        this.image.src = imagePath;
        this.frameWidth = frameWidth;
        this.frameHeight = frameHeight;
        this.frameCount = frameCount;
        this.fps = fps;
        this.currentFrame = 0;
        this.frameTimer = 0;
        this.loaded = false;
        this.image.onload = () => { this.loaded = true; };
    }

    update(deltaTime) {
        this.frameTimer += deltaTime;
        if (this.frameTimer >= 1000 / this.fps) {
            this.currentFrame = (this.currentFrame + 1) % this.frameCount;
            this.frameTimer = 0;
        }
    }

    draw(ctx, x, y, scale = 1, flipX = false) {
        if (!this.loaded) return;

        ctx.save();
        if (flipX) {
            ctx.scale(-1, 1);
            x = -x - this.frameWidth * scale;
        }

        ctx.drawImage(
            this.image,
            this.currentFrame * this.frameWidth,
            0,
            this.frameWidth,
            this.frameHeight,
            x,
            y,
            this.frameWidth * scale,
            this.frameHeight * scale
        );
        ctx.restore();
    }

    reset() {
        this.currentFrame = 0;
        this.frameTimer = 0;
    }
}

// Player Class
class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 64;
        this.height = 64;
        this.velocityX = 0;
        this.velocityY = 0;
        this.facingRight = true;
        this.onGround = false;
        this.scale = 2;

        // Animation states
        this.currentState = 'IDLE';
        this.animations = {
            'IDLE': new SpriteAnimation('Sprites/with_outline/IDLE.png', 64, 64, 10, 8),
            'WALK': new SpriteAnimation('Sprites/with_outline/WALK.png', 64, 64, 8, 10),
            'RUN': new SpriteAnimation('Sprites/with_outline/RUN.png', 64, 64, 8, 12),
            'JUMP': new SpriteAnimation('Sprites/with_outline/JUMP.png', 64, 64, 3, 8),
            'ATTACK1': new SpriteAnimation('Sprites/with_outline/ATTACK 1.png', 64, 64, 4, 12),
            'ATTACK2': new SpriteAnimation('Sprites/with_outline/ATTACK 2.png', 64, 64, 4, 12),
            'ATTACK3': new SpriteAnimation('Sprites/with_outline/ATTACK 3.png', 64, 64, 4, 12),
            'DEFEND': new SpriteAnimation('Sprites/with_outline/DEFEND.png', 64, 64, 2, 6),
            'HURT': new SpriteAnimation('Sprites/with_outline/HURT.png', 64, 64, 2, 8),
            'DEATH': new SpriteAnimation('Sprites/with_outline/DEATH.png', 64, 64, 10, 8)
        };

        this.attackCombo = 0;
        this.attackCooldown = 0;
        this.isAttacking = false;
        this.isDefending = false;
        this.isHurt = false;
        this.invulnerable = false;
        this.invulnerableTimer = 0;
    }

    update(deltaTime) {
        // Update invulnerability
        if (this.invulnerable) {
            this.invulnerableTimer -= deltaTime;
            if (this.invulnerableTimer <= 0) {
                this.invulnerable = false;
            }
        }

        // Attack cooldown
        if (this.attackCooldown > 0) {
            this.attackCooldown -= deltaTime;
            if (this.attackCooldown <= 0) {
                this.isAttacking = false;
                this.attackCombo = 0;
            }
        }

        // Handle input and movement
        if (!this.isAttacking && !this.isHurt && gameState.playerHealth > 0) {
            this.velocityX = 0;

            if (input.defend) {
                this.isDefending = true;
                this.currentState = 'DEFEND';
            } else {
                this.isDefending = false;

                if (input.left) {
                    this.velocityX = input.run ? -CONFIG.playerRunSpeed : -CONFIG.playerSpeed;
                    this.facingRight = false;
                }
                if (input.right) {
                    this.velocityX = input.run ? CONFIG.playerRunSpeed : CONFIG.playerSpeed;
                    this.facingRight = true;
                }

                if (input.attack && this.attackCooldown <= 0) {
                    this.isAttacking = true;
                    this.attackCooldown = 500;
                    this.attackCombo = (this.attackCombo + 1) % 3;
                    this.currentState = 'ATTACK' + (this.attackCombo + 1);
                    this.animations[this.currentState].reset();
                } else if (this.velocityX !== 0) {
                    this.currentState = input.run ? 'RUN' : 'WALK';
                } else if (!this.onGround) {
                    this.currentState = 'JUMP';
                } else {
                    this.currentState = 'IDLE';
                }
            }
        }

        if (gameState.playerHealth <= 0 && this.currentState !== 'DEATH') {
            this.currentState = 'DEATH';
            this.animations.DEATH.reset();
        }

        // Apply movement
        this.x += this.velocityX;

        // Boundary checking
        const room = rooms[gameState.currentRoom];
        if (this.x < 50) this.x = 50;
        if (this.x > room.width - 100) this.x = room.width - 100;

        // Keep player grounded
        this.y = CONFIG.height - 200;
        this.onGround = true;

        // Update current animation
        this.animations[this.currentState].update(deltaTime);
    }

    draw(ctx) {
        const anim = this.animations[this.currentState];
        const drawX = this.x - gameState.camera.x;
        const drawY = this.y - gameState.camera.y;

        // Flash when invulnerable
        if (this.invulnerable && Math.floor(Date.now() / 100) % 2 === 0) {
            ctx.globalAlpha = 0.5;
        }

        anim.draw(ctx, drawX, drawY, this.scale, !this.facingRight);
        ctx.globalAlpha = 1;

        // Draw hitbox for debugging
        // ctx.strokeStyle = 'red';
        // ctx.strokeRect(drawX, drawY, this.width * this.scale, this.height * this.scale);
    }

    getHitbox() {
        return {
            x: this.x,
            y: this.y,
            width: this.width * this.scale,
            height: this.height * this.scale
        };
    }

    takeDamage(amount) {
        if (this.invulnerable || this.isDefending) {
            if (this.isDefending) {
                amount = Math.floor(amount * 0.3); // 70% damage reduction when defending
            } else {
                return;
            }
        }

        gameState.playerHealth -= amount;
        if (gameState.playerHealth < 0) gameState.playerHealth = 0;

        if (gameState.playerHealth > 0) {
            this.isHurt = true;
            this.currentState = 'HURT';
            this.animations.HURT.reset();
            this.invulnerable = true;
            this.invulnerableTimer = 1000;

            setTimeout(() => {
                this.isHurt = false;
            }, 300);
        }

        updateHealthBar();
    }

    heal(amount) {
        gameState.playerHealth += amount;
        if (gameState.playerHealth > gameState.maxHealth) {
            gameState.playerHealth = gameState.maxHealth;
        }
        updateHealthBar();
    }

    getAttackHitbox() {
        if (!this.isAttacking) return null;

        return {
            x: this.facingRight ? this.x + this.width * this.scale : this.x - 80,
            y: this.y,
            width: 80,
            height: this.height * this.scale
        };
    }
}

// Dragon Lord Boss
class DragonLord {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 74;
        this.height = 74;
        this.scale = 3;
        this.health = 300;
        this.maxHealth = 300;
        this.facingRight = false;
        this.currentState = 'idle';

        this.animations = {
            'idle': new SpriteAnimation('END_USER_DRAGON_LORD_BASIC/Spritesheets/dragon_lord_idle_basic_74x74.png', 74, 74, 4, 6),
            'walk': new SpriteAnimation('END_USER_DRAGON_LORD_BASIC/Spritesheets/dragon_lord_walk_basic_74x74.png', 74, 74, 8, 8),
            'attack': new SpriteAnimation('END_USER_DRAGON_LORD_BASIC/Spritesheets/dragon_lord_attack_arms_90x70.png', 90, 70, 12, 10),
            'hurt': new SpriteAnimation('END_USER_DRAGON_LORD_BASIC/Spritesheets/dragon_lord_hurt_basic_130x130.png', 130, 130, 3, 8),
            'death': new SpriteAnimation('END_USER_DRAGON_LORD_BASIC/Spritesheets/dragon_lord_death_160x160.png', 160, 160, 9, 8)
        };

        this.velocityX = 0;
        this.aiState = 'idle';
        this.aiTimer = 0;
        this.attackCooldown = 0;
        this.isAttacking = false;
        this.isDead = false;
        this.invulnerable = false;
        this.invulnerableTimer = 0;
    }

    update(deltaTime, player) {
        if (this.isDead) {
            this.animations.death.update(deltaTime);
            return;
        }

        if (this.invulnerable) {
            this.invulnerableTimer -= deltaTime;
            if (this.invulnerableTimer <= 0) {
                this.invulnerable = false;
            }
        }

        this.aiTimer += deltaTime;
        this.attackCooldown -= deltaTime;

        // AI Behavior
        const distToPlayer = Math.abs(this.x - player.x);

        if (this.attackCooldown <= 0 && distToPlayer < 150) {
            // Attack
            this.isAttacking = true;
            this.currentState = 'attack';
            this.attackCooldown = 2000;
            this.aiState = 'attack';
            this.animations.attack.reset();

            // Deal damage to player after animation starts
            setTimeout(() => {
                if (this.checkAttackHit(player)) {
                    player.takeDamage(15);
                }
            }, 400);

        } else if (distToPlayer > 100 && !this.isAttacking) {
            // Move towards player
            this.currentState = 'walk';
            this.aiState = 'chase';

            if (this.x < player.x) {
                this.velocityX = 1.5;
                this.facingRight = true;
            } else {
                this.velocityX = -1.5;
                this.facingRight = false;
            }

            this.x += this.velocityX;
        } else if (!this.isAttacking) {
            this.currentState = 'idle';
            this.velocityX = 0;
        }

        if (this.aiTimer > 500 && this.isAttacking) {
            this.isAttacking = false;
            this.aiTimer = 0;
        }

        this.animations[this.currentState].update(deltaTime);
    }

    draw(ctx) {
        const anim = this.animations[this.currentState];
        const drawX = this.x - gameState.camera.x;
        const drawY = this.y - gameState.camera.y;

        // Flash when invulnerable
        if (this.invulnerable && Math.floor(Date.now() / 100) % 2 === 0) {
            ctx.globalAlpha = 0.5;
        }

        // Adjust position based on current animation size
        let offsetX = 0;
        let offsetY = 0;
        if (this.currentState === 'attack') {
            offsetX = -20;
            offsetY = 10;
        } else if (this.currentState === 'hurt') {
            offsetX = -30;
            offsetY = -30;
        } else if (this.currentState === 'death') {
            offsetX = -40;
            offsetY = -40;
        }

        anim.draw(ctx, drawX + offsetX, drawY + offsetY, this.scale, this.facingRight);
        ctx.globalAlpha = 1;

        // Draw health bar
        if (!this.isDead) {
            const barWidth = 200;
            const barHeight = 20;
            const barX = drawX - 50;
            const barY = drawY - 40;

            ctx.fillStyle = '#333';
            ctx.fillRect(barX, barY, barWidth, barHeight);

            ctx.fillStyle = '#ff0000';
            ctx.fillRect(barX, barY, (this.health / this.maxHealth) * barWidth, barHeight);

            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.strokeRect(barX, barY, barWidth, barHeight);

            ctx.fillStyle = '#fff';
            ctx.font = '14px Courier New';
            ctx.textAlign = 'center';
            ctx.fillText('Dragon Lord', drawX + 50, barY - 5);
        }
    }

    getHitbox() {
        return {
            x: this.x,
            y: this.y,
            width: this.width * this.scale,
            height: this.height * this.scale
        };
    }

    takeDamage(amount) {
        if (this.invulnerable || this.isDead) return;

        this.health -= amount;
        if (this.health <= 0) {
            this.health = 0;
            this.isDead = true;
            this.currentState = 'death';
            this.animations.death.reset();

            setTimeout(() => {
                gameState.victory = true;
                showGameOver(true);
            }, 2000);
        } else {
            this.currentState = 'hurt';
            this.animations.hurt.reset();
            this.invulnerable = true;
            this.invulnerableTimer = 500;

            setTimeout(() => {
                if (!this.isDead) {
                    this.currentState = 'idle';
                }
            }, 300);
        }
    }

    checkAttackHit(player) {
        const bossBox = this.getHitbox();
        const playerBox = player.getHitbox();

        const attackBox = {
            x: this.facingRight ? bossBox.x + bossBox.width : bossBox.x - 100,
            y: bossBox.y,
            width: 100,
            height: bossBox.height
        };

        return checkCollision(attackBox, playerBox);
    }
}

// Interactive Object
class InteractiveObject {
    constructor(x, y, type, imagePath, width, height) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.width = width;
        this.height = height;
        this.scale = 2;
        this.collected = false;

        this.image = new Image();
        this.image.src = imagePath;
        this.loaded = false;
        this.image.onload = () => { this.loaded = true; };

        // Animation
        this.bobOffset = 0;
        this.bobSpeed = 0.003;
    }

    update(deltaTime) {
        if (!this.collected) {
            this.bobOffset += this.bobSpeed * deltaTime;
        }
    }

    draw(ctx) {
        if (this.collected || !this.loaded) return;

        const drawX = this.x - gameState.camera.x;
        const drawY = this.y - gameState.camera.y + Math.sin(this.bobOffset) * 5;

        ctx.drawImage(
            this.image,
            drawX,
            drawY,
            this.width * this.scale,
            this.height * this.scale
        );

        // Glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.type === 'coin' ? '#ffdd00' : '#ff00ff';
        ctx.drawImage(
            this.image,
            drawX,
            drawY,
            this.width * this.scale,
            this.height * this.scale
        );
        ctx.shadowBlur = 0;
    }

    checkCollision(player) {
        if (this.collected) return false;

        const objBox = {
            x: this.x,
            y: this.y,
            width: this.width * this.scale,
            height: this.height * this.scale
        };

        return checkCollision(objBox, player.getHitbox());
    }

    collect() {
        if (this.collected) return;

        this.collected = true;

        if (this.type === 'coin') {
            gameState.coins++;
            document.getElementById('coin-count').textContent = gameState.coins;
        } else if (this.type === 'potion') {
            gameState.potions++;
            document.getElementById('potion-count').textContent = gameState.potions;
        }
    }
}

// Room System
class Room {
    constructor(name, width, height, backgroundColor) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.backgroundColor = backgroundColor;
        this.objects = [];
        this.enemies = [];
        this.doors = [];
        this.backgroundTiles = [];
    }

    addObject(obj) {
        this.objects.push(obj);
    }

    addEnemy(enemy) {
        this.enemies.push(enemy);
    }

    addDoor(x, y, width, height, targetRoom, message) {
        this.doors.push({ x, y, width, height, targetRoom, message });
    }

    addBackgroundTile(x, y, imagePath, width, height, scale = 1) {
        const tile = {
            x, y, width, height, scale,
            image: new Image(),
            loaded: false
        };
        tile.image.src = imagePath;
        tile.image.onload = () => { tile.loaded = true; };
        this.backgroundTiles.push(tile);
    }

    update(deltaTime, player) {
        this.objects.forEach(obj => obj.update(deltaTime));
        this.enemies.forEach(enemy => enemy.update(deltaTime, player));

        // Check object collection
        this.objects.forEach(obj => {
            if (obj.checkCollision(player)) {
                obj.collect();
            }
        });

        // Check door transitions
        this.doors.forEach(door => {
            const playerBox = player.getHitbox();
            if (checkCollision(door, playerBox)) {
                showInteractionPrompt(door.message);
                if (input.interact) {
                    changeRoom(door.targetRoom, player);
                }
            }
        });
    }

    draw(ctx) {
        // Draw background
        ctx.fillStyle = this.backgroundColor;
        ctx.fillRect(-gameState.camera.x, -gameState.camera.y, this.width, this.height);

        // Draw background tiles
        this.backgroundTiles.forEach(tile => {
            if (tile.loaded) {
                ctx.drawImage(
                    tile.image,
                    tile.x - gameState.camera.x,
                    tile.y - gameState.camera.y,
                    tile.width * tile.scale,
                    tile.height * tile.scale
                );
            }
        });

        // Draw objects
        this.objects.forEach(obj => obj.draw(ctx));

        // Draw doors
        ctx.fillStyle = 'rgba(100, 100, 200, 0.3)';
        ctx.strokeStyle = '#6666ff';
        ctx.lineWidth = 3;
        this.doors.forEach(door => {
            ctx.fillRect(
                door.x - gameState.camera.x,
                door.y - gameState.camera.y,
                door.width,
                door.height
            );
            ctx.strokeRect(
                door.x - gameState.camera.x,
                door.y - gameState.camera.y,
                door.width,
                door.height
            );
        });

        // Draw enemies
        this.enemies.forEach(enemy => enemy.draw(ctx));
    }
}

// Collision Detection
function checkCollision(box1, box2) {
    return box1.x < box2.x + box2.width &&
           box1.x + box1.width > box2.x &&
           box1.y < box2.y + box2.height &&
           box1.y + box1.height > box2.y;
}

// Room Definitions
const rooms = {};

function initializeRooms() {
    // Starting Room
    const startRoom = new Room('start', 2000, CONFIG.height, '#1a1a2e');

    // Add floor tiles
    for (let i = 0; i < 30; i++) {
        startRoom.addBackgroundTile(i * 64, CONFIG.height - 150, 'environment/ground_stone1.png', 256, 256, 0.5);
    }

    // Add dungeon decorations
    startRoom.addBackgroundTile(200, 100, 'Dungeon Gathering Free Version/Set 1.1.png', 192, 192, 2);
    startRoom.addBackgroundTile(600, 150, 'Dungeon Gathering Free Version/Structure.png', 64, 64, 2);
    startRoom.addBackgroundTile(1000, 200, 'Dungeon Gathering Free Version/Torch Yellow L.png', 16, 16, 3);

    // Add collectibles
    startRoom.addObject(new InteractiveObject(300, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/Coin Sheet.png', 16, 16));
    startRoom.addObject(new InteractiveObject(500, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/Coin Sheet.png', 16, 16));
    startRoom.addObject(new InteractiveObject(700, CONFIG.height - 250, 'potion', 'Dungeon Gathering Free Version/Potion 1.png', 16, 16));
    startRoom.addObject(new InteractiveObject(900, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/BlueCoin Sheet.png', 16, 16));

    // Add door to dungeon
    startRoom.addDoor(1800, CONFIG.height - 300, 100, 150, 'dungeon', 'Press E to enter the Dungeon');

    rooms.start = startRoom;

    // Dungeon Corridor
    const dungeonRoom = new Room('dungeon', 2500, CONFIG.height, '#0f0f1a');

    // Add floor
    for (let i = 0; i < 40; i++) {
        dungeonRoom.addBackgroundTile(i * 64, CONFIG.height - 150, 'environment/ground_stone1.png', 256, 256, 0.5);
    }

    // Add decorations
    for (let i = 0; i < 8; i++) {
        dungeonRoom.addBackgroundTile(i * 300 + 100, 150, 'Dungeon Gathering Free Version/Torch Yellow.png', 16, 16, 3);
    }
    dungeonRoom.addBackgroundTile(400, 120, 'Dungeon Gathering Free Version/Set 1.2.png', 48, 48, 2.5);
    dungeonRoom.addBackgroundTile(800, 120, 'Dungeon Gathering Free Version/Set 1.3.png', 48, 48, 2.5);
    dungeonRoom.addBackgroundTile(1200, 100, 'Dungeon Gathering Free Version/Set 3.5.png', 64, 64, 2);
    dungeonRoom.addBackgroundTile(1600, 100, 'Dungeon Gathering Free Version/Set 4.5.png', 64, 64, 2);

    // Add collectibles
    dungeonRoom.addObject(new InteractiveObject(400, CONFIG.height - 250, 'potion', 'Dungeon Gathering Free Version/Potion 2.png', 16, 16));
    dungeonRoom.addObject(new InteractiveObject(800, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/BlueCoin Sheet.png', 16, 16));
    dungeonRoom.addObject(new InteractiveObject(1200, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/Coin Sheet.png', 16, 16));
    dungeonRoom.addObject(new InteractiveObject(1600, CONFIG.height - 250, 'potion', 'Dungeon Gathering Free Version/Potion 3.png', 16, 16));
    dungeonRoom.addObject(new InteractiveObject(2000, CONFIG.height - 250, 'coin', 'Dungeon Gathering Free Version/BlueCoin Sheet.png', 16, 16));

    // Add doors
    dungeonRoom.addDoor(50, CONFIG.height - 300, 100, 150, 'start', 'Press E to return to Start');
    dungeonRoom.addDoor(2300, CONFIG.height - 300, 100, 150, 'boss', 'Press E to face the Dragon Lord');

    rooms.dungeon = dungeonRoom;

    // Boss Room
    const bossRoom = new Room('boss', 1800, CONFIG.height, '#0a0a15');

    // Add floor
    for (let i = 0; i < 30; i++) {
        bossRoom.addBackgroundTile(i * 64, CONFIG.height - 150, 'environment/ground_stone1.png', 256, 256, 0.5);
    }

    // Add dramatic decorations
    bossRoom.addBackgroundTile(100, 80, 'Dungeon Gathering Free Version/Torch Yellow L.png', 16, 16, 4);
    bossRoom.addBackgroundTile(1600, 80, 'Dungeon Gathering Free Version/Torch Yellow L.png', 16, 16, 4);
    bossRoom.addBackgroundTile(800, 50, 'Dungeon Gathering Free Version/Set 1.1.png', 192, 192, 3);

    // Add health potions for boss fight
    bossRoom.addObject(new InteractiveObject(200, CONFIG.height - 250, 'potion', 'Dungeon Gathering Free Version/Potion 4.png', 16, 16));
    bossRoom.addObject(new InteractiveObject(1500, CONFIG.height - 250, 'potion', 'Dungeon Gathering Free Version/Potion 5.png', 16, 16));

    // Add Dragon Lord boss
    const dragonLord = new DragonLord(1200, CONFIG.height - 350);
    bossRoom.addEnemy(dragonLord);

    // Add door back
    bossRoom.addDoor(50, CONFIG.height - 300, 100, 150, 'dungeon', 'Press E to retreat');

    rooms.boss = bossRoom;
}

// Room Management
function changeRoom(roomName, player) {
    gameState.currentRoom = roomName;

    // Update UI
    const roomNames = {
        'start': 'Starting Chamber',
        'dungeon': 'Dark Dungeon',
        'boss': 'Dragon Lord\'s Lair'
    };
    document.getElementById('current-room').textContent = roomNames[roomName] || roomName;

    // Reset player position based on room
    if (roomName === 'start') {
        player.x = 100;
    } else if (roomName === 'dungeon') {
        player.x = roomName === 'start' ? 1800 : 200;
    } else if (roomName === 'boss') {
        player.x = 200;
    }

    hideInteractionPrompt();
}

// UI Functions
function updateHealthBar() {
    const healthFill = document.getElementById('health-fill');
    const healthText = document.getElementById('health-text');
    const healthPercent = (gameState.playerHealth / gameState.maxHealth) * 100;

    healthFill.style.width = healthPercent + '%';
    healthText.textContent = `${gameState.playerHealth}/${gameState.maxHealth}`;

    if (gameState.playerHealth <= 0) {
        setTimeout(() => {
            showGameOver(false);
        }, 1500);
    }
}

function showInteractionPrompt(message) {
    const prompt = document.getElementById('interaction-prompt');
    prompt.textContent = message;
    prompt.style.display = 'block';
}

function hideInteractionPrompt() {
    document.getElementById('interaction-prompt').style.display = 'none';
}

function showGameOver(victory) {
    gameState.gameOver = true;
    const gameOverDiv = document.getElementById('game-over');
    const title = document.getElementById('game-over-title');
    const message = document.getElementById('game-over-message');

    if (victory) {
        gameOverDiv.classList.add('victory');
        title.textContent = 'VICTORY!';
        message.textContent = `You have slain the Dragon Lord!\nCoins collected: ${gameState.coins}`;
    } else {
        gameOverDiv.classList.remove('victory');
        title.textContent = 'GAME OVER';
        message.textContent = `The Dragon Lord has defeated you...\nCoins collected: ${gameState.coins}`;
    }

    gameOverDiv.style.display = 'block';
}

// Camera System
function updateCamera(player) {
    const room = rooms[gameState.currentRoom];

    // Center camera on player
    gameState.camera.x = player.x - CONFIG.width / 2;
    gameState.camera.y = 0;

    // Clamp camera to room bounds
    if (gameState.camera.x < 0) gameState.camera.x = 0;
    if (gameState.camera.x > room.width - CONFIG.width) {
        gameState.camera.x = room.width - CONFIG.width;
    }
    if (gameState.camera.y < 0) gameState.camera.y = 0;
    if (gameState.camera.y > room.height - CONFIG.height) {
        gameState.camera.y = room.height - CONFIG.height;
    }
}

// Input Handling
document.addEventListener('keydown', (e) => {
    keys[e.key.toLowerCase()] = true;

    // Update input state
    input.left = keys['a'] || keys['arrowleft'];
    input.right = keys['d'] || keys['arrowright'];
    input.up = keys['w'] || keys['arrowup'];
    input.down = keys['s'] || keys['arrowdown'];
    input.attack = keys[' '];
    input.defend = keys['shift'];
    input.run = keys['shift'];
    input.interact = keys['e'];

    // Use potion
    if (keys['e'] && gameState.potions > 0 && gameState.playerHealth < gameState.maxHealth) {
        // Only use if not near a door
        let nearDoor = false;
        const currentRoom = rooms[gameState.currentRoom];
        const playerBox = player.getHitbox();
        currentRoom.doors.forEach(door => {
            if (checkCollision(door, playerBox)) {
                nearDoor = true;
            }
        });

        if (!nearDoor) {
            gameState.potions--;
            player.heal(30);
            document.getElementById('potion-count').textContent = gameState.potions;
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key.toLowerCase()] = false;

    input.left = keys['a'] || keys['arrowleft'];
    input.right = keys['d'] || keys['arrowright'];
    input.up = keys['w'] || keys['arrowup'];
    input.down = keys['s'] || keys['arrowdown'];
    input.attack = keys[' '];
    input.defend = keys['shift'];
    input.run = keys['shift'];
    input.interact = keys['e'];
});

// Game Loop
let player;
let lastTime = 0;

function gameLoop(timestamp) {
    const deltaTime = timestamp - lastTime;
    lastTime = timestamp;

    if (!gameState.gameOver) {
        // Update
        player.update(deltaTime);

        const currentRoom = rooms[gameState.currentRoom];
        currentRoom.update(deltaTime, player);

        // Check player attacks against enemies
        const attackBox = player.getAttackHitbox();
        if (attackBox) {
            currentRoom.enemies.forEach(enemy => {
                if (checkCollision(attackBox, enemy.getHitbox())) {
                    enemy.takeDamage(20);
                }
            });
        }

        updateCamera(player);

        // Clear prompt if not near any door
        let nearDoor = false;
        const playerBox = player.getHitbox();
        currentRoom.doors.forEach(door => {
            if (checkCollision(door, playerBox)) {
                nearDoor = true;
            }
        });
        if (!nearDoor) {
            hideInteractionPrompt();
        }
    }

    // Render
    const ctx = CONFIG.ctx;
    ctx.clearRect(0, 0, CONFIG.width, CONFIG.height);

    const currentRoom = rooms[gameState.currentRoom];
    currentRoom.draw(ctx);
    player.draw(ctx);

    requestAnimationFrame(gameLoop);
}

// Initialize Game
function initGame() {
    CONFIG.canvas = document.getElementById('gameCanvas');
    CONFIG.ctx = CONFIG.canvas.getContext('2d');
    CONFIG.canvas.width = CONFIG.width;
    CONFIG.canvas.height = CONFIG.height;

    initializeRooms();
    player = new Player(100, CONFIG.height - 200);

    updateHealthBar();

    // Restart button
    document.getElementById('restart-button').addEventListener('click', () => {
        location.reload();
    });

    requestAnimationFrame(gameLoop);
}

// Start game when page loads
window.addEventListener('load', initGame);
