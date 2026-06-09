from cmu_graphics import *
"""
Github: https://githubcom/oracl8/SlayTheDragon

Note:
I spent a long time working with the sprites. I had to learn how to download sprite sheets, unzip rar and zip files, 
work with github in terms of uploading the correct size and ammount of files, slicing sprites, reversing sprites, and looping through sprites.

Overview:

I made a 2d platformer game where you can explore 9 connected rooms, collected coins, purchase upgrades in a shop and defeat a dragon boss.

Features to grade:

Animation System:
Use of sprites
Knight has 7 animation states: idle, walk, attack1, attack2, death, hurt and jump
Dragon has 5 animation states: idle, walk, attack, hurt and death
All animations have smooth frame cycling as well as good state transitions

Rooms:
Center room connects to: top,bottom,left1-2, and right1-3
Each room has unique platform layout and things to do (such as spikes)
Smooth room transitions at screen edges

Physics:
Gravity and jumping mechanics
platform collision - standing, head bumps, and side collision
Spike sections with respawn and damage

Coin system:
20 coins to collect across rooms
Animated coin rotation with sprite
Collection animation on pickup
Coin counter display

Shop system - 'inside' room:
When in left 2 and near shop press e to enter
4 upgrades 10 coins each - clear what they do
use arrow keys to nagivate and enter to purchase
There is visual feedback for all the above
Cant move when in shop

Boss fight:
Cutscene
Dragon walks back and forth and attacks every 4 seconds whne facing the player
Health bars displayed
Invulnerability of knight after you take damage
Victory screen - cant move and sick animation of dragon death

Combat:
Two sprite attack types. 1: 'i' 2: 'o'
Directional sword hitboxes based on which was you are facing. - had to use vscode to flip all sliced sprites and reupload to github.
attack cooldown
dragon hurt animation with immunity
knockback on player when they get hit

How to test:
Start in the center and explore all rooms using a and d keys as well as jumping with space. 
Collect coins in left right and bottom and then go tho the very left and enter shop enter with 'e' then walk to shopekeeper and press 'f'.
Buy upgrades with coins. Go to top to trigger boss fight. Use 'i' and 'o' to fight. Press r to restart after death or win.

Shortcuts:
Press '1' to make dragon hp 2. - Obviously only works in boss room.
press '2' to get 40 coins.
Press '3' to teleport to shop.
press '4' to go to boss with all upgrades - 5 hp, 2x damage, faster attack speed, faster movement speed




"""


