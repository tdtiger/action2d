import pygame
from pygame import mixer
import random
import math

#プログラムの初めに必ず初期化
pygame.init()
#ウィンドウの大きさ，名前設定
screen = pygame.display.set_mode((600, 450))

#画面の左端，右端(画像が32×32なことを考慮)
leftEdge = 0
rightEdge = 568
#背景色の設定
screen.fill((0, 0, 0))
pygame.display.set_caption('action2d')

#画像読み込み
playerImg = pygame.image.load('rocket.png')
playerX = 284
playerY = 400
#移動度合い
playerX_Change = 0
playerY_Change = 0

enemyImg = pygame.image.load('rocket.png')
enemyX = random.randint(leftEdge, rightEdge)
enemyY = random.randint(50, 100)
enemyX_Change = 3
enemyY_Change = 30

bulletImg = pygame.image.load('rocket.png')
bulletX = 0
bulletY = 400
bulletX_Change = 0
bulletY_Change = 3
bulletState = 'ready'

scoreValue = 0

#音声出力
#mixer.sound('').play()

#プレイヤーを表示する関数
def displayPlayer(x, y):
    screen.blit(playerImg, (x, y))

def movePlayer(playerX, playerX_Change):
    #プレイヤーを移動
    newPos = playerX + playerX_Change

    #画面外にはみ出すのを防止
    if newPos <= leftEdge:
        newPos = leftEdge
    elif newPos > rightEdge:
        newPos = rightEdge
    return newPos

def displayEnemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

#ゲーム本体
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        #QUIT = ウィンドウの×ボタンが押された時
        if event.type == pygame.QUIT:
            running = False

        #キーが押された時
        if event.type == pygame.KEYDOWN:
            #左キーが押された時
            if event.key == pygame.K_LEFT:
                playerX_Change = -1.5
            #右キーが押された時
            elif event.key == pygame.K_RIGHT:
                playerX_Change = 1.5
            #スペースキーが押された時
            elif event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        #キーが離された時
        if event.type == pygame.KEYUP:
            #左キーか右キーが押された時
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_Change = 0

        playerX = movePlayer(playerX, playerX_Change)

    #敵が一定ラインを越えたらゲームオーバー
    if enemyY > 380:
        break

    enemyX += enemyX_Change
    if enemyX <= leftEdge:
        enemyX_Change = 3
        enemyY += enemyY_Change
    elif enemyX >= rightEdge:
        enemyX_Change = -3
        enemyY += enemyY_Change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 400
        bulletState = 'ready'
        scoreValue += 1
        enemyX = random.randint(leftEdge, rightEdge)
        enemyY = random.randint(50, 100)

    if bulletY <= 0:
        bulletY = 400
        bulletState = 'ready'

    if bulletState == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change


    font = pygame.font.SysFont(None, 32)
    score = font.render("Score :" + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (20,30))

    displayPlayer(playerX, playerY)
    displayEnemy(enemyX, enemyY)

    #スクリーン上のものを更新したときは必ず更新
    pygame.display.update()

pygame.quit()
