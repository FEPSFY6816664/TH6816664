import random as r
import math as m
import pygame as pg


ALI = 50
SEP = 0.2
COH = 1

MAXSPEED = 3

HIGHLIGHT = True




vec = pg.Vector2
col = pg.color.Color
rect = pg.Rect
clock = pg.time.Clock()

DIM = vec(500, 500)
BGCOL = col(200, 200, 200)
BOIDCOL = col(0, 0, 0)
BLACK = col(0, 0, 0)
FPS = 60


class boid():
    def __init__(self, pos, simulation, angle = None) -> None:
        self.sim:Simulation = simulation
        self.pos = vec(pos)
        self.angle = (2*m.pi)*r.random()

        self.maxSpeed = MAXSPEED

        try: self.angle = m.radians(angle)
        except: pass

        self.vel = vec(m.cos(self.angle), m.sin(self.angle))
        self.acc = vec(0, 0)
        self.steer = vec(0, 0)

        self.viewRadius = 100
        self.FOV = m.radians(270)


    def update(self):
        self.getAngle()
        self.getLocalBoids()
        self.move()


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


        self.steer = vec(0, 0)
        if self.localBoids != []:
            self.steer += self.ali()*ALI
            self.steer += self.sep()*SEP
            self.steer += self.coh()*COH

        self.steer /= 3

        self.acc = self.steer

        try:self.vel = self.acc
        except: pass

        self.pos += (self.vel + (1/2)*self.acc).normalize()*self.maxSpeed
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
            relativeAngle = m.atan2(vecTo.y, vecTo.x)-self.angle
            if relativeAngle > m.radians(180):
                relativeAngle -= m.radians(360)
            elif relativeAngle < m.radians(-180):
                relativeAngle += m.radians(360)
            isWithin = abs(relativeAngle) < self.FOV/2

            if isClose and isWithin:
                self.localBoids.append(boid)



    def ali(self):
        velSum = vec(0, 0)
        for b in self.localBoids:
            velSum+=b.vel
        return velSum.normalize()


    def coh(self):
        centerOfMass = vec(0, 0)
        for b in self.localBoids:
            centerOfMass += b.pos
        centerOfMass /= len(self.localBoids)
        return centerOfMass-self.pos


    def sep(self):
        sumVecTo = vec(0, 0)
        for b in self.localBoids:
            sumVecTo += b.pos-self.pos
        sumVecAway = sumVecTo*-1
        return sumVecAway






class Simulation():
    def __init__(self) -> None:
        self.running = 1
        self.boids = [boid((r.randint(0, DIM.x), r.randint(0, DIM.y)), self) for i in range(100)]
        self.boids.append(boid(DIM/2, self, 0))
        self.Target = self.boids[-1]

        self.display = pg.display.set_mode(DIM)
        self.mainloop()

    def mainloop(self):
        while self.running:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.close()
                if e.type == pg.MOUSEBUTTONDOWN:
                    self.Target = r.choice(self.boids)

            self.display.fill(BGCOL)

            for boid in self.boids:
                boid.update()

            for boid in self.boids:
                pg.draw.circle(self.display, BOIDCOL, boid.pos, 2)

            if HIGHLIGHT:

                try:
                    pg.draw.arc(self.display, BLACK, rect(self.Target.pos.x-self.Target.viewRadius, self.Target.pos.y-self.Target.viewRadius, self.Target.viewRadius*2, self.Target.viewRadius*2), -self.Target.angle-self.Target.FOV/2, -self.Target.angle+self.Target.FOV/2, 1)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle-self.Target.FOV/2), m.sin(self.Target.angle-self.Target.FOV/2)).normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle+self.Target.FOV/2), m.sin(self.Target.angle+self.Target.FOV/2)).normalize()*self.Target.viewRadius)
                    

                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+self.Target.vel*self.Target.viewRadius)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+self.Target.steer.normalize()*self.Target.viewRadius)



                    pg.draw.line(self.display, col(255, 0, 0), self.Target.pos, self.Target.pos+self.Target.ali().normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, col(0, 255, 0), self.Target.pos, self.Target.pos+self.Target.sep().normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, col(0, 0, 255), self.Target.pos, self.Target.pos+self.Target.coh().normalize()*self.Target.viewRadius)

                    pg.draw.circle(self.display, col(255, 0, 0), self.Target.pos+self.Target.ali()*ALI, 5)
                    pg.draw.circle(self.display, col(0, 255, 0), self.Target.pos+self.Target.sep()*SEP, 5)
                    pg.draw.circle(self.display, col(0, 0, 255), self.Target.pos+self.Target.coh()*COH, 5)

                    pg.draw.line(self.display, col(255, 255, 255), self.Target.pos, self.Target.pos+self.Target.acc)

                    pg.draw.circle(self.display, col(255, 255, 255), self.Target.pos+self.Target.steer/3, 5)

                except:
                    pass

                # for boid in self.Target.localBoids:
                #     pg.draw.line(self.display, col(150, 150, 150), self.Target.pos, boid.pos)
            

            pg.display.update()
            clock.tick(FPS)




    def close(self):
        self.running = 0





if __name__ == '__main__':
    Simulation()