def onAppStart(app):
    
    app.width = 700
    app.height = 700
    app.instructionTimer = 90
    app.showInstructions = True
    
    app.currentRoom = 'center'
    app.gameOver = False
    app.multiplier = 1
    app.nearShopDoor = False
    app.nearShopExit = False
    app.nearShopkeeper = False
    
    app.inShop = False
    app.shopSelectedItem = 0
    app.shopItems = {
    'health_upgrade': {'cost': 10, 'purchased': False, 'name': 'Max HP +1'},
    'damage_boost': {'cost': 10, 'purchased': False, 'name': 'Damage +1'},
    'speed_boost': {'cost': 10, 'purchased': False, 'name': 'Speed +1'},
    'attack_speed': {'cost': 10, 'purchased': False, 'name': 'Fast Attack'}
    }
    app.shopItemsList = ['health_upgrade','damage_boost','speed_boost','attack_speed']
    


    
    app.knightHasHitAttack = False
    app.knightX = 350
    app.knightY = 350
    app.knightSpeed = 5
    app.knightFrame = 1
    app.knightState = 'idle'
    app.knightFrameTimer = 0 
    app.knightAnimSpeed = 8
    app.knightMoving = False
    app.knightVelocityY = 0
    app.knightAttacking = False
    app.knightAttackType = None
    app.knightAttackCooldown = 0
    app.knightAttackCooldownTime = 15
    app.knightAttack1Frames = 6
    app.knightAttack2Frames = 5
    app.knightHurtFrames = 4
    app.knightHP = 4
    app.knightInvulnerable = False
    app.knightInvulnerabilityTime = 60
    app.knightFacingRight = True
    
    app.dragonDeathComplete = False
    app.victoryWaitTimer = 0
    app.victory = False
    
    app.gravity = 0.4
    app.jumpStrength = -12
    app.onGround = False
    
    app.dragonFacingRight = True
    app.dragonX = 350
    app.dragonY = 200
    app.dragonSpeed = 2
    app.dragonDirection = 1
    app.dragonFrame = 1
    app.dragonFrameTimer = 0
    app.dragonState = 'idle'
    app.dragonDeathFrames  =36
    app.dragonAttackTimer = 120
    app.dragonAttackCooldown = 120
    
    app.coinFrame = 1
    app.coinFrameTimer = 0
    app.coinAnimSpeed = 5
    app.collectedCoins = []
    app.coinsCollected = 0
    
    app.bossFightStarted = False
    app.bossIntroTimer = 0
    app.bossIntroLength = 60
    app.dragonHP = 15
    app.dragonAttacking = False
    app.dragonAttackFrame = 0
    app.dragonAttackFrames = 16
    app.dragonHurtFrames = 5
    app.dragonShowingHurt = False
    app.dragonHurtTimer = 0
    
    app.projectiles = []
    app.projectileSpeed = 8
    app.projectileLife = 100

    
    
    app.knightIdleFrames = 7
    app.knightWalkFrames = 8
    app.knightJumpFrames = 5
    app.dragonIdleFrames = 4
    app.dragonWalkFrames = 8
    
    app.stepsPerSecond = 30
    
    app.platforms = {
        'center': [(0,590,130,210), (265,590,180,210),(0,0,395,350),(440,675,45,15),(550,550,100,120), (480,415,60,95), (530,455,160,100),
        (395,245,50,125),(530,85,60,50),(590,0,100,200)],
        'left1': [(615,545,155,155),(425,545,120,160),(225,545,120,165),(0,505,145,185)],
        'left2': [(0,586,700,110),(0,0,5,700)],
        'right1': [(0,675,700,700)],
        'right2': [(0,560,700,700)],
        'right3': [(0,650,700,700),(695,0,5,700)],
        'inside': [(0,555,700,700),(600,0,100,700),(0,0,5,700)],
        'top': [(0,0,25,700),(695,0,5,700),(25,468,50,700),(0,640,287,60),(640,468,60,350),(385,640,315,60),(287,635,97,10), (145,287,430,130)],
        'bottom': [(0,0,55,700),(395,0,50,175),(202,0,50,175),(0,630,225,170),(435,630,200,170),(600,0,150,700),(195,380,260,150),(42,535,47,10),(560,535,47,10),(300,240,47,10),(260,120,47,10)]
    }
    app.spikes = {
        'center': [(125,700,140)],
        'left1': [(540,610,90),(340,610,90),(140,610,90)],
        'left2': [],
        'right1': [],
        'right2': [],
        'right3': [],
        'inside': [],
        'top': [],
        'bottom': [(220,700,210)]
    }
    app.coins = {
        'center': [(460,660), (415,225)],
        'left1': [(475,515),(285,515),(80,475)],
        'left2': [],
        'right1': [(470,625),(200,500)], 
        'right2': [(200,520),(300,520),(400,520),(500,520)],
        'right3': [(500,610),(600,610),(500,500),(600,500)],
        'inside': [],
        'top': [],
        'bottom': [(450,600),(500,600),(66,495),(175,605),(217,305)]
    }
    
    
    
