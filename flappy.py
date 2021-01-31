from pyglet.gl import *
import numpy as np
from pygame.math import Vector2
import random
from pyglet.window import key
import time

disp_width = 1500
disp_height = 900


window = pyglet.window.Window(disp_width, disp_height, 'FLAPPY', resizable=True)

datas = []
outs = []

class flappy:

    def __init__(self, x, y):

        self.position = Vector2(x, y)

        flap = pyglet.resource.image('assets/bluebird-downflap.png')
        flap2 = pyglet.resource.image('assets/bluebird-midflap.png')
        flap3 = pyglet.resource.image('assets/bluebird-upflap.png')

        width, height = flap.width * 2.3 , flap.height * 2.3
        flap.width, flap.height = width, height
        flap2.width, flap2.height = width, height
        flap3.width, flap3.height = width, height


        self.flap_num = 0
        self.rotation = 0

        self.flaps = [
            pyglet.sprite.Sprite(flap , x = self.position.x, y = self.position.y),
            pyglet.sprite.Sprite(flap2, x=self.position.x, y=self.position.y),
            pyglet.sprite.Sprite(flap3, x=self.position.x, y=self.position.y)
        ]

    def draw(self):
        self.flaps[self.flap_num].update(y = self.position.y, rotation= self.rotation)
        self.flaps[self.flap_num].draw()
        self.flap_num = (self.flap_num + 1) % 3


class pipes:

    def __init__(self):

        self.pipe_up = pyglet.resource.image("assets/pipe-green_up.png")
        self.pipe_down = pyglet.resource.image("assets/pipe-green_down.png")

        width, height = 200, 600
        self.pipe_up.width, self.pipe_up.height = width, height
        self.pipe_down.width, self.pipe_down.height = width, height

        self.xs = np.array([[disp_width , disp_width]])
        self.ys = np.array([[-300, -300  + self.pipe_up.height + 300 ]])

        self.pipes = [[pyglet.sprite.Sprite(self.pipe_up, x=self.xs[0][0], y=self.ys[0][0]),
                       pyglet.sprite.Sprite(self.pipe_down, x=self.xs[0][1], y=self.ys[0][1])]]

        self.puan = 0


    def draw(self):
        for i in range(len(self.pipes)):
            self.pipes[i][0].update(x = self.xs[i][0])
            self.pipes[i][1].update(x = self.xs[i][1])
            self.pipes[i][0].draw()
            self.pipes[i][1].draw()



    def add_pip(self):
        rd = random.randint(- self.pipe_up.height , 0)
        rd2 = random.randint(250, 350)
        ys = np.array([[rd, rd  + self.pipe_up.height + rd2]])
        xs = np.array([[disp_width, disp_width]])
        self.pipes += [[pyglet.sprite.Sprite(self.pipe_up, x=xs[0][0], y=ys[0][0]),
                       pyglet.sprite.Sprite(self.pipe_down, x=xs[0][1], y=ys[0][1])]]

        self.ys = np.concatenate((self.ys , ys))
        self.xs = np.concatenate((self.xs, xs))


    def delete_pip(self):
        if self.xs[0][0] + self.pipe_up.width <= 0 :
            self.pipes = self.pipes[1:]
            self.xs = self.xs[1:]
            self.ys = self.ys[1:]
            self.puan += 1


my_flappy = flappy(100, disp_height / 2)
my_pipes = pipes()
gravity = 0
space, nsp = False, True
game_on = False

label = pyglet.text.Label("puan : 0",
                          font_name='Times New Roman',
                          font_size=24,
                          x=disp_width - 100, y=disp_height - 50,
                          anchor_x='center', anchor_y='center')

bg = pyglet.resource.image('assets/background-day.png')

bg.height, bg.width = bg.height * 2, bg.width * 6

a = 150

@window.event
def on_key_press(symbol, modefier):

    global space, game_on
    if symbol == key.SPACE:
        space = True
        game_on = True


@window.event
def on_key_release(symbol, modefier):
    global space, nsp
    if symbol == key.SPACE:
        space = False
        nsp = True


@window.event
def on_draw():
    bg.blit(0,0)
    my_flappy.draw()
    my_pipes.draw()
    label.text = "puan : " + str(my_pipes.puan)
    label.draw()


def run(dt):

    global gravity, nsp, my_pipes, my_flappy, game_on, datas, outs, a

    if game_on:
        my_pipes.xs += -8

        if my_pipes.xs[len(my_pipes.xs) - 1][0] <= 500:
            my_pipes.add_pip()

        for i in range(len(my_pipes.xs)):
            if my_pipes.xs[i][0] <= my_flappy.position.x + my_flappy.flaps[0].width and my_flappy.position.x <= \
                    my_pipes.xs[i][0] + my_pipes.pipe_up.width:
                if my_pipes.ys[i][0] + my_pipes.pipe_up.height <= my_flappy.position.y and my_flappy.position.y + \
                        my_flappy.flaps[0].height <= my_pipes.ys[i][1]:
                    pass

                else:

                    del my_pipes, my_flappy
                    my_pipes, my_flappy = pipes(), flappy(100, disp_height / 2)
                    time.sleep(1.0)
                    game_on = False
                    gravity = 0
                    break

        if (space and nsp):
            gravity = -12
            my_flappy.rotation = -4
            nsp = False

        for i in range(len(my_pipes.xs)):

            if my_pipes.xs[i][1] + my_pipes.pipe_up.width >= my_flappy.position.y:

                dat = [
                    gravity,
                    my_flappy.position.y + my_flappy.flaps[0].height / 2,
                    my_pipes.ys[i][0] + my_pipes.pipe_up.height,
                    my_pipes.ys[i][1],
                    my_flappy.position.y  - (my_pipes.ys[i][0] + my_pipes.pipe_up.height),
                    my_pipes.ys[i][1] - (my_flappy.position.y + my_flappy.flaps[0].height),
                    my_pipes.xs[i][0] - (my_flappy.position.x + my_flappy.flaps[0].width),
                    my_pipes.xs[i][1] - (my_flappy.position.x + my_flappy.flaps[0].width),
                    abs(my_pipes.ys[i][0] + my_pipes.pipe_up.height - my_pipes.ys[i][1]),
                    my_pipes.ys[i][1]  >= a + my_flappy.position.y + my_flappy.flaps[0].height
                ]

                datas += [dat]
                outs += [space]

                break


        gravity += 0.5
        my_flappy.rotation += 0.5
        my_flappy.position.y += -gravity

        my_pipes.delete_pip()


pyglet.clock.schedule_interval(run, 1 / 120)
pyglet.app.run()

#np.save("datas",np.array(datas).reshape(-1,10))
#np.save("outs", np.array(outs).reshape(-1,))



