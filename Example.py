import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(300,320)
    body.position = x, 550
    shape = pymunk.Circle(body, radius, (0,0))
    space.add(body, shape)
    return shape

def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300,300)

    rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_limit_body.position = (300,300)

    body = pymunk.Body(10, 10000)
    body.position = (300,300)
    l1 = pymunk.Segment(rotation_limit_body, (25, -20), (25, 200.0), 1.0)
    l2 = pymunk.Segment(rotation_limit_body, (-25, -20), (-25, 200.0), 1.0)

    l3 = pymunk.Segment(rotation_limit_body, (25, -20), (85.0, -90.0), 1.3)
    l4 = pymunk.Segment(rotation_limit_body, (-25, -20), (-85.0, -90.0), 1.3)
    # l8 = pymunk.Segment(body, (-150, -200), (150.0, -200.0), 5.0)
    #
    # rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,-200), (0,-200))
    # joint_limit = 25
    # rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,-200), (0,-200), 0, joint_limit)
    l8 = pymunk.Segment(body, (-250, -200), (200.0, -200.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, -200), (0, -200))
    joint_limit = 1
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-20, -200), (0, -200), 0, joint_limit)

    space.add(l1,l2,l3,l4,l8,rotation_limit_body,rotation_center_body, body, rotation_center_joint, rotation_limit_joint)
    return l8

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    lines = add_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25000000000
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill((255,255,255))

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 0:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.debug_draw(draw_options)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()