def onStep(app):
    if app.gameOver:
        return
    if app.showInstructions:
        app.instructionTimer -=1
        if app.instructionTimer <= 0:
            app.showInstructions = False
    app.knightFrameTimer += 1
    if app.knightFrameTimer >= 30 // app.knightAnimSpeed:
        app.knightFrameTimer = 0
        if app.knightState == 'idle':
            app.knightFrame = (app.knightFrame % app.knightIdleFrames) + 1
        elif app.knightState == 'walk':
            app.knightFrame = (app.knightFrame % app.knightWalkFrames) + 1
        elif app.knightState == 'jump':
            app.knightFrame = (app.knightFrame % app.knightJumpFrames) + 1
        elif app.knightState == 'attack1':
            app.knightFrame = (app.knightFrame % app.knightAttack1Frames) + 1              
        elif app.knightState == 'attack2':
            app.knightFrame = (app.knightFrame % app.knightAttack2Frames) + 1
        elif app.knightState == 'hurt':
            app.knightFrame = (app.knightFrame % app.knightHurtFrames) + 1
        elif app.knightState == 'death':
            app.knightFrame = (app.knightFrame % app.knightDeathFrames) + 1
            
    app.knightVelocityY += app.gravity
    app.knightY += app.knightVelocityY
    app.onGround = False
    for platform in app.platforms[app.currentRoom]:
        px,py,pw,ph = platform
        if (app.knightX > px and app.knightX < px+pw and app.knightY + 25 > py and app.knightY + 25 < py + ph and app.knightVelocityY > 0):
            app.knightY = py - 25
            app.knightVelocityY = 0
            app.onGround = True
            if app.knightState == 'jump':
                app.knightState = 'idle'
        if app.knightY + 10 > py and app.knightY - 10 < py + ph:
            if  app.knightX +10 > px and app.knightX < px:
                app.knightX = px -10
            elif app.knightX - 10 < px +pw and app.knightX > px + pw:
                app.knightX = px + pw +10
                
                
    #Headbump
    if app.currentRoom == 'bottom':
        px,py,pw,ph = 195,380,245,100
        if (app.knightX > px and app.knightX < px + pw and app.knightY - 25 < py + ph and app.knightY - 25 > py and app.knightVelocityY < 0):
            app.knightY = py+ph+25
            app.knightVelocityY = 0
    elif app.currentRoom == 'right2':
        px,py,pw,ph = 0,0,700,420
        if (app.knightX > px and app.knightX < px + pw and app.knightY - 25 < py + ph and app.knightY - 25 > py and app.knightVelocityY < 0):
            app.knightY = py+ph+25
            app.knightVelocityY = 0
    elif app.currentRoom == 'center':
        px,py,pw,ph = 480,430,60,100
        if (app.knightX > px and app.knightX < px + pw and app.knightY - 25 < py + ph and app.knightY - 25 > py and app.knightVelocityY < 0):
            app.knightY = py+ph+25
            app.knightVelocityY = 0
    #spikes
    for spike in app.spikes[app.currentRoom]:
        sx,sy,sw= spike
        if (app.knightX > sx and app.knightX < sx+sw and app.knightY + 25 > sy):
            app.knightY = 500
            app.knightX = 300
            app.knightHP -=1
            if app.knightHP <= 0:
                app.gameOver = True
            app.knightVelocityY = 0
    
    app.coinFrameTimer +=1
    if app.coinFrameTimer >= app.coinAnimSpeed:
        app.coinFrameTimer = 0
        app.coinFrame = (app.coinFrame % 8) + 1
    coinsToRemove = []
    for coin in app.coins[app.currentRoom]:
        cx,cy = coin
        if distance(app.knightX,app.knightY,cx,cy) < 30:                
            app.collectedCoins.append([cx,cy,app.currentRoom,9])
            coinsToRemove.append(coin)
            app.coinsCollected +=1
    for coin in coinsToRemove:
        app.coins[app.currentRoom].remove(coin)
    newCollectedCoins = []
    for collected in app.collectedCoins:
        collected[3] +=1
        if collected[3] <=16:
            newCollectedCoins.append(collected)
    app.collectedCoins = newCollectedCoins
    
    
    if app.knightAttackCooldown > 0:
        app.knightAttackCooldown -=1
        
    if app.knightAttacking:
        if app.knightAttackType == 'attack1' and app.knightFrame >= app.knightAttack1Frames:
            app.knightAttacking = False
            app.knightState = 'idle'
            app.knightFrame = 1
            app.knightAttackCooldown = app.knightAttackCooldownTime
        elif app.knightAttackType == 'attack2' and app.knightFrame >= app.knightAttack2Frames:
            app.knightAttacking = False
            app.knightState = 'idle'    
            app.knightFrame = 1
            app.knightAttackCooldown = app.knightAttackCooldownTime
    
    if app.knightAttacking and not app.knightHasHitAttack:
        if app.currentRoom == 'top':
            if app.knightFacingRight:
                attackX = app.knightX + 40                                          
            else:
                attackX = app.knightX - 40
            if distance(attackX,app.knightY,app.dragonX,app.dragonY) < 80:
                app.dragonHP -= 1 * app.multiplier
                if app.dragonHP <= 0:
                    app.dragonState = 'death'
                    app.dragonFrame = 1
                else:
                    app.dragonShowingHurt = True
                    app.dragonHurtTimer = 10
                    app.knightHasHitAttack = True
                    app.dragonFrame = 1
    if app.dragonShowingHurt:
        app.dragonHurtTimer -= 1
        if app.dragonHurtTimer <= 0:
            app.dragonShowingHurt = False
            app.dragonFrame = 1
    if app.knightInvulnerable:
        app.knightInvulnerabilityTime -= 1
        if app.knightInvulnerabilityTime <= 0 :
            app.knightInvulnerable = False
            app.knightInvulnerabilityTime = 60
            if app.knightState == 'hurt':
                app.knightState = 'idle'
                app.knightFrame = 1
    if not app.knightInvulnerable and app.currentRoom == 'top':
        if distance(app.knightX,app.knightY,app.dragonX,app.dragonY) < 80:
            if app.knightX < app.dragonX:
                app.knightX -= 30
            else:
                app.knightX += 30
            app.knightHP -= 1
            if app.knightHP <=0:
                    app.gameOver = True
            app.knightInvulnerable = True
            app.knightState = 'hurt'
            
            app.knightFrame = 1
    
            
    if app.currentRoom == 'top':
        if not app.bossFightStarted:
            app.bossFightStarted = True
            app.bossIntroTimer = 0
            app.dragonState = 'idle'
            app.dragonFrame = 1
            
        if app.bossIntroTimer < app.bossIntroLength:
            app.bossIntroTimer += 1
            app.dragonFrameTimer +=1
            if app.dragonFrameTimer >= 30 // 8:
                app.dragonFrameTimer = 0
                app.dragonFrame = (app.dragonFrame % app.dragonIdleFrames) + 1
        else:
            if app.dragonState == 'idle':
                app.dragonState = 'walk'
                app.dragonFrame = 1
            if app.dragonAttackTimer > 0:
                app.dragonAttackTimer-=1
            if app.dragonAttackTimer == 0 and app.dragonState != 'death':
                playerToRight = app.knightX > app.dragonX
                if (playerToRight and app.dragonFacingRight) or (not playerToRight and not app.dragonFacingRight):
                    app.dragonState = 'attack'
                    app.dragonFrame = 1
                    app.dragonAttackTimer = app.dragonAttackCooldown
            app.dragonFrameTimer +=1
            if app.dragonFrameTimer >= 30 // 8:
                app.dragonFrameTimer = 0
                if app.dragonShowingHurt:
                    app.dragonFrame = (app.dragonFrame % app.dragonHurtFrames) + 1 
                elif app.dragonState == 'walk':
                    app.dragonFrame = (app.dragonFrame % app.dragonWalkFrames) + 1 
                elif app.dragonState == 'idle':
                    app.dragonFrame = (app.dragonFrame % app.dragonIdleFrames) + 1 
                elif app.dragonState == 'attack':
                    if app.dragonFrame < app.dragonAttackFrames:
                        app.dragonFrame +=1
                    else:
                        app.dragonState = 'walk'
                        app.dragonFrame = 1
                elif app.dragonState == 'death':
                    if not app.dragonDeathComplete:
                        if app.dragonFrame < app.dragonDeathFrames:
                            app.dragonFrame = (app.dragonFrame % app.dragonDeathFrames) + 1 
                        else:
                            app.dragonDeathComplete = True
                            app.victoryWaitTimer = 15
                    else:
                        if app.victoryWaitTimer > 0:
                            app.victoryWaitTimer -=1
                        else:
                            app.victory = True
            
            if app.dragonState == 'walk':
                app.dragonX += app.dragonSpeed * app.dragonDirection
                if app.dragonX > 570 or app.dragonX < 140:
                    app.dragonDirection *= -1
                    app.dragonFacingRight = not app.dragonFacingRight
        if app.dragonState == 'attack':
            if app.dragonFrame == 5 or app.dragonFrame == 9 or app.dragonFrame == 14:
                direction = 1 if app.dragonFacingRight else -1
                alreadySpawned = False
                for proj in app.projectiles:
                    if proj[0] ==app.dragonX and proj[1] == app.dragonY +50:
                        alreadySpawned = True
                        break
                if not alreadySpawned:
                    app.projectiles.append([app.dragonX,app.dragonY + 50,direction,app.projectileLife])
        newProjectiles = []
        for proj in app.projectiles:
            hit = False
            proj[0] += proj[2] * app.projectileSpeed
            proj[3] -= 1
            if not app.knightInvulnerable and distance(proj[0],proj[1], app.knightX,app.knightY) < 50:
                app.knightHP -= 1
                if app.knightHP <=0:
                    app.gameOver = True
                app.knightInvulnerable = True                                   
                app.knightState = 'hurt'
                app.knightFrame = 1
                app.knightX += proj[2] * 40
                hit = True
            if not hit and proj[3] > 0 :
                newProjectiles.append(proj)
        app.projectiles = newProjectiles
    if app.currentRoom == 'left2' and app.knightX >= 250 and app.knightX <=365:
        app.nearShopDoor = True
    else:
        app.nearShopDoor = False
    if app.currentRoom == 'inside' and app.knightX < 100:
        app.nearShopExit = True
    else:
        app.nearShopExit = False
    if app.currentRoom == 'inside' and app.knightX > 350 and app.knightX < 550:
        app.nearShopkeeper = True
    else:
        app.nearShopkeeper = False
    if not (app.currentRoom == 'top' and app.bossIntroTimer < app.bossIntroLength):
        checkRoomTransitions(app)

