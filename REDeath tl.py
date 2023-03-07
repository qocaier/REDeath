import random
from os import listdir
from os.path import isfile, join
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


def prompt_file(descr, ras):
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=[(descr, ras)])
    top.destroy()
    return file_name


def load_image(name):
    fullname = os.path.join('data', name)  # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def inland(name):
    if os.path.exists(f"data/levels/{name[:-3]}png"):
        pass

    else:
        mpl.use('TkAgg')

        spf = wave.open(f"data/music/wav/{name[:-3]}wav", "r")

        # Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        fs = spf.getnframes()
        rate = spf.getframerate()
        dur = fs / float(rate)

        if spf.getnchannels() == 2:  # If Stereo
            print("Just mono files")
            sys.exit(0)

        Time = np.linspace(0, len(signal) / rate, num=len(signal))

        mpl.rcParams['agg.path.chunksize'] = 10000

        plt.figure(1, figsize=(round(dur / 10), 1))
        plt.axis('off')
        plt.plot(Time, signal, color='#3A430A')
        plt.savefig(f"data/levels/{name[:-3]}png", dpi=1000, edgecolor='black', bbox_inches='tight',
                    transparent=True)
        plt.close(1)


def terminate():
    pygame.quit()
    sys.exit()


class Start:
    def __init__(self):
        fon = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        smallfont = pygame.font.SysFont('Segoe UI Semibold', 28)
        self.rand = smallfont.render('Случайная игра', True, '#000000')
        self.loadlv = smallfont.render('Загрузить уровень', True, '#000000')
        self.loadsv = smallfont.render('Загрузить сохранение', True, '#000000')
        pygame.mixer.music.load('data/music/TremLoadingloopl.wav')
        pygame.mixer.music.play(-1)

    def update(self):
        global mus_now, star
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            mouse = pygame.mouse.get_pos()
            if width / 2 <= mouse[0] <= width / 2 + 230 and height / 3 <= mouse[1] <= height / 3 + 40:
                pygame.draw.rect(screen, '#D72D2E', [width / 2, height / 3, 230, 40])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mus_now = random.choice(playList)
                    pygame.mixer.music.load('data/music/mp3/' + random.choice(playList))
                    pygame.mixer.music.play()
                    tasovka()
                    star = False
            else:
                pygame.draw.rect(screen, '#357B45', [width / 2, height / 3, 230, 40])
            if width / 2 + 160 <= mouse[0] <= width / 2 + 430 and height / 3 + 60 <= mouse[1] <= height / 3 + 100:
                pygame.draw.rect(screen, '#D72D2E', [width / 2 + 160, height / 3 + 60, 270, 40])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mel = (prompt_file("Land level files", "*.png")[:-3] + 'mp3').split('/')
                    mel = mel[len(mel) - 1]
                    if mel != "mp3":
                        mus_now = mel
                        pygame.mixer.music.load('data/music/mp3/' + mel)
                        pygame.mixer.music.play()
                        tasovka()
                        star = False
            else:
                pygame.draw.rect(screen, '#357B45', [width / 2 + 160, height / 3 + 60, 270, 40])
            if width / 2 + 80 <= mouse[0] <= width / 2 + 350 and height / 3 + 120 <= mouse[1] <= height / 3 + 160:
                pygame.draw.rect(screen, '#D72D2E', [width / 2 + 80, height / 3 + 120, 320, 40])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if load_save():
                        star = False
            else:
                pygame.draw.rect(screen, '#357B45', [width / 2 + 80, height / 3 + 120, 320, 40])
            screen.blit(self.rand, (width / 2 + 10, height / 3))
            screen.blit(self.loadlv, (width / 2 + 170, height / 3 + 60))
            screen.blit(self.loadsv, (width / 2 + 90, height / 3 + 120))

        pygame.display.flip()
        clock.tick(fps)


