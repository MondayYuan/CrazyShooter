import  cv2
import numpy as np
from PIL import ImageGrab
import  pyautogui as pag
import time
from pymouse import PyMouse
import wx

def getMyX(img, y):
    for x in range(img.shape[1]):
        if(img[y][x][0] < 60 and img[y][x][1] < 60 and img[y][x][2] < 60):
            break
    return x + 15

def getEnemyXY(img, myself_x, myself_y):
    center_x = img.shape[1]//2
    if(myself_x < center_x):
        xx = img.shape[1] - 5
    else:
        xx = 5
    groundColor = img[myself_y][xx]
    for y in range(myself_y-5,0,-1):
        if(img[y][xx][0] != groundColor[0] or img[y][xx][1] != groundColor[1] or img[y][xx][2] != groundColor[2]):
            break
    enemy_y = y - 5

    if(myself_x < center_x):
        left = center_x
        right = img.shape[1]
    else:
        left = 0
        right = center_x

    groundColor = img[enemy_y][left+1]
    for x in range(left,right-1,1):
        if(img[enemy_y][x][0] != groundColor[0] or img[enemy_y][x][1] != groundColor[1] or img[enemy_y][x][2] != groundColor[2]):
            break

    enemy_x_left = x

    groundColor = img[enemy_y][right-1]
    for x in range(right-1,left,-1):
        if(img[enemy_y][x][0] != groundColor[0] or img[enemy_y][x][1] != groundColor[1] or img[enemy_y][x][2] != groundColor[2]):
            break

    enemy_x_right = x

    enemy_x = (enemy_x_left + enemy_x_right)//2
    return enemy_x,enemy_y - 45

def isAimed(img,angel,gun_x,gun_y,radius,isMeRight):
    if isMeRight:
        for theta in range(1800,900,-1):
            if(isWhite(getColor(img,[gun_x,gun_y],theta,radius))):
                break
        #if(angel > 180 -theta and angel - 180 + theta < 5):
        if(abs((1800 - theta)/10 -angel) < 1):
            x = int(gun_x + radius * np.cos(theta / 1800 * np.pi))
            y = int(gun_y - radius * np.sin(theta / 1800 * np.pi))
            cv2.circle(img,(x,y),5,[0,0,255],5)
            return  True
    else:
        for theta in range(0,900,1):
            if(isWhite(getColor(img,[gun_x,gun_y],theta,radius))):
                break
        #if (angel - theta < 5 and angel - theta > 0):
        if(abs(angel - theta/10) < 1):
            x = int(gun_x + radius * np.cos(theta / 1800 * np.pi))
            y = int(gun_y - radius * np.sin(theta / 1800 * np.pi))
            cv2.circle(img, (x, y), 5, [0, 0, 255],5)
            return  True

    return False

def isWhite(color):
    if(color[0] > 90 and color[1] > 90 and color[2] > 90 and color[0] + color[1] + color[2] > 550):
        return True
    return False

def getColor(img, center, theta, radiu):
    x = int(center[0] + radiu * np.cos(theta/1800*np.pi))
    y = int(center[1] - radiu * np.sin(theta/1800*np.pi))
    return img[y][x]

def isSeclect(img):
    pass

def closeSeclet():
    pass

def touchScreen():
    mouse.click(lt_x + 300, lt_y + 500)
    #pag.click(lt_x + 300, lt_y + 500)

def screenShot():
    screenshot = ImageGrab.grab((lt_x,lt_y,rb_x,rb_y))
    return np.array(screenshot)

def checkIsAimed(img, angel, gun_x, gun_y, radius, isMeRight):
    if isMeRight:
        x = int(gun_x - np.cos(angel * np.pi /180) * radius)
    else:
        x = int(gun_x + np.cos(angel * np.pi /180) * radius)

    y = int(gun_y - np.sin(angel * np.pi /180) * radius)

    return isWhite(pag.pixel(x, y))




pag.FAILSAFE = True

mouse = PyMouse()

lt_x= 1020
lt_y = 11
rb_x = 1600
rb_y = 770
myself_y = 650

myself_y = myself_y - lt_y
myGun_y = myself_y - 30

while True:
    start = time.clock()
    img = screenShot()
    print('screen time:' + str(time.clock() - start))

    if(isSeclect(img)):
        closeSeclet()

    start = time.clock()
    myself_x = getMyX(img, myself_y)
    print('getMyX time:' + str(time.clock() - start))

    start = time.clock()
    enemy_x, enemy_y = getEnemyXY(img, myself_x, myself_y)
    print('getEnemyXY time:' + str(time.clock() - start))

    start = time.clock()
    cv2.circle(img, (myself_x, myGun_y), 5, [0, 0, 255], 5)
    cv2.circle(img, (enemy_x, enemy_y), 5, [0, 0, 255], 5)
    print('circle time:' + str(time.clock() - start))

    start = time.clock()
    angel = np.arctan(abs((enemy_y - myGun_y) / (enemy_x - myself_x))) * 180 / np.pi
    print('angel time:' + str(time.clock() - start))

    start = time.clock()

    while True:
        start = time.clock()
        flag = checkIsAimed(img,angel,myself_x,myGun_y,65 , myself_x > img.shape[1]//2)
        print('pag time:' + str(time.clock() - start))
        if(flag):
            touchScreen()
            time.sleep(5)
            print('angel:',angel)
            print('sin:',np.sin(angel * 180 / np.pi))
            if myself_x > img.shape[1]//2:
                x = int(myself_x - np.cos(angel * np.pi /180) * 65)
            else:
                x = int(myself_x + np.cos(angel * np.pi /180) * 65)

            y = int(myGun_y - np.sin(angel * np.pi /180) * 65)
            #cv2.circle(img,(x,y),5,[0,0,255],5)
            #cv2.imshow('picture',img)
            #cv2.waitKey()
            break


    '''if(isAimed(img, angel, myself_x, myGun_y, 56, myself_x > img.shape[1] // 2)):
        start = time.clock()
        touchScreen()
        print('click time:' + str(time.clock() - start))
        cv2.imshow('picture', img)
        time.sleep(5)
        cv2.waitKey()
    print('isAimed time:' + str(time.clock() - start))

    start = time.clock()
    cv2.imshow('picture', img)
    print('show time:' + str(time.clock() - start))

    cv2.waitKey(200)'''