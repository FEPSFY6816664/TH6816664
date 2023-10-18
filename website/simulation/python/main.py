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
FPS = 30


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
        self.acc = vec(0, 0)

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


        self.acc = vec(0, 0)
        if self.localBoids != []:
            self.acc += self.ali()*ALI
            self.acc += self.sep()*SEP
            self.acc += self.coh()*COH

        self.acc /= 3

        # self.acc = self.acc

        try:
            self.vel = self.vel.normalize()
            self.vel += self.acc
            offs = (self.vel + (1/2)*self.acc).normalize()*self.maxSpeed
        except: pass



        self.pos += offs
        self.acc = vec(0, 0)
        
        wrap()


    def getAngle(self):
        self.angle = m.atan2(self.vel.y, self.vel.x)
            

    def getLocalBoids(self):
        self.localBoids: list[boid] = []
        for b in self.sim.boids:
            if b == self:
                continue

            sumPos = b.pos-self.pos
            dist = m.sqrt(sumPos.x**2 + sumPos.y**2)
            isClose = dist < self.viewRadius

            vecTo = b.pos-self.pos
            relativeAngle = m.atan2(vecTo.y, vecTo.x)-self.angle
            if relativeAngle > m.radians(180):
                relativeAngle -= m.radians(360)
            elif relativeAngle < m.radians(-180):
                relativeAngle += m.radians(360)
            isWithin = abs(relativeAngle) < self.FOV/2

            if isClose and isWithin:
                self.localBoids.append(b)



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
        return (centerOfMass-self.pos).normalize()


    def sep(self):
        sumVecTo = vec(0, 0)
        for b in self.localBoids:
            sumVecTo += b.pos-self.pos
        sumVecAway = sumVecTo*-1
        return sumVecAway.normalize()






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
                    print(self.Target.pos, self.Target.vel, self.Target.acc)

                    pg.draw.arc(self.display, BLACK, rect(self.Target.pos.x-self.Target.viewRadius, self.Target.pos.y-self.Target.viewRadius, self.Target.viewRadius*2, self.Target.viewRadius*2), -self.Target.angle-self.Target.FOV/2, -self.Target.angle+self.Target.FOV/2, 1)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle-self.Target.FOV/2), m.sin(self.Target.angle-self.Target.FOV/2)).normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+vec(m.cos(self.Target.angle+self.Target.FOV/2), m.sin(self.Target.angle+self.Target.FOV/2)).normalize()*self.Target.viewRadius)
                    

                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+self.Target.vel*self.Target.viewRadius)
                    pg.draw.line(self.display, BLACK, self.Target.pos, self.Target.pos+self.Target.acc.normalize()*self.Target.viewRadius)



                    pg.draw.line(self.display, col(255, 0, 0), self.Target.pos, self.Target.pos+self.Target.ali().normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, col(0, 255, 0), self.Target.pos, self.Target.pos+self.Target.sep().normalize()*self.Target.viewRadius)
                    pg.draw.line(self.display, col(0, 0, 255), self.Target.pos, self.Target.pos+self.Target.coh().normalize()*self.Target.viewRadius)

                    pg.draw.circle(self.display, col(255, 0, 0), self.Target.pos+self.Target.ali()*ALI, 5)
                    pg.draw.circle(self.display, col(0, 255, 0), self.Target.pos+self.Target.sep()*SEP, 5)
                    pg.draw.circle(self.display, col(0, 0, 255), self.Target.pos+self.Target.coh()*COH, 5)

                    pg.draw.line(self.display, col(255, 255, 255), self.Target.pos, self.Target.pos+self.Target.acc)

                    pg.draw.circle(self.display, col(255, 255, 255), self.Target.pos+self.Target.acc/3, 5)


                except:
                    pass
            

            pg.display.update()
            clock.tick(FPS)




    def close(self):
        self.running = 0





if __name__ == '__main__':
    Simulation()