def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5
    
def checkRoomTransitions(app):
    if app.knightX < 3 and app.currentRoom == 'center':
        app.currentRoom = 'left1'
        app.knightX = 650
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX > 697 and app.currentRoom == 'center':
        app.currentRoom = 'right1'
        app.knightX = 50
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightY < 3 and app.currentRoom == 'center':
        app.currentRoom = 'top'
        app.knightX = 350
        app.knightY = 525
        app.knightVelocityY = 0
    elif app.knightY + 25 > 700 and app.currentRoom == 'center':
        app.currentRoom = 'bottom'
        app.knightX = 350
        app.knightY = 100
        app.knightVelocityY = 0
    
        
    elif app.knightX > 697 and app.currentRoom == 'left1':
        app.currentRoom = 'center'
        app.knightX = 50
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX < 3 and app.currentRoom == 'left1':
        app.currentRoom = 'left2'
        app.knightX = 650
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX > 697 and app.currentRoom == 'left2':
        app.currentRoom = 'left1'
        app.knightX = 50
        app.knightY = 550
        app.knightVelocityY = 0
        
        
    elif app.knightX < 3 and app.currentRoom == 'right1':
        app.currentRoom = 'center'
        app.knightX = 650
        app.knightY = 425
        app.knightVelocityY = 0
    elif app.knightX > 697 and app.currentRoom == 'right1':
        app.currentRoom = 'right2'
        app.knightX = 50
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX < 3 and app.currentRoom == 'right2':
        app.currentRoom = 'right1'
        app.knightX = 650
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX > 697 and app.currentRoom == 'right2':
        app.currentRoom = 'right3'
        app.knightX = 50
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightX < 3 and app.currentRoom == 'right3':
        app.currentRoom = 'right2'
        app.knightX = 650   
        app.knightY = 550
        app.knightVelocityY = 0
    elif app.knightY + 25 > 700 and app.currentRoom == 'top':
        app.currentRoom = 'center'
        app.knightX = 350
        app.knightY = 100
        app.knightVelocityY = 0
    elif app.knightY < 0 and app.currentRoom == 'bottom':
        app.currentRoom = 'center'
        app.knightX = 460
        app.knightY = 635
        app.knightVelocityY = 0
    else:
        app.knightX = max(0,min(app.knightX,700))
        app.knightY = max(0,min(app.knightY,700))
        

