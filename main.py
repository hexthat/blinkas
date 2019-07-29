import ugame
import stage
import random

class Blinkas(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(bank, 8, x, y)
        self.dx = 0
        self.dy = (ugame.display.height//40)
        self.dead = False

    def update(self, frame):
        super().update()
        if self.dead:
            sprite.set_frame(15, (frame // 4) * 4)
            self.dy = 0
            return
        self.move(self.x + self.dx, self.y + self.dy)
        if not -1 < self.x < (ugame.display.width-15):
            self.dx = -self.dx
        if not -1 < self.y < (ugame.display.height-15):
            self.dy = -self.dy
            if self.frame is 8:
                self.set_frame(10, (frame // 4) * 4)
            elif self.frame is 10:
                self.set_frame(8, (frame // 4) * 4)
        self.set_frame(self.frame, (frame // 4) * 4)
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_DOWN:
            if 0 < self.y < (ugame.display.height-16):
                self.dy = (ugame.display.height//40)
                self.set_frame(8, (frame // 4) * 4)
        elif keys & ugame.K_UP:
            if 0 < self.y < (ugame.display.height-16):
                self.dy = -(ugame.display.height//40)
                self.set_frame(10, (frame // 4) * 4)

    def kill(self):
        if not self.dead:
            sound.play(dead_sound)
        self.dead = True


class Bug(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(bank, (random.randint(2,7)), x, y)
        self.dx = -(blinkas.dy * 2)

    def update(self, frame):
        super().update()
        sprite.set_frame(self.frame, 3)
        self.move(self.x + self.dx, self.y)
        if stage.collide(self.x + 3, self.y + 1, self.x + 13, self.y + 15,
                         blinkas.x + 8, blinkas.y + 8):
            scores()
            sprite.set_frame((random.randint(2,7)), 3)
            self.move((ugame.display.width), (random.randint(0,(ugame.display.height - 12))))
        if self.x <= -(random.randint(16,(ugame.display.width))):
            sprite.set_frame((random.randint(2,7)), 3)
            self.move((ugame.display.width), (random.randint(0,(ugame.display.height - 12))))


class Wall(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(bank, 1, x, y)
        self.dx = -((blinkas.dy * 2) - 0.5)

    def update(self, frame):
        super().update()
        sprite.set_frame(self.frame)
        self.move(self.x + self.dx, self.y)
        if stage.collide(self.x + 3, self.y + 1, self.x + 13, self.y + 15,
                         blinkas.x + 8, blinkas.y + 8):
            blinkas.kill()
            global score
            text.clear()
            text.cursor(0, 0)
            text.move((ugame.display.width//8 - 16), (ugame.display.height//2 - 8))
            text.text("End" + " Score:" + str(score))
            game.render_block()
        if self.x <= -(ugame.display.width//2):
            self.move((ugame.display.width), random.randint(0, (ugame.display.height - 16)))


def scores():
    if not blinkas.dead:
        global score
        text.clear()
        text.cursor(0, 0)
        score += 1
        text.text("Score:" + str(score))
        game.render_block()
        sound.play(eat_sound)


bank = stage.Bank.from_bmp16("bace.bmp")
background = stage.Grid(bank, ugame.display.width//16, ugame.display.height//16)
blinkas = Blinkas((ugame.display.width//16 - 8),(ugame.display.height//2 - 8))
sprites = [blinkas]
for i in range((ugame.display.height//24)):
    i = Bug((ugame.display.width+(random.randint(0,ugame.display.width))), (random.randint(16,(ugame.display.height - 12))))
    sprites += [i]
for i in range((ugame.display.height//16//2 + 1)):
    i = Wall((ugame.display.width), random.randint(0, (ugame.display.height - 16)))
    sprites += [i]
game = stage.Stage(ugame.display, 12)
text = stage.Text(10, 2)
text.move(4, 4)
game.layers = [text] + sprites + [background]
frame = 0
score = 0
text.text("Score:" + str(score))
game.render_block()
eat_sound = open("eat.wav", 'rb')
dead_sound = open("dead.wav", 'rb')
sound = ugame.audio

while True:
    frame = (frame + 1) % 8
    for sprite in sprites:
        sprite.update(frame)
    game.render_sprites(sprites)
    game.tick()