def loading_screen():
    screen.fill('#357B45')
    text = pygame.font.SysFont('Segoe UI Semibold', 28).render('Генерация ландшафта', True, '#ffffff')
    descr = pygame.font.SysFont('Segoe UI Semibold',
                                10).render("""Если видите надпись "Не отвечает", то это """
                                           """неправда, и на самом деле все в полном порядке""", True, '#ffffff')
    scuch = random.choice(['Завариваем чай', 'Гладим котика', 'Садим деревья', 'Ищем сбежавших зомби',
                           'Распаковываем солнце', 'Подбрасываем монетку', 'Вам не надоело читать эти надписи?',
                           'Готовим все самое нужное', 'Разравниваем холмы',
                           'Вы устали ждать, а мы генерировать идеи для этих надписей', 'Растим траву',
                           'Делаем все, как надо', 'Выжимаем сок из ваших треков'])
    fint = pygame.font.SysFont('Segoe UI', 28).render(scuch, True, '#ffffff')
    screen.blit(fint, (width // 2 - 150, height // 2 + 30))
    screen.blit(text, (width // 2 - 150, height // 2))
    screen.blit(descr, (10, 10))
    pygame.display.flip()
    clock.tick(fps)
    return


def death_screen():
    screen.fill('#D72D2E')
    fon = pygame.transform.scale(load_image('leg.png'), (148, 40))
    screen.blit(fon, (width // 2 - 74, height // 2 - 200))
    text = pygame.font.SysFont('Segoe UI Semibold', 28).render('Вы умерли', True, '#ffffff')
    screen.blit(text, (width // 2 - 74, height // 2))
    fint = pygame.font.SysFont('Segoe UI', 28).render('Нам очень жаль осознавать это, но вам не удалось выжить',
                                                      True, '#ffffff')
    screen.blit(fint, (width // 2 - 350, height // 2 + 30))
    pygame.display.flip()
    clock.tick(fps)
    return


def result_screen():
    screen.fill('#ffffff')
    text = pygame.font.SysFont('Segoe UI Semibold', 28).render('Вы выжили', True, '#000000')
    screen.blit(text, (width // 2 - 100, height // 2 - 350))
    fint = pygame.font.SysFont('Segoe UI', 28).render('Поздравляем с победой, вы продержались до самого конца',
                                                      True, '#000000')
    screen.blit(fint, (width // 2 - 350, height // 2 - 320))
    pygame.display.flip()
    clock.tick(fps)
    return


def save():
    with open(f"data/saves/{dt.datetime.now().strftime('%d_%m_%Y %H_%M_%S')} save.txt", 'w') as f:
        f.write(';'.join([str(player.rect.x), str(player.rect.y), str(player.health), str(time_skl.patr)]) + '\n')
        f.write(';'.join([str(camera.dx), str(camera.dy), str(camera.smx), str(camera.smy)]) + '\n')
        f.write(';'.join([str(pygame.mixer.music.get_pos() + time_skl.izn), mus_now,
                          str(mountain.rect.x), str(mountain.rect.y)]) + '\n')
        f.write(';'.join([str(day.r), str(day.g), str(day.b), str(day.frame), str(day.time), str(day.kra),
                          str(day.sin), str(day.zel)]) + '\n')
        for j in z_list:
            f.write(';'.join([j.sheet, str(j.rect.x), str(j.rect.y), str(j.health)]) + '\n')
        f.close()


def load_save():
    global player, z_list, zapusheno, camera, mountain, mus_now, time_skl
    fn = prompt_file("Text save files", "*.txt")
    if fn != '':
        with open(fn, 'r') as f:
            li = f.readlines()
            pldt = li[0].split(';')
            try:
                player.kill()
                player.skl.kill()
            except Exception:
                pass
            player = Landing('run_hunt.png', 9, 1, int(pldt[0]), int(pldt[1]), 50)
            player.health = int(pldt[2])
            time_skl.patr = int(pldt[3])

            pldt = li[1].split(';')
            camera = Camera(int(pldt[0]), int(pldt[1]), int(pldt[2]), int(pldt[3]))

            pldt = li[2].split(';')
            mountain.upd(pldt[1], int(pldt[2]), int(pldt[3]))
            mus_now = pldt[1]
            pygame.mixer.music.load('data/music/mp3/' + pldt[1])
            pygame.mixer.music.play(start=(int(pldt[0]) / 1000))
            time_skl.__init__((width - 216, 0), pygame.mixer.Sound(f"data/music/wav/{mus_now[:-3]}wav").get_length(),
                              (216, 36), False)
            time_skl.hp = pygame.mixer.Sound(f"data/music/wav/{mus_now[:-3]}wav").get_length()
            time_skl.izn = int(pldt[0])
            time_skl.update_time()

            pldt = li[3].split(';')
            day.r, day.g, day.b, day.frame, day.time, day.kra, day.sin, day.zel = \
                int(pldt[0]), int(pldt[1]), int(pldt[2]), int(pldt[3]), int(pldt[4]), \
                int(pldt[5]), int(pldt[6]), int(pldt[7])

            try:
                for o in z_list:
                    o.kill()
                    o.skl.kill()
            except Exception:
                pass
            z_list = []
            for j in range(4, len(li) - 1):
                pldt = li[j].split(';')
                z_list.append(Zombie(pldt[0], 7, 1, int(pldt[1]), int(pldt[2])))
                z_list[j - 4].health = int(pldt[3])
            f.close()

            player.after_jump = True
            player.jump = True

            for group in notallll:
                for sprite in group:
                    camera.apply(sprite)

            return True
    else:
        return False


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
    def __init__(self, dx, dy, smx, smy):  # зададим начальный сдвиг камеры
        self.dx = dx
        self.dy = dy
        self.smx = smx
        self.smy = smy

    def apply(self, obj):  # сдвинуть объект obj на смещение камеры
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, x, y):  # позиционировать камеру на объекте target
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
        self.image = load_image("base.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # вычисляем маску для эффективного сравнения

    def upd(self, name, x, y):
        super().__init__(another)
        self.image = load_image(f"levels/{name[:-3]}png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        pygame.mixer.music.load(f"data/music/mp3/{name}")
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
        if player.image == Landing.image or player.image == Landing.reverse_image:
            self.rect = self.rect.move(pos[0], pos[1] - 7)
        else:
            self.rect = self.rect.move(pos[0], pos[1] - 27)
        self.mask = pygame.mask.from_surface(self.image)
        self.cosn = False
        vystrel.play()
        time_skl.patr += 1

    def update(self):
        for j in range(len(z_list)):
            if pygame.sprite.collide_mask(self, z_list[j]):
                self.cosn = True
            if z_list[j].health == 0:
                z_list.pop(j)
                zdeat.play()
                break
        if not (pygame.sprite.collide_mask(self, mountain) or self.cosn or self.rect.centerx > width or
                self.rect.centerx < 0):
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
        self.izn, self.patr = 0, 0

    def update(self, pos, health):
        self.image.fill('dark red')
        pygame.draw.rect(self.image, [255, 0, 0], [2, 2, round(health / self.hp * 50), 5], 0)
        self.rect.center = [pos[0], pos[1] - 50]

    def update_hero(self, health):
        self.image.fill('dark red')
        pygame.draw.rect(self.image, [255, 0, 0], [8, 8, round(health / self.hp * 200), 20], 0)
        descr = pygame.font.SysFont('Segoe UI Semibold',
                                    15).render(f"{health} / {self.hp} hp", True, '#ffffff')
        screen.blit(descr, (80, 5))

    def update_time(self):
        self.image.fill('dark grey')
        pygame.draw.rect(self.image, [255, 255, 255], [8, 8, round((self.izn + pygame.mixer.music.get_pos()) / 1000 /
                                                                   self.hp * 200), 20], 0)
        descr = pygame.font.SysFont('Segoe UI Semibold',
                                    15).render(f"{(self.izn + pygame.mixer.music.get_pos()) // 1000 // 60}"
                                               f":{(self.izn + pygame.mixer.music.get_pos()) // 1000 % 60}"
                                               f" / {round(self.hp) // 60}:{round(self.hp) % 60}", True, '#000000')
        screen.blit(descr, (width - 130, 5))
        descr = pygame.font.SysFont('Segoe UI Semibold',
                                    15).render(f"{500 - len(z_list)} killed, {self.patr} shoots, "
                                               f"{mus_now[:-4]}", True, '#000000')
        screen.blit(descr, (250, 5))


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
        if gde[0] > self.rect[0]:
            pic = pic[:-4] + '_4' + pic[-4:]
        self.cut_sheet(load_image(pic), self.columns + 1, self.rows)
        if self.cur_frame == len(self.frames):
            self.kill()
            self.skl.kill()
        else:
            self.image = self.frames[self.cur_frame]
            if self.cur_frame == 0:
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
            if self.kuda == 1 and self.rect.x >= mountain.image.get_width() - width:
                self.kuda = -1
            elif self.kuda == -1 and self.rect.x <= 0.5 * width:
                self.kuda = 1
            for j in range(len(zapusheno)):
                if pygame.sprite.collide_mask(self, zapusheno[j]):
                    self.health -= 1
                    zapusheno.pop(j)
                    break
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
                elif self.rect.center[0] >= mountain.image.get_width() - width:
                    if not pygame.sprite.collide_mask(self, mountain):
                        self.rect = self.rect.move(-2, 2)
                    else:
                        self.rect = self.rect.move(-2, -2)
                elif self.rect.center[0] <= 0.5 * width:
                    if not pygame.sprite.collide_mask(self, mountain):
                        self.rect = self.rect.move(2, 2)
                    else:
                        self.rect = self.rect.move(2, -2)
                else:
                    self.pod = True


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pauic)
        self.image = load_image("pause.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, 100)


class Landing(pygame.sprite.Sprite):
    image = load_image('sid.png')
    reverse_image = pygame.transform.flip(image, True, False)

    def __init__(self, sheet, columns, rows, x, y, health):
        super().__init__(all_sprites)
        self.frames = []
        self.revers = []
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.rect = pygame.Rect(0, 0, load_image(sheet).get_width() // columns, load_image(sheet).get_height() // rows)
        self.cut_sheet(load_image(sheet), columns, rows)
        self.cur_frame = random.randrange(0, len(self.frames))
        self.kuda = 1

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.health = health
        self.skl = Shkala((0, 0), self.health, (216, 36), False)
        self.jump = False
        self.after_jump = False
        self.before_jump = False
        self.sit = False
        self.now_frame = self.frame
        self.nd = False

    def cut_sheet(self, sheet, columns, rows):
        for j in range(rows):
            for o in range(columns):
                frame_location = (self.rect.w * o, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                self.revers.append(pygame.transform.flip((sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))), True, False))

    def update(self, x, y):
        global dea
        self.skl.update_hero(self.health)
        self.frame += 1
        self.frame %= 60
        if self.health <= 0:
            time_skl.kill()
            death_screen()
            dea = True
            pygame.mixer.music.stop()
        if self.frame % 4 == 0 and x != 0:
            if self.kuda == 1:
                self.image = self.frames[self.cur_frame]
            else:
                self.image = self.revers[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.frame == 0:
            for j in range(len(z_list)):
                if pygame.sprite.collide_mask(self, z_list[j]):
                    self.health -= 1
                    zatta.play()
        if not pygame.sprite.collide_mask(self, mountain):  # если ещё в небе
            self.rect = self.rect.move(x, y)
        else:
            self.rect = self.rect.move(x, -1)
        if self.jump:
            if self.before_jump:
                if self.frame != (self.now_frame + 20) % 60:
                    if player.kuda == 1:
                        self.image = Landing.image
                    else:
                        self.image = Landing.reverse_image
                else:
                    if self.nd:
                        if self.kuda == 1:
                            self.image = self.frames[5]
                        else:
                            self.image = self.revers[5]
                        self.nd = False
                        self.jump = False
                    self.before_jump = False
            elif self.after_jump:
                if self.kuda == 1:
                    self.image = self.frames[0]
                else:
                    self.image = self.revers[0]
                self.rect = self.rect.move(x, 10)
                if pygame.sprite.collide_mask(self, mountain):
                    self.after_jump = False
                    self.now_frame = self.frame
                    self.before_jump = True
                    self.nd = True
            elif self.frame != (self.now_frame + 50) % 60:
                if self.kuda == 1:
                    self.image = self.frames[0]
                else:
                    self.image = self.revers[0]
                self.rect = self.rect.move(x, -10)
            else:
                self.after_jump = True
        elif self.sit:
            if player.kuda == 1:
                self.image = Landing.image
            else:
                self.image = Landing.reverse_image


def tasovka():
    global zapusheno, pause, player, camera, z_list, time_skl
    for j in zapusheno:
        j.kill()
    zapusheno = []

    time_skl = Shkala((width - 216, 0), pygame.mixer.Sound(f"data/music/wav/{mus_now[:-3]}wav").get_length(),
                      (216, 36), False)
    time_skl.hp = pygame.mixer.Sound(f"data/music/wav/{mus_now[:-3]}wav").get_length()
    time_skl.izn, time_skl.patr = 0, 0

    player.after_jump = True
    player.jump = True

    try:
        mountain.kill()
        player.kill()
        player.skl.kill()
    except Exception:
        pass
    player = Landing('run_hunt.png', 9, 1, 400, 200, 50)

    camera = Camera(0, 0, 0, 0)

    mountain.upd(mus_now, - 1.5 * width, height // 4)

    day.__init__()

    try:
        for o in z_list:
            o.kill()
            o.skl.kill()
    except Exception:
        pass
    z_list = []
    for j in range(500):
        zomim = random.choice(["Zombie_Run.png", "Zombie2_Run_2.png", "Zombie3_Run_2.png", "Zombie4_Run_2.png"])
        z_list.append(Zombie(zomim, 7, 1, random.randint(0.5 * width, mountain.image.get_width() - width), height // 2))

    for group in notallll:
        for sprite in group:
            camera.apply(sprite)


if __name__ == '__main__':
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
    playList = [f for f in listdir('data/music/mp3') if isfile(join('data/music/mp3', f))]
    for i in playList:
        loading_screen()
        inland(i)
    random.shuffle(playList)
    mus_now = random.choice(playList)

    vystrel = pygame.mixer.Sound("data/music/Gun.wav")
    vystrel.set_volume(0.8)
    zatta = pygame.mixer.Sound("data/music/Zombie Attack Sound.wav")
    zatta.set_volume(0.6)
    zdeat = pygame.mixer.Sound("data/music/Zombie Death.mp3")
    sounds = [vystrel, zatta, zdeat]

    mountain.upd(mus_now, - 1.5 * width, height // 4)

    mx, my = 0, 1
    nx, ny = 0, 0
    z_list = []
    Pause()
    for i in range(500):
        zomim = random.choice(["Zombie_Run.png", "Zombie2_Run_2.png", "Zombie3_Run_2.png", "Zombie4_Run_2.png"])
        z_list.append(Zombie(zomim, 7, 1, random.randint(0.5 * width, mountain.image.get_width() - width), height // 2))
    player = Landing('run_hunt.png', 9, 1, 400, 200, 50)
    time_skl = Shkala((width - 216, 0), pygame.mixer.Sound(f"data/music/wav/{mus_now[:-3]}wav").get_length(),
                      (216, 36), False)

    player.after_jump = True
    player.jump = True
    start = Start()
    star = True
    dea = False
    fi = True
    while running:
        if star:
            if fi:
                start.__init__()
                fi = False
            start.update()
        elif dea:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    star = True
                    dea = False
                    fi = True
        else:
            fi = True
            if not pause:
                screen.fill(day.color())
                if not pygame.mixer.music.get_busy():
                    player.skl.kill()
                    time_skl.kill()
                    result_screen()
                    dea = True
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
                        player.sit = False
                        if not player.jump:
                            my = 1
                            if k == pygame.K_UP:
                                if pygame.sprite.collide_mask(player, mountain):
                                    player.before_jump = True
                                    player.jump = True
                                    player.now_frame = player.frame
                        if k == pygame.K_LEFT:
                            mx = -1
                            player.kuda = -1
                        elif k == pygame.K_RIGHT:
                            mx = 1
                            player.kuda = 1
                        elif k == pygame.K_DOWN:
                            player.sit = True
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
                        if k == pygame.K_SPACE:
                            if player.kuda == 1:
                                zapusheno.append(Pula(gde, True))
                            else:
                                zapusheno.append(Pula(gde, False))
                    else:
                        if k == pygame.K_s:
                            save()
                        if k == pygame.K_l and load_save():
                            pause = False
                            pygame.mixer.music.unpause()
                        if k == pygame.K_e:
                            star = True
                        if k == pygame.K_m:
                            star = True
                            pause = False
                else:
                    if player.jump:
                        mx, my = 0, 5
                    else:
                        mx, my = 0, 1
            for group in allll:
                group.draw(screen)
            if not pause:
                all_sprites.update(mx, my)
                another.update()
                zombies.update(gde[0])
                if not dea:
                    time_skl.update_time()
                camera.update(player, nx, ny)  # изменяем ракурс камеры
                for group in notallll:  # обновляем положение всех спрайтов
                    for sprite in group:
                        camera.apply(sprite)
            else:
                pauic.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
    pygame.quit()
