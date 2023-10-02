import random as r
import math as m
import pygame as pg





vec = pg.Vector2
col = pg.color.Color
clock = pg.time.Clock()

DIM = vec(500, 500)
BGCOL = col(200, 200, 200)
BOIDCOL = col(0, 0, 0)

FPS = 30





class boid():
    def __init__(self, pos, simulation) -> None:
        self.sim:Simulation = simulation
        self.pos = vec(pos)

        angle = (2*m.pi)*r.random()

        self.vel = vec(m.cos(angle), m.sin(angle))
        self.acc = vec(0, 0)

    def update(self):
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



        self.vel += self.acc
        self.pos += self.vel + (1/2)*self.acc
        self.acc = vec(0, 0)
        #
        wrap()


    def getLocalBoids(self):
        self.localBoids = []
        for boid in self.sim.boids:
            if boid == self:
                continue
            ## a^^2 + b^^2 = c^^2
            dist = m.sqrt(vec(self.pos-boid.pos)**2)
            if dist < 50:
                self.localBoids.append(boid)



    def ali(self):
        

        pass


    def sep(self):
        pass

    def coh(self):
        pass





class Simulation():
    def __init__(self) -> None:
        self.running = 1
        self.boids = [boid((r.randint(0, DIM.x), r.randint(0, DIM.y)), self) for i in range(100)]


        self.display = pg.display.set_mode(DIM)


        self.mainloop()

    def mainloop(self):
        while self.running:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.close()

            self.display.fill(BGCOL)


            for boid in self.boids:
                boid.update()

            for boid in self.boids:
                pg.draw.circle(self.display, BOIDCOL, boid.pos, 3)

            

            pg.display.update()
            clock.tick(FPS)




    def close(self):
        self.running = 0





if __name__ == '__main__':
    Simulation()