import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def cheak_bound(obj_rct: pg.Rect):
    """ 引数：こうかとんレクト＆爆弾レクト
    戻り値：タプル（横方向の判定結果、縦方向の判定結果"""
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img2 = pg.image.load("ex02/fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    bd_img = pg.Surface((20, 20))
    pg.draw.circle(bd_img, (255, 0, 0),(10, 10), 10)
    bd_img.set_colorkey((0, 0, 0))
    bd_rct = bd_img.get_rect()
    x, y = random.randint(0,WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)
    vx, vy = 0, 0
    vx += 5
    vy += 5
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバ")
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img2, kk_rct)
            pg.display.update()
            return

        screen.blit(bg_img, [0, 0])
        """こうかとん"""
        key_list = pg.key.get_pressed()
        sum_move = [0, 0]
        for key, mv in delta.items():
            if key_list[key]:
                sum_move[0] += mv[0]
                sum_move[1] += mv[1]

        accs = [a for a in range(1, 11)] #爆弾の加速度のリスト
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)] #爆弾のスピードが速くなる
        bb_img = bb_imgs[min(tmr//500, 9)]

        kk_rct.move_ip(sum_move[0], sum_move[1])
        if cheak_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_move[0], -sum_move[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(avx, avy)
        yoko, tate = cheak_bound(bd_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    