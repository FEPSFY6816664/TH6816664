import random as r
import math as m
import pygame as pg





vec = pg.Vector2
col = pg.color.Color
rect = pg.Rect
clock = pg.time.Clock()

DIM = vec(500, 500)
BGCOL = col(200, 200, 200)
BOIDCOL = col(0, 0, 0)
BLACK = col(0, 0, 0)

FPS = 30


class boid():
    def __init__(self, pos, simulation, angle = None) -> None:
        self.sim:Simulation = simulation
        self.pos = vec(pos)

        self.angle = (2*m.pi)*r.random()

        try:
            self.angle = m.radians(angle)
        except:pass

        self.vel = vec(m.cos(self.angle), m.sin(self.angle))
        self.acc = vec(0, 0)

        self.viewRadius = 75
        self.FOV = m.radians(270)


    def update(self):
        #self.getAngle()
        self.getLocalBoids()
        # self.move()

    def move(self):
        def wrap():
            if self.pos.x > DIM.x:
                self.pos.x -= DIM.x
            elif self.pos.x < 0:
                self.pos.x += DIM.x
            if self.pos.y > DIM.y:
                self.pos.y -=DIM.y
            elif self.pos.y < 0:
                self.pos.y += DIM.y

        self.vel += self.acc
        self.pos += self.vel + (1/2)*self.acc
        self.acc = vec(0, 0)
        
        wrap()

    def getAngle(self):
        self.angle = m.atan2(self.vel.y, self.vel.x)
            


    def getLocalBoids(self):
        self.localBoids = []
        for boid in self.sim.boids:
            if boid == self:
                continue

            sumPos = boid.pos-self.pos
            dist = m.sqrt(sumPos.x**2 + sumPos.y**2)
            isClose = dist < self.viewRadius

            vecTo = boid.pos-self.pos
            angleTo = m.atan2(vecTo.y, vecTo.x)
            relativeAngle = angleTo-self.angle
            if relativeAngle > m.radians(180):
                relativeAngle -= m.radians(360)
            elif relativeAngle < m.radians(-180):
                relativeAngle += m.radians(360)
            isWithin = -self.FOV/2 < abs(relativeAngle) < self.FOV/2

            if isClose and isWithin:
                self.localBoids.append(boid)





class Simulation():
    def __init__(self) -> None:
        self.running = 1
        self.boids = [boid(vec(m.cos(m.radians(i))*50, m.sin(m.radians(i))*50)+DIM/2, self) for i in range(360)]
        self.boids.append(boid(DIM/2, self, 0))
        self.Target = self.boids[-1]


        self.display = pg.display.set_mode(DIM)


        self.mainloop()

    def mainloop(self):
        while self.running:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.close()
                if e.type == pg.MOUSEWHEEL:
                    print(e)
                    self.Target.angle += m.radians(e.y)

            self.display.fill(BGCOL)


            for boid in self.boids:
                boid.update()

            for boid in self.boids:
                pg.draw.circle(self.display, BOIDCOL, boid.pos, 2)

            
            pg.draw.arc(self.display, BLACK, rect(self.Target.pos.x-self.Target.viewRadius, self.Target.pos.y-self.Target.viewRadius, self.Target.viewRadius*2, self.Target.viewRadius*2), -self.Target.angle-self.Target.FOV/2, -self.Target.angle+self.Target.FOV/2, 1)
            pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle-self.Target.FOV/2), m.sin(self.Target.angle-self.Target.FOV/2)).normalize()*self.Target.viewRadius)
            pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle+self.Target.FOV/2), m.sin(self.Target.angle+self.Target.FOV/2)).normalize()*self.Target.viewRadius)
            
            for boid in self.Target.localBoids:
                pg.draw.circle(self.display, col(0, 255, 0), boid.pos, 2)

            
            
            pg.display.update()
            clock.tick(FPS)




    def close(self):
        self.running = 0





if __name__ == '__main__':
    Simulation()