def onKeyHold(app, keys):
    if app.inShop:
        return
    if app.dragonState == 'death':
        return
    if app.currentRoom == 'top' and app.bossIntroTimer < app.bossIntroLength:
        return
    
    app.knightMoving = False
    

    if 'a' in keys and 'd' not in keys:
        app.knightX -= app.knightSpeed
        app.knightMoving = True
        app.knightFacingRight = False

    if 'd' in keys and 'a' not in keys:
        app.knightX += app.knightSpeed
        app.knightMoving = True
        app.knightFacingRight = True
    
    if app.knightAttacking:
        return
        
    if app.knightMoving:
        if app.knightState != 'walk':
            app.knightState = 'walk'
            app.knightFrame = 1
    else:
        if app.knightState != 'idle':
            app.knightState = 'idle'
            app.knightFrame = 1
def onKeyPress(app,key):    
    if key == 'r' and (app.gameOver or app.victory):
        onAppStart(app)
        return
    if key == '1':
        if app.currentRoom == 'top':
            app.dragonHP = 2
    elif key == '2':
        app.coinsCollected = 40
    elif key == '3':
        app.currentRoom = 'inside'
        app.knightX = 400
        app.knightY = 500
        app.knightVelocityY = 0
    elif key == '4':
        app.currentRoom = 'top'
        app.knightX = 350
        app.knightY = 525
        app.knightVelocityY = 0
        app.knightHP = 5
        app.multiplier = 2
        app.knightSpeed = 7
        app.knightAttackCooldownTime = 10
        app.bossFightStarted = False
        app.dragonHP = 15
        
    if app.inShop and key != 'f' and key not in ['up','left','right','down','enter']:
        return
    if key == 'space' and app.onGround:
        if app.currentRoom == 'top' and app.bossIntroTimer < app.bossIntroLength:
            return
        app.knightVelocityY = app.jumpStrength
        app.knightState = 'jump'
        app.knightFrame = 1
    if not app.knightAttacking and app.knightAttackCooldown == 0:
        if app.currentRoom == 'top' and app.bossIntroTimer < app.bossIntroLength:
            return
        if key == 'i':
            app.knightAttacking = True
            app.knightAttackType = 'attack1'
            app.knightState = 'attack1'
            app.knightFrame = 1
            app.knightHasHitAttack = False
        elif key == 'o':
            app.knightAttacking = True
            app.knightState = 'attack2'
            app.knightAttackType = 'attack2'
            app.knightFrame = 1
            app.knightHasHitAttack = False
    if key == 'e':
        if app.currentRoom == 'left2' and app.nearShopDoor:
            app.currentRoom = 'inside'
            app.knightX = 50
            app.knightY = 500
            app.knightVelocityY = 0
        elif app.currentRoom == 'inside' and app.nearShopExit:
            app.currentRoom = 'left2'
            app.knightX = 300
            app.knightY = 540
            app.knightVelocityY = 0
    if key == 'f':
        if app.currentRoom == 'inside' and app.nearShopkeeper:
            app.inShop = not app.inShop
    if app.inShop:
        if key == 'up':
            if app.shopSelectedItem >= 2:
                app.shopSelectedItem -= 2
        elif key == 'down':
            if app.shopSelectedItem <= 1:
                app.shopSelectedItem += 2     
        elif key == 'left':                                         # Used inspiration from isLegalSudoku HW
            if app.shopSelectedItem % 2 == 1:
                app.shopSelectedItem -= 1
        
        elif key == 'right':
            if app.shopSelectedItem %2 == 0:
                app.shopSelectedItem += 1
        elif key == 'enter':
            itemKey = app.shopItemsList[app.shopSelectedItem]
            item = app.shopItems[itemKey]
            if not item['purchased']:                                   
                if app.coinsCollected >= item['cost']:
                    app.coinsCollected -= item['cost']
                    item['purchased'] = True
                    if itemKey == 'health_upgrade':
                        app.knightHP  +=1
                    elif itemKey == 'damage_boost':
                        app.multiplier = 2
                    elif itemKey == 'speed_boost':
                        app.knightSpeed += 2
                    elif itemKey == 'attack_speed':
                        app.knightAttackCooldownTime = max(5,app.knightAttackCooldownTime - 5)
            
