from pygame import *

window = display.set_mode((700, 500))
display.set_caption("Догонялки")


#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
 
#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
 
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y,):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))     #шаг 1
        self.image.fill((color_1, color_2, color_3))        #шаг 2
        self.rect = self.image.get_rect()                   #шаг 3
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



#сама игра

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("background.jpg"), (win_width, win_height))


#Персонажи игры:
player = Player('sprite1.jpeg', 210, win_height - 179, 4)
monster = Enemy('sprite2.jpg', win_width - 72, 349, 2)
final = GameSprite('sprite1.png',600, 246, 0)

#Таймер
clock = time.Clock()
FPS = 60
#rgb(249, 194, 91)
w1 = Wall(249, 194, 91, 10, 100, 370, 200)
w2 = Wall(249, 194, 91, 10, 80, 504, 380)
w3 = Wall(249, 194, 91, 100, 10, 407,380)
w4 = Wall(249, 194, 91, 300, 10, 504,450)
w5 = Wall(249, 194, 91, 100, 10, 370,200)
w6 = Wall(249, 194, 91, 10, 100, 470,200)
w7 = Wall(249, 194, 91, 100, 10, 470,300)
w8 = Wall(249, 194, 91, 380, 10, 0,300)

#музыка
mixer.init()
mixer.music.load('burger_king_gvno_spider_dance_mashup-mob4ik.com.mp3')
mixer.music.play()

money = mixer.Sound('chashku-stavjat-na-bljudechko1.mp3')
kick = mixer.Sound('aaaa.mp3')

#текст
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

#Игровой цикл
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        player.update()
        monster.update()
           
        window.blit(background,(0, 0))
        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()

        #Ситуация "Проигрыш"
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2)or sprite.collide_rect(player, w3):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
 
        #Ситуация "Выигрыш"
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()


    display.update()
    clock.tick(FPS)

