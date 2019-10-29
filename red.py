"""A basic playground. Most interesting function is draw a shape, basically
move the mouse as you want and pymunk will approximate a Poly shape from the
drawing.
"""
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d
import pymunk.util as u

# TODO: Clean up code

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

size_factor = .5;


class PhysicsDemo:
   def flipyv(self, v):
       return int(v.x), int(-v.y + self.h)

   def __init__(self):
       self.running = True
       ### Init pygame and create screen
       pygame.init()
       self.w, self.h = 800, 800
       self.screen = pygame.display.set_mode((self.w, self.h))
       self.clock = pygame.time.Clock()

       ### Init pymunk and create space
       self.space = pm.Space()
       self.space.gravity = (0.0, -990.0)

       ### Walls
       self.walls = []
       self.create_wall_segments([(100, 50), (500, 50)])

       ## Balls
       # balls = [createBall(space, (100,300))]
       self.balls = []

       ### Polys
       self.polys = []
       h = 6
       for y in range(1, h):
           # for x in range(1, y):
           x = 0
           s = 10  # the reason for the bottom line is the when we divide 50/4 it truncates, but for 50/5 it is a good number
           p = Vec2d( (y * s * 1.5 ) + (20/y)/5, 25) + Vec2d(250, 20 + 40/y)
           self.polys.append(self.create_box(p, size=10/y, mass=5))

       p = Vec2d((100 * 2) -40 , 30) + Vec2d(80, 80)
       self.polys.append(self.create_box(p, size=12, mass=5))

       p1 = Vec2d((100 * 2)-40, 30+50) + Vec2d(80, 80 +40)
       self.polys.append(self.create_box(p1, size=12, mass=5))

       p2 = Vec2d(10,650)
       self.balls.append(self.create_ball(p2, .5, 7.0))

       p2 = Vec2d(400, 650)

       moment = pm.moment_for_circle(.5, 0.0, 15)
       ball_body = pm.Body(3, moment)
       ball_body.position = Vec2d(p2)
       ball_body.mass = 2
       ball_body = pm.Body(body_type=pm.Body.STATIC)  # 1
       body = pm.Body(10,100)
       ball_joint = pm.PinJoint(body, ball_body, (0,0), (0,0)) # 3
       ball_shape = pm.Circle(ball_body, 15)
       l1 = pm.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
       l2 = pm.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

       ball_shape.friction = 1.5
       ball_shape.collision_type = COLLTYPE_DEFAULT
       self.space.add(l1, l2, body, ball_joint)
       self.space.add(ball_body, ball_shape)

       self.balls.append(ball_shape)


       #

       # points = [(100, 300), (500, 400)]
       # points = list(map(Vec2d, points))
       # for i in range(len(points) - 1):
       #     v1 = Vec2d(points[i].x - 50, points[i].y)
       #     v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
       #     wall_body = pm.Body(body_type=pm.Body.DYNAMIC)
       #     wall_shape = pm.Segment(wall_body, v1, v2, .0)
       #     wall_shape.friction = 1.0
       #     wall_shape.collision_type = COLLTYPE_DEFAULT
       #     self.space.add(wall_shape)
       #     self.walls.append(wall_shape)

       points = [(450, 40), (500, 80)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       points = [(50, 550), (70, 500)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       points = [(299, 155), (300, 200)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)

           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       self.run_physics = True

       ### Wall under construction
       self.wall_points = []
       ### Poly under construction
       self.poly_points = []

       self.shape_to_remove = None
       self.mouse_contact = None

   def draw_helptext(self):
       font = pygame.font.Font(None, 16)
       text = ["nunu's project"
               ]
       y = 5
       for line in text:
           text = font.render(line, 1, THECOLORS["black"])
           self.screen.blit(text, (5, y))
           y += 10

   def create_ball(self, point, mass=1.0, radius=15.0):
       moment = pm.moment_for_circle(mass, 0.0, radius)
       ball_body = pm.Body(3, moment)
       ball_body.position = Vec2d(point)
       ball_body.mass = 2

       ball_shape = pm.Circle(ball_body, radius)
       ball_shape.friction = 1.5
       ball_shape.collision_type = COLLTYPE_DEFAULT
       #ball_shape.elasticity = 0.0001
       self.space.add(ball_body, ball_shape)
       return ball_shape

   def create_box(self, pos, size, mass=5.0):
       sizex = 3
       if size == 12:
           sizex = 7
       box_points = [(-sizex, -size*4), (-sizex, size*4), (sizex, size*4), (sizex, -size*4)]
       return self.create_poly(box_points, mass=mass, pos=pos)

   def create_poly(self, points, mass=5.0, pos=(0, 0)):

       moment = pm.moment_for_poly(mass, points)
       # moment = 1000
       body = pm.Body(mass, moment)
       body.position = Vec2d(pos)
       shape = pm.Poly(body, points)
       shape.friction = 0.5
       shape.collision_type = COLLTYPE_DEFAULT
       self.space.add(body, shape)
       return shape

   def create_wall_segments(self, points):
       """Create a number of wall segments connecting the points"""
       if len(points) < 2:
           return []
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x-50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7.0
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

   def run(self):
       while self.running:
           self.loop()

   def draw_ball(self, ball):

       body = ball.body
       v = body.position + ball.offset.cpvrotate(body.rotation_vector)
       p = self.flipyv(v)
       r = ball.radius
       pygame.draw.circle(self.screen, THECOLORS["blue"], p, int(r), 2)

   def draw_wall(self, wall):
       body = wall.body
       pv1 = self.flipyv(body.position + wall.a.cpvrotate(body.rotation_vector))
       pv2 = self.flipyv(body.position + wall.b.cpvrotate(body.rotation_vector))
       pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [pv1, pv2])

   def draw_poly(self, poly):
       body = poly.body
       ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
       ps.append(ps[0])
       ps = list(map(self.flipyv, ps))
       if u.is_clockwise(ps):
           color = THECOLORS["green"]
       else:
           color = THECOLORS["red"]
       pygame.draw.lines(self.screen, color, False, ps)

   def draw(self):

       ### Clear the screen
       self.screen.fill(THECOLORS["white"])

       ### Display some text
       self.draw_helptext()

       ### Draw balls
       for ball in self.balls:
           self.draw_ball(ball)

       ### Draw walls
       for wall in self.walls:
           self.draw_wall(wall)

       ### Draw polys
       for poly in self.polys:
           self.draw_poly(poly)

       ### Draw Uncompleted walls
       if len(self.wall_points) > 1:
           ps = [self.flipyv(Vec2d(p)) for p in self.wall_points]
           pygame.draw.lines(self.screen, THECOLORS["gray"], False, ps, 2)

       ### Uncompleted poly
       if len(self.poly_points) > 1:
           ps = [self.flipyv(Vec2d(p)) for p in self.poly_points]
           pygame.draw.lines(self.screen, THECOLORS["red"], False, ps, 2)

       ### Mouse Contact
       if self.mouse_contact is not None:
           p = self.flipyv(self.mouse_contact)
           pygame.draw.circle(self.screen, THECOLORS["red"], p, 3)

       ### All done, lets flip the display
       pygame.display.flip()

   def loop(self):
       for event in pygame.event.get():
           if event.type == QUIT:
               self.running = False
           # elif event.type == KEYDOWN and event.key == K_ESCAPE:
           #     self.running = False
           # elif event.type == KEYDOWN and event.key == K_p:
           #     pygame.image.save(self.screen, "playground.png")

           # elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # LMB
           #     if pygame.key.get_mods() & KMOD_SHIFT:
           #         p = self.flipyv(Vec2d(event.pos))
           #         self.polys.append(self.create_box(pos=p))
           #     else:
           #         # t = -10000
           #         p = self.flipyv(Vec2d(event.pos))
           #         self.balls.append(self.create_ball(p))




       mpos = pygame.mouse.get_pos()

       if pygame.key.get_mods() & KMOD_SHIFT and pygame.mouse.get_pressed()[2]:
           p = self.flipyv(Vec2d(mpos))
           self.poly_points.append(p)
       hit = self.space.point_query_nearest(self.flipyv(Vec2d(mpos)), 0, pm.ShapeFilter())
       if hit != None:
           self.shape_to_remove = hit.shape
       else:
           self.shape_to_remove = None

       ### Update physics
       if self.run_physics:
           x = 1
           dt = 1.0 / 60.0 / x
           for x in range(x):
               self.space.step(dt)
               for ball in self.balls:
                   # ball.body.reset_forces()
                   pass
               for poly in self.polys:
                   # poly.body.reset_forces()
                   pass

       ### Draw stuff
       self.draw()

       ### Check for objects outside of the screen, we can remove those
       # Balls
       xs = []
       for ball in self.balls:
           if ball.body.position.x < -1000 or ball.body.position.x > 1000 \
                   or ball.body.position.y < -1000 or ball.body.position.y > 1000:
               xs.append(ball)
       for ball in xs:
           self.space.remove(ball, ball.body)
           self.balls.remove(ball)

       # Polys
       xs = []
       for poly in self.polys:
           if poly.body.position.x < -1000 or poly.body.position.x > 1000 \
                   or poly.body.position.y < -1000 or poly.body.position.y > 1000:
               xs.append(poly)

       for poly in xs:
           self.space.remove(poly, poly.body)
           self.polys.remove(poly)

       ### Tick clock and update fps in title
       self.clock.tick(50)
       pygame.display.set_caption("fps: " + str(self.clock.get_fps()))


def main():
   demo = PhysicsDemo()
   demo.run()

main()


