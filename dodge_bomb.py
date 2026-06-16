import os
import random
import sys
import pygame as pg
import time
import math

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),  
    pg.K_RIGHT: (+5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  
        tate = False
    return yoko, tate
def calc_orientation(
    org: pg.Rect,
    dst: pg.Rect
) -> tuple[float, float]:
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery

    norm = math.sqrt(dx**2 + dy**2)

    return dx / norm, dy / norm
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    img = pg.transform.rotozoom(
        pg.image.load("fig/3.png"),
        0,
        0.9
    )

    return {
        (0, 0): img,
        (-5, 0): img,
        (5, 0): pg.transform.flip(img, True, False),
        (0, -5): pg.transform.rotozoom(img, -90, 1.0),
        (0, 5): pg.transform.rotozoom(img, 90, 1.0),
        (-5, -5): pg.transform.rotozoom(img, -45, 1.0),
        (-5, 5): pg.transform.rotozoom(img, 45, 1.0),
        (5, -5): pg.transform.flip(
            pg.transform.rotozoom(img, -45, 1.0),True,False),
        (5, 5): pg.transform.flip(
            pg.transform.rotozoom(img, 45, 1.0),True,False),
    }
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []

    for r in range(1, 11):
        img = pg.Surface((20*r, 20*r))
        pg.draw.circle(
            img,
            (255, 0, 0),
            (10*r, 10*r),
            10*r
        )
        img.set_colorkey((0, 0, 0))
        bb_imgs.append(img)

    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs
def gameover(screen: pg.Surface) -> None:
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(200)

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2, HEIGHT//2)

    cry_img = pg.transform.rotozoom(
    pg.image.load("fig/8.png"),
    0,
    0.9
)

    left_rct = cry_img.get_rect()
    right_rct = cry_img.get_rect()


    left_rct.center = (WIDTH//2 - 250, HEIGHT//2)
    right_rct.center = (WIDTH//2 + 250, HEIGHT//2)

    black.blit(cry_img, left_rct)
    black.blit(txt, txt_rct)
    black.blit(cry_img, right_rct)

    screen.blit(black, (0, 0))
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgs = get_kk_imgs()
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_img = pg.Surface((20, 20)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() 
    bb_rct.centerx = random.randint(0, WIDTH) 
    bb_rct.centery = random.randint(0, HEIGHT) 
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  
                sum_mv[1] += mv[1] 
        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  
        screen.blit(kk_img, kk_rct)
        idx = min(tmr // 500, 9)

        bb_img = bb_imgs[idx]

        bb_rct.width = bb_img.get_width()
        bb_rct.height = bb_img.get_height()

        vx = vx * bb_accs[idx]
        vy = vy * bb_accs[idx]
        vx, vy = calc_orientation(bb_rct, kk_rct)

        bb_rct.move_ip(vx * 5, vy * 5)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()