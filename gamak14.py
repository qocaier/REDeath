import csv
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime as dt
import wave
import pygame
import sys
import os
import tkinter.filedialog


pygame.mixer.init()


def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=[("Text level files", "*.txt")])
    top.destroy()
    return file_name


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def duration(file):
    spf = wave.open(f"music/wav/{file[:-3]}wav", "r")
    fs = spf.getnframes()
    rate = spf.getframerate()
    dur = fs / float(rate)
    return dur


def inland(name):
    if os.path.exists(f"data/lvl/{name[:-3]}png"):
        pass

    else:
        mpl.use('TkAgg')

        spf = wave.open(f"music/wav/{name[:-3]}wav", "r")

        # Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        fs = spf.getnframes()
        rate = spf.getframerate()
        dur = fs / float(rate)
        print(dur)

        # If Stereo
        if spf.getnchannels() == 2:
            print("Just mono files")
            sys.exit(0)

        Time = np.linspace(0, len(signal) / rate, num=len(signal))

        mpl.rcParams['agg.path.chunksize'] = 10000

        plt.figure(1, figsize=(round(dur / 10), 1), edgecolor='black')
        plt.axis('off')
        plt.plot(Time, signal)
        plt.savefig(f"data/lvl/{name[:-3]}png", dpi=1000, edgecolor='black', bbox_inches='tight',
                    transparent=True)
        plt.close(1)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('zastavka2.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    smallfont = pygame.font.SysFont('Segoe UI Semibold', 28)
    text = smallfont.render('Играть', True, '#000000')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            mouse = pygame.mouse.get_pos()
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, '#D72D2E', [width / 2, height / 2, 140, 40])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            else:
                pygame.draw.rect(screen, '#357B45', [width / 2, height / 2, 140, 40])
            screen.blit(text, (width / 2 + 50, height / 2))

        pygame.display.flip()
        clock.tick(fps)


def save():
    with open(f"data/{dt.datetime.now().strftime('%d_%m_%Y %H_%M_%S')} save.txt", 'w') as f:
        f.write(';'.join([str(player.rect.x), str(player.rect.y), str(player.health)]) + '\n')
        f.write(';'.join([str(camera.dx), str(camera.dy), str(camera.smx), str(camera.smy)]) + '\n')
        f.write(';'.join([str(pygame.mixer.music.get_pos()), mus_now,
                          str(mountain.rect.x), str(mountain.rect.y)]) + '\n')
        print(mus_now)
        for j in z_list:
            f.write(';'.join([j.sheet, str(j.rect.x), str(j.rect.y), str(j.health)]) + '\n')
        f.close()


def load_save():
    global player, z_list, zapusheno, camera, mountain
    fn = prompt_file()
    if fn != '':
        with open(fn, 'r') as f:
            li = f.readlines()
            pldt = li[0].split(';')
            player.kill()
            player.skl.kill()
            player = Landing(int(pldt[0]), int(pldt[1]), 50)
            player.health = int(pldt[2])

            pldt = li[1].split(';')
            camera = Camera(int(pldt[0]), int(pldt[1]), int(pldt[2]), int(pldt[3]))

            pldt = li[2].split(';')
            mountain.upd(pldt[1], int(pldt[2]), int(pldt[3]))
            pygame.mixer.music.play(start=(int(pldt[0]) / 1000))

            for o in z_list:
                o.kill()
                o.skl.kill()
            z_list = []
            for j in range(3, len(li) - 1):
                pldt = li[j].split(';')
                z_list.append(Zombie(pldt[0], 7, 1, int(pldt[1]), int(pldt[2])))
                z_list[j - 3].health = int(pldt[3])
            f.close()

            for group in notallll:
                for sprite in group:
                    camera.apply(sprite)

            return True
    else:
        return False


# def choose_lvl():



class Day:
    def __init__(self):
        self.r = 210
        self.g = 210
        self.b = 255
        self.frame = 0
        self.kra = 1
        self.sin = 0
        self.zel = 1
        self.noch = False
        self.time = 0

    def color(self):
        self.frame += 1
        self.frame %= 4
        if self.frame == 0:
            self.time += 1
            self.time %= 360
            if self.r == 15:
                self.noch = True

            if self.r == 255:
                self.kra = -1
            elif self.r == 25:
                self.kra = 1

            if self.g == 255:
                self.zel = -1
            elif self.g == 25:
                self.zel = 1

            if self.b == 255:
                self.sin = -1
            elif self.b == 25:
                self.sin = 1

            self.r += self.kra
            self.g += self.zel
            self.b += self.sin
        return tuple([self.r, self.g, self.b])


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, dx, dy, smx, smy):
        self.dx = dx
        self.dy = dy
        self.smx = smx
        self.smy = smy

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target, x, y):
        self.smx += x
        self.smy += y
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2 - self.smx)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2 - self.smy)

    def move(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy


class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(another)
        self.image = load_image("lvl/fi.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        # self.rect.x, self.rect.y = x, y
        # self.rect.bottom = height

    def upd(self, name, x, y):
        super().__init__(another)
        self.image = load_image(f"lvl/{name[:-3]}png")
        # colouredImage = pygame.Surface(self.image.get_size())
        # colouredImage.fill([255, 0, 0])
        #
        # finalImage = self.image.copy()
        # finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
        # self.image = finalImage

        # self.image = pygame.Surface(self.image.get_size())
        # self.image.fill([255, 0, 0])
        # self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        self.rect = self.image.get_rect()
        print(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect.bottom = height
        self.rect.x, self.rect.y = x, y
        pygame.mixer.music.load(f"music/mp3/{name}")
        pygame.mixer.music.play()

    def update(self):
        for j in range(len(zapusheno)):
            if pygame.sprite.collide_mask(self, zapusheno[j]):
                zapusheno.pop(j)
                break


class Pula(pygame.sprite.Sprite):
    def __init__(self, pos, napr):
        super().__init__(another)
        self.image = load_image("pistol_bullet.png")
        if not napr:
            self.image = pygame.transform.flip(self.image, True, False)
        self.napr = napr
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.cosn = False
        vystrel.play()

    def update(self):
        for j in range(len(z_list)):
            if pygame.sprite.collide_mask(self, z_list[j]):
                self.cosn = True
            if z_list[j].health == 0:
                z_list.pop(j)
                zdeat.play()
                break
        if not (pygame.sprite.collide_mask(self, mountain) or self.cosn):
            if self.napr:
                self.rect = self.rect.move(10, 0)
            else:
                self.rect = self.rect.move(-10, 0)
        else:
            self.kill()


class Shkala(pygame.sprite.Sprite):
    def __init__(self, pos, hp, size, is_replacable):
        if is_replacable:
            super().__init__(shkales)
        else:
            super().__init__(dismov_shkales)
        self.image = pygame.Surface(size)
        self.image.fill('dark red')
        pygame.draw.rect(self.image, [255, 0, 0], [2, 2, 50, 5], 0)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.hp = hp

    def update(self, pos, health):
        self.image.fill('dark red')
        pygame.draw.rect(self.image, [255, 0, 0], [2, 2, round(health / self.hp * 50), 5], 0)
        self.rect.center = [pos[0], pos[1] - 50]

    def update_hero(self, health):
        self.image.fill('dark red')
        pygame.draw.rect(self.image, [255, 0, 0], [8, 8, round(health / self.hp * 200), 20], 0)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(zombies)
        self.frames = []
        self.revers = []
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.rect = pygame.Rect(0, 0, load_image(sheet).get_width() // columns,
                                load_image(sheet).get_height() // rows)
        self.cut_sheet(load_image(sheet), columns, rows)
        self.cur_frame = random.randrange(0, len(self.frames))
        self.kuda = random.choice([-1, 1])
        if self.kuda == 1:
            self.image = self.frames[self.cur_frame]
        else:
            self.image = self.revers[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0
        self.time = 0
        self.pod = True
        self.cosn = False
        if sheet == "Zombie_Run.png":
            self.health = 1
        elif sheet == "Zombie2_Run_2.png":
            self.health = 3
        elif sheet == "Zombie3_Run_2.png":
            self.health = 5
        elif sheet == "Zombie4_Run_2.png":
            self.health = 7
        else:
            self.health = 125
        self.skl = Shkala(self.rect.center, self.health, (54, 9), True)

    def cut_sheet(self, sheet, columns, rows):
        for j in range(rows):
            for o in range(columns):
                frame_location = (self.rect.w * o, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.revers.append(pygame.transform.flip((sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))), True, False))

    def tuda_suda(self):
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(self.kuda, 2)
        else:
            self.rect = self.rect.move(self.kuda, -2)
        if self.frame == 0:
            self.time += 1
            self.time %= 11
            if self.time == 10:
                self.pod = False
            if self.time == 0 or self.time == 5:
                self.kuda = -self.kuda

    def change_kadr_d(self, pic):
        global money
        if gde[0] > self.rect[0]:
            pic = pic[:-4] + '_4' + pic[-4:]
        self.cut_sheet(load_image(pic), self.columns + 1, self.rows)
        if self.cur_frame == len(self.frames):
            self.kill()
            self.skl.kill()
        else:
            self.image = self.frames[self.cur_frame]
            if self.cur_frame == 0:
                money += self.skl.hp
                zdeat.play()
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames) + 1)

    def death(self):
        if self.frame % 10 == 0:
            self.frames = []
            if self.sheet == "Zombie_Run.png":
                self.change_kadr_d("Zombie_death.png")
            elif self.sheet == "Zombie2_Run_2.png":
                self.change_kadr_d("Zombie2_death.png")
            elif self.sheet == "Zombie3_Run_2.png":
                self.change_kadr_d("Zombie3_death.png")
            elif self.sheet == "Zombie4_Run_2.png":
                self.change_kadr_d("Zombie4_death.png")


    def update(self, x):
        self.skl.update(self.rect.center, self.health)
        self.frame += 1
        self.frame %= 60
        if self.health <= 0:
            self.death()
        else:
            for j in range(len(zapusheno)):
                if pygame.sprite.collide_mask(self, zapusheno[j]):
                    self.health -= 1
                    zapusheno.pop(j)
                    break
            # if pygame.sprite.collide_mask(self, player):
            #     zatta.play()
            if self.pod:
                if self.frame % 10 == 0:
                    if self.kuda == 1:
                        self.image = self.frames[self.cur_frame]
                    else:
                        self.image = self.revers[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.tuda_suda()
            else:
                if abs(self.rect.center[0] - x) < 500:
                    if self.frame % 10 == 0:
                        if self.rect.center[0] < x:
                            self.image = self.frames[self.cur_frame]
                        else:
                            self.image = self.revers[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)

                    self.pod = False
                    if x == self.rect.center[0]:
                        self.pod = True
                    else:
                        if x > self.rect.center[0]:
                            n = 2
                        else:
                            n = -2
                        if not pygame.sprite.collide_mask(self, mountain):
                            self.rect = self.rect.move(n, 2)
                        else:
                            self.rect = self.rect.move(n, -2)
                else:
                    self.pod = True


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pauic)
        self.image = load_image("pause.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, 100)


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, x, y, health):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.health = health
        self.skl = Shkala((0, 0), self.health, (216, 36), False)

    def update(self, x, y):
        self.skl.update_hero(self.health)
        self.frame += 1
        self.frame %= 60
        if self.frame == 0:
            for j in range(len(z_list)):
                if pygame.sprite.collide_mask(self, z_list[j]):
                    self.health -= 1
                    zatta.play()
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(x, y)
        else:
            self.rect = self.rect.move(0, -1)


if __name__ == '__main__':
    money = 0

    camera = Camera(0, 0, 0, 0)
    day = Day()
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    shkales = pygame.sprite.Group()
    dismov_shkales = pygame.sprite.Group()
    another = pygame.sprite.Group()
    pauic = pygame.sprite.Group()
    notallll = [all_sprites, zombies, another, shkales]
    allll = [all_sprites, zombies, another, shkales, dismov_shkales]
    mountain = Mountain()
    zapusheno = []

    running = True
    pause = False
    fps = 60
    clock = pygame.time.Clock()

    # МУЗЫКА!
    playList = ['Fraunhofer Diffraction - Burning Bridges.mp3',
                'Fraunhofer Diffraction - Take Me Back.mp3', 'Pryda - Shadows.mp3', 'deadmau5 - GG.mp3',
                'Forsch,Broosnica,Forsch, Broosnica - Odinochestvo V Seti.mp3']
    for i in playList:
        inland(i)
    random.shuffle(playList)
    mus_now = random.choice(playList)

    start_screen()

    vystrel = pygame.mixer.Sound("data/Gun.wav")
    vystrel.set_volume(0.8)
    zatta = pygame.mixer.Sound("data/Zombie Attack Sound.wav")
    zatta.set_volume(0.6)
    zdeat = pygame.mixer.Sound("data/Zombie Death.mp3")
    sounds = [vystrel, zatta, zdeat]

    mountain.upd(mus_now, - 1.5 * width, height // 4)

    mx, my = 0, 1
    nx, ny = 0, 0
    z_list = []
    Pause()
    for i in range(101):
        zomim = random.choice(["Zombie_Run.png", "Zombie2_Run_2.png", "Zombie3_Run_2.png", "Zombie4_Run_2.png"])
        z_list.append(Zombie(zomim, 7, 1, 10000 - i * 100, 200))
    player = Landing(400, 200, 50)

    while running:
        if not pause:
            screen.fill(day.color())
        gde = player.rect.center
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_p:
                    if not pause:
                        pygame.mixer.music.pause()
                        for i in sounds:
                            i.stop()
                        pause = True
                    else:
                        pygame.mixer.music.unpause()
                        pause = False
                if not pause:
                    if k == pygame.K_LEFT:
                        mx, my = -1, 0
                    elif k == pygame.K_RIGHT:
                        mx, my = 1, 0
                    elif k == pygame.K_DOWN:
                        mx, my = 0, 2
                    elif k == pygame.K_UP:
                        mx, my = 0, -1
                    if k == pygame.K_d:
                        if nx == 2 and ny == 0:
                            nx, ny = 0, 0
                        else:
                            nx, ny = -2, 0
                    elif k == pygame.K_a:
                        if nx == -2 and ny == 0:
                            nx, ny = 0, 0
                        else:
                            nx, ny = 2, 0
                    elif k == pygame.K_w:
                        if nx == 0 and ny == -2:
                            nx, ny = 0, 0
                        else:
                            nx, ny = 0, 2
                    elif k == pygame.K_s:
                        if nx == 0 and ny == 2:
                            nx, ny = 0, 0
                        else:
                            nx, ny = 0, -2
                    if k == pygame.K_e:
                        zapusheno.append(Pula(gde, True))
                    if k == pygame.K_q:
                        zapusheno.append(Pula(gde, False))
                else:
                    if k == pygame.K_s:
                        save()
                    if k == pygame.K_l and load_save():
                        pause = False
                        pygame.mixer.music.unpause()
            else:
                mx, my = 0, 1
        for group in allll:
            group.draw(screen)
        if not pause:
            all_sprites.update(mx, my)
            another.update()
            zombies.update(gde[0])
            # изменяем ракурс камеры
            camera.update(player, nx, ny)
            # обновляем положение всех спрайтов
            for group in notallll:
                for sprite in group:
                    camera.apply(sprite)
        else:
            pauic.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