def onKeyRelease(app, key):
    if app.onGround and not app.knightAttacking:
        app.knightState = 'idle'
        app.knightFrame = 1
    
def redrawAll(app):
    if app.gameOver:
        drawRect(0,0,700,700,fill = 'black')
        drawLabel('YOU DIED', 350,250, size = 60, fill = 'red', bold = True, font = 'monospace')
        drawLabel('Press R to Restart', 350,400, size = 30, fill = 'red', font = 'monospace')
        return
    if app.victory:
        drawRect(0,0,700,700,fill = 'black')
        drawLabel('Victory!', 350,250, size = 60, fill = 'gold', bold = True, font = 'monospace')
        drawLabel('Press R to Restart', 350,400, size = 30, fill = 'gold', font = 'monospace')
        return
    
        
    drawRoomBackground(app)
    if app.showInstructions:
        drawRect(0,0,700,700,fill = 'black',opacity = 50)
        drawLabel('Press A and D to move', 150,100, fill = 'white', size = 24, bold = True)
        drawLabel('Press SPACE to jump', 150,150, fill = 'white', size = 24, bold = True)
        drawLabel('Press I and O to attack', 150,200, fill = 'white', size = 24, bold = True)

    if app.currentRoom == 'bottom':
        drawRect(260,120,47,10,fill = 'black',border = 'gray')
        drawRect(42,535,47,10,fill = 'black',border = 'gray')
        drawRect(560,535,47,10,fill = 'black',border = 'gray')
        drawRect(300,240,47,10,fill = 'black',border = 'gray')
    if app.currentRoom == 'top':
        drawRect(287,635,97,10,fill = 'black',border = 'gray')
        
    for spike in app.spikes[app.currentRoom]:
        sx,sy,sw= spike
        numSpikes = sw//15
        for i in range(numSpikes):
            x = sx+i*15
            drawPolygon(x,sy,x+7.5,sy-15,x+15,sy,fill = 'black',border = 'gray')
            
    if app.nearShopDoor:
        drawLabel('Press E to Enter Shop', 320,350, fill = 'yellow', size = 16, bold = True)
    if app.nearShopExit:
        drawLabel('Press E to Exit', 125,580, fill = 'yellow', size = 16, bold = True)
    if app.nearShopkeeper and not app.inShop:
        drawLabel('Press F to Shop', 425,560, fill = 'yellow', size = 16, bold = True)
    if app.inShop:
        drawRect(0,0,700,700,fill = 'black', opacity = 80)
        drawLabel('SHOP', 350,100,fill = 'brown', size = 50, bold = True, font = 'monospace')
        drawLabel(f'Coins: {app.coinsCollected}',350,150,fill = 'gold',size = 20, bold = True)
        itemPositions = [(200,250),(500,250),(200,450),(500,450)]
        for i in range(4):
            itemKey = app.shopItemsList[i]
            item = app.shopItems[itemKey]
            x,y = itemPositions[i]
            fillColor = 'darkGray' if item['purchased'] else 'gray'
            borderColor = 'red' if i == app.shopSelectedItem else 'white'
            borderWidth = 3 if i == app.shopSelectedItem else 1
            drawRect(x,y,150,120,fill = fillColor,borderWidth = borderWidth,border = borderColor,align = 'center')
            drawLabel(item['name'],x,y-30,fill = 'white',size = 14, bold = True)
            drawLabel(f"{item['cost']} coins",x,y+10,fill = 'gold',size = 12)
            if item['purchased']:
                drawLine(x-50,y-40,x+50,y+40, fill = 'red',lineWidth = 5)
                drawLine(x+50,y-40,x-50,y+40, fill = 'red',lineWidth = 5)   
        
            
            
        
            
    for coin in app.coins[app.currentRoom]:
        cx,cy = coin
        coinUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/coin_collect_{app.coinFrame:02d}.png'
        drawImage(coinUrl,cx,cy,align = 'center',width = 30,height = 30)
    for collected in app.collectedCoins:
        if collected[2] == app.currentRoom:
            cx,cy,room,frame  = collected
            coinUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/coin_collect_{frame:02d}.png'
            drawImage(coinUrl,cx,cy,align = 'center',width = 30,height = 30)
            
            
        
            
            
            
            
    if app.currentRoom == 'top':
        if app.dragonFacingRight:
            if app.dragonShowingHurt:
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_hurt_{app.dragonFrame:02d}.png'
            elif app.dragonState == 'idle':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_idle_{app.dragonFrame:02d}.png'                
            elif app.dragonState == 'attack':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_attack_{app.dragonFrame:02d}.png'
            elif app.dragonState == 'death':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_death_{app.dragonFrame:02d}.png'# 02d so that frames start like 01 02 03 etc.
            else:
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_walk_{app.dragonFrame:02d}.png'
        else:
            if app.dragonShowingHurt:
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_hurt_left_{app.dragonFrame:02d}.png'
            elif app.dragonState == 'idle':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_idle_left_{app.dragonFrame:02d}.png'
            elif app.dragonState == 'attack':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_attack_left_{app.dragonFrame:02d}.png'
            elif app.dragonState == 'death':
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_death_left_{app.dragonFrame:02d}.png'
            else:
                dragonUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/dragon_walk_left_{app.dragonFrame:02d}.png'
        
        drawImage(dragonUrl,app.dragonX,app.dragonY,align = 'center', width = 200, height = 200)
            
        if app.bossIntroTimer < app.bossIntroLength:
            drawLabel('YOU DARE CHALLENGE ME?', 350, 100, size = 16, fill = 'red')
    if app.knightFacingRight:
        if app.knightState == 'idle':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_idle_{app.knightFrame:02d}.png'
        elif app.knightState == 'jump':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_jump_{app.knightFrame:02d}.png'
        elif app.knightState == 'attack2':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_attack2_{app.knightFrame:02d}.png'
        elif app.knightState == 'attack1':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_attack1_{app.knightFrame:02d}.png'
        elif app.knightState == 'hurt':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_hurt_{app.knightFrame:02d}.png'
        else:
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_walk_{app.knightFrame:02d}.png' 
    else:
        if app.knightState == 'idle':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_idle_left_{app.knightFrame:02d}.png'           
        elif app.knightState == 'jump':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_jump_left_{app.knightFrame:02d}.png'
        elif app.knightState == 'attack2':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_attack2_left_{app.knightFrame:02d}.png'
        elif app.knightState == 'attack1':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_attack1_left_{app.knightFrame:02d}.png'
        elif app.knightState == 'hurt':
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_hurt_left_{app.knightFrame:02d}.png'
        else:
            knightUrl = f'https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/knight_walk_left_{app.knightFrame:02d}.png'
    
    drawImage(knightUrl, app.knightX,app.knightY, align = 'center', width = 100, height = 100)
    
    #proj
    for proj in app.projectiles:
        drawRect(proj[0],proj[1],20,10,fill = 'red',align = 'center')
    
    #Health
    drawRect(50,20,120,15,fill = 'gray',border = 'white',borderWidth = 2)
    drawRect(50,20,app.knightHP*30,15,fill = 'green')
    drawLabel(f'HP: {app.knightHP}/4', 110,12, fill = 'white', size = 14,bold = True)           # Very slight assistance from ai on drawing the healthbar
 
    if app.currentRoom == 'top' and app.dragonHP > 0:
        drawRect(530,20,150,15,fill = 'gray',border = 'white')
        drawRect(530,20,app.dragonHP*10,15,fill = 'red')
        drawLabel(f'Dragon: {app.dragonHP}/15', 605,12, fill = 'white', size = 14,bold = True)
    drawLabel(f'Coins: {app.coinsCollected}',350,680,fill = 'gold',size = 16, bold = True)
        
    
    
def drawRoomBackground(app):
    if app.currentRoom == 'center':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/center.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'top':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/top.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'bottom':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/low.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'left1':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/left1.png',0,0,width = 700,height = 700)                 
    elif app.currentRoom == 'left2':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/left2.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'inside':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/inside.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'right1':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/right1.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'right2':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/right2.png',0,0,width = 700,height = 700)
    elif app.currentRoom == 'right3':
        drawImage('https://raw.githubusercontent.com/oracl8/SlayTheDragon/main/right3.png',0,0,width = 700,height = 700)

def main():
    runApp()
main()

