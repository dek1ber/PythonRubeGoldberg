import math, sys, random

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util


def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], THECOLORS["black"], p, r, 1)

def add_L(space):
    # """Add a inverted L shape with two joints"""
    # rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    # rotation_center_body.position = (300,300)
    #
    # rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    # rotation_limit_body.position = (200,300)
    #
    # body = pymunk.Body(10, 10000)
    # body.position = (250,300)
    # l1 = pymunk.Segment(body, (-50, 200), (100.0, 200.0), 1)
    # l2 = pymunk.Segment(body, (100.0, 200), (100.0, 250.0), 1)
    #
    # rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    # joint_limit = 125
    # rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-50,0), (0,0), 0, joint_limit)
    #
    # space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    # return l1,l2
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(10, 10000)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-100, 125), (100.0, 125.0), 1)
    l2 = pymunk.Segment(body, (100.0, 125), (100.0, 150.0), 1)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 25), (0, 25))
    joint_limit = 200
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-150, 125), (0, 125), 0, joint_limit)

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1, l2


def main():
    global contact
    global shape_to_remove

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
    ## Balls

    lines = add_L(space)

    balls = []

    ### walls
    static_lines = [pymunk.Segment(space.static_body, (10.0, 575.0), (150.0, 475.0), 5)]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position = (300, 300)

    # skiLift = [pymunk.Segment(space.static_body, (300.0, 500.0), (450.0, 475.0), 5.0), pymunk.Segment(space.static_body, (450.0, 475.0), (450.0, 525.0), 5.0)]

    # for l in skiLift:
    #     l.friction = 0.5
    # space.add(skiLift)


    body = pymunk.Body(10, 10000)
    body.position = (300, 300)
    # l1 = pymunk.Segment(rotation_limit_body, (25, -20), (25, 100.0), 1.0)
    # l2 = pymunk.Segment(rotation_limit_body, (-25, -20), (-25, 100.0), 1.0)
    #
    # l3 = pymunk.Segment(rotation_limit_body, (25, -20), (85.0, -100.0), 1.3)
    # l4 = pymunk.Segment(rotation_limit_body, (-25, -20), (-85.0, -100.0), 1.3)
    # # l8 = pymunk.Segment(body, (-150, -200), (150.0, -200.0), 5.0)
    # #
    # # rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,-200), (0,-200))
    # # joint_limit = 25
    # # rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,-200), (0,-200), 0, joint_limit)
    # l8 = pymunk.Segment(body, (-100, -200), (100.0, -200.0), 5.0)
    #
    # rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, -200), (0, -200))
    # joint_limit = 1
    # rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-20, -200), (0, -200), 0, joint_limit)
    #
    # space.add(l1, l2, l3, l4, l8, rotation_limit_body, rotation_center_body, body, rotation_center_joint,
    #           rotation_limit_joint)

    ticks_to_next_ball = 1

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "contact_with_friction.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball == 0:
            ticks_to_next_ball = 0
            mass = 0.5
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            # x = random.randint(50, 200)
            body.position = 30, 650
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.friction = 0.5
            space.add(body, shape)
            balls.append(shape)

        ### Clear screen
        screen.fill(THECOLORS["white"])

        ### Draw stuff
        space.debug_draw(draw_options)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        # Make body for pulley

        # Update physics
        ## Balls

        ### walls

        ### Draw stuff
        # balls_to_remove = []
        # for ball in balls:
        #     if ball.body.position.y > 400: balls_to_remove.append(ball)
        #     p = tuple(map(int, ball.body.position))
        #     pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)
        #
        # for ball in balls_to_remove:
        #     space.remove(ball, ball.body)
        #     balls.remove(ball)
        #
        # for line in static_lines:
        #     body = line.body
        #     p1 = body.position + line.a.rotated(body.angle)
        #     p2 = body.position + line.b.rotated(body.angle)
        #     pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1, p2])

        ## Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("Rube Goldberg")


if __name__ == '__main__':
    sys.exit(main())
