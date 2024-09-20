import pygame
from pygame import mixer
import time
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

#プレイヤー
playerImg = pygame.image.load('rocket.png')
playerX = 284
playerY = 400
playerX_Change = 0
playerY_Change = 0

#敵
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(leftEdge, rightEdge)
enemyY = random.randint(50, 100)
enemyX_Change = 3
enemyY_Change = 30

#弾
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 400
bulletX_Change = 0
bulletY_Change = 3
bulletState = 'ready'

scoreValue = 0

#音声出力
#mixer.sound('').play()

def displayPlayer(x, y):
    screen.blit(playerImg, (x, y))

#関数化したらダメやった．なんでや．
#def movePlayer(playerX, playerX_Change):
#    #プレイヤーを移動
#    newPos = playerX + playerX_Change
#
#    #画面外にはみ出すのを防止
#    if newPos <= leftEdge:
#        newPos = leftEdge
#    elif newPos > rightEdge:
#        newPos = rightEdge
#    return newPos

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

def gameover():
    font = pygame.font.SysFont(None, 84)
    message = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(message, (105, 190))
    pygame.display.update()
    time.sleep(5)

#ゲーム本体
running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (40, 40, 40), (0, 390), (600, 390), 3)
    font = pygame.font.SysFont(None, 24)
    line = font.render("defence line", True, (70, 70, 70))
    screen.blit(line, (10,365))

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

    #プレイヤーを移動
    playerX += playerX_Change

    #画面外にはみ出すのを防止
    if playerX <= leftEdge:
        playerX = leftEdge
    elif playerX > rightEdge:
        playerX = rightEdge

    #敵が一定ラインを越えたらゲームオーバー
    if enemyY > 380:
        gameover()
        break

    #敵の移動
    enemyX += enemyX_Change
    if enemyX <= leftEdge:
        enemyX_Change = 3
        enemyY += enemyY_Change
    elif enemyX >= rightEdge:
        enemyX_Change = -3
        enemyY += enemyY_Change

    #弾の当たり判定
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 400
        bulletState = 'ready'
        scoreValue += 1
        enemyX = random.randint(leftEdge, rightEdge)
        enemyY = random.randint(50, 100)

    #弾がウィンドウ外に行ったら消す
    if bulletY <= 0:
        bulletY = 400
        bulletState = 'ready'

    #発射中の弾があれば進める
    if bulletState == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    #スコア表示
    font = pygame.font.SysFont(None, 32)
    score = font.render("Score :" + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (20,30))

    #プレイヤー，自機の位置(表示)更新
    displayPlayer(playerX, playerY)
    displayEnemy(enemyX, enemyY)

    #スクリーン上のものを更新したときは必ず更新
    pygame.display.update()

pygame.quit()
