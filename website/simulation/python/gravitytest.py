import random as r
import math as m
import pygame as pg





vec = pg.Vector2
col = pg.color.Color
rect = pg.Rect
clock = pg.time.Clock()


DIM = vec(500, 500)
BGCOL = col(200, 200, 200)
BALLCOL = col(0, 0, 0)
BLACK = col(0, 0, 0)

FPS = 60

G = vec(0, 1)
LARGEMASS = DIM/3
LARGEMASS2 = DIM/2+DIM/3

def vecTo(v1, v2):
    return v2-v1




class Ball():
    def __init__(self, pos) -> None:
        self.pos = vec(pos)
        self.vel = vec(10, 0)
        self.acc = vec(0, 0)

    def update(self):
        # self.acc += G

        self.acc += (1/self.pos.distance_to(LARGEMASS))*vecTo(self.pos, LARGEMASS)
        self.acc += (1/self.pos.distance_to(LARGEMASS2))*vecTo(self.pos, LARGEMASS2)

        self.vel += self.acc 
        self.pos += self.vel + (1/2)*self.acc
        self.acc = vec(0, 0)

        if self.pos.x > DIM.x or self.pos.x < 0:
            self.vel.x = -self.vel.x
            if self.pos.x > DIM.x:
                self.pos.x = DIM.x
            else:
                self.pos.x = 0
        elif self.pos.y > DIM.y or self.pos.y < 0:
            self.vel.y = -self.vel.y
            if self.pos.y > DIM.y:
                self.pos.y = DIM.y
            else:
                self.pos.y = 0

        
        
        



class Simulation():
    def __init__(self) -> None:
        self.running = 1

        self.ball = Ball(DIM/2)
        self.display = pg.display.set_mode(DIM)

        self.mainloop()



    def mainloop(self):
        while self.running:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.close()

            self.display.fill(BGCOL)
            
            
            self.ball.update()
            pg.draw.circle(self.display, BALLCOL, self.ball.pos, 5)


            # Acceleration arrow
            pg.draw.line(self.display, col(0, 255, 0), self.ball.pos, self.ball.pos+self.ball.acc)

            # velocity arrow
            pg.draw.line(self.display, col(255, 0, 0), self.ball.pos, self.ball.pos+self.ball.vel)
            
            
            pg.display.update()
            clock.tick(FPS)




    def close(self):
        self.running = 0





if __name__ == '__main__':
    Simulation()