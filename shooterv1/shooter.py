import pygame
pygame.init()
from random import *
W= 700
H =550
fon = pygame.transform.scale(pygame.image.load('galaxy.jpg'),(W,H))
scr = pygame.display.set_mode((W,H))
pygame.display.set_caption('Shooter')
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire = pygame.mixer.Sound('fire.ogg')
fps = pygame.time.Clock()
asteroid_count =0
class Asteroid():
    def __init__(self,x,y,w,h,img):

        self.x = x
        self.y = y
        self.w =w
        self.h = h
        self.img =img
        self.image= pygame.transform.scale(pygame.image.load(self.img), (self.w, self.h))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = randint(1, 3)  # - змінюємо швидкість ворогів
    def update(self):
        self.rect.y +=self.speed

        if self.rect.bottom>= 550:
            self.rect.y = -10
            self.rect.x = randint(30, 650)
            global asteroid_count
            asteroid_count+=1
asteroids = []
for el in range(5):
    asteroid = Asteroid(randint(30,650),-10,50,50,'asteroid.png')
    asteroids.append(asteroid)


print(asteroids)
class Player():
    def __init__(self,x,y,w,h,img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.img_new = pygame.transform.scale(pygame.image.load(self.img),(self.w,self.h))
        self.rect = self.img_new.get_rect(center = (self.x,self.y))
        self.speed = randint(1,3)# - змінюємо швидкість ворогів
    def control(self,W):# керування

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left >=0:
            self.rect.x -= move
        if key[pygame.K_RIGHT] and self.rect.right <= W:
            self.rect.x += move


class Bullet():
    def __init__(self,x,y,w,h,img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.img_new = pygame.transform.scale(pygame.image.load(self.img), (self.w, self.h))
        self.rect = self.img_new.get_rect(center=(self.x, self.y))
player = Player(W//2,H - 50,70,100,'rocket.png')

bul_chek = False
bul_list = []
enemy_list = []
def add_enemy():# створюємо 5 ворогів і додаємо до списку enemy
    for el in range(5):
        x = randint(50,650)#  вказуємо випадкове положення звідки почнеться рух
        y = randint(-100,150)
        enemy = Player(x,y,50,50,'ufo.png')
        enemy_list.append(enemy)

add_enemy()# викликаємо функцію яка додає ворогів

run = True
s = 0# кількість вбитих воргів тобто рахунок score
l = 0# відповідає за кількість пропущених ворогів
def loose(enemy,bullets,scr):# функція поразки
    global chek_text
    text = pygame.font.Font(None,55).render('Ви програли',True,(155,95,55))
    global move
    global health
    for el in enemy:
        if el.rect.colliderect(player.rect) or l>=15 or health ==0:# кількість пропущених ворогів
            asteroids.clear()# очищуємо списки з астероїдами
            enemy.clear()# очищуємо списки ворогами
            bullets.clear()# з кулями
            move = 0
            chek_text =True# потрібен для того якщо настане умова програшу зробити так щоб текст програшу відмалювався
    if chek_text:
        scr.blit(text,(W//2 -95,H//2))

def win(enemy,bullets,scr):# тут прописуєм умову перемоги
    global chek_text_win
    text = pygame.font.Font(None,55).render('Ви перемогли',True,(155,95,55))
    global move
    global s

    if s>=15:# прописуємо скільки ворогів треба вбити щоб перемогти
        enemy.clear()# очищає список для того щоб на екрані вже нічого не відмальовувалось
        bullets.clear()
        move = 0# робимо рух по координаті x = 0  для того щоб не могти рухати ракетою
        chek_text_win =True
    if chek_text_win:
        scr.blit(text,(W//2 -95,H//2))# відмальовуємо текст перемоги
chek_text = False
move = 4
chek_text_win = False
health = 3
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:# клавіша пробіл
                fire.play()# відтворюмо звук
                bul_list.append(Bullet(player.rect.x, player.rect.y, 16, 31, 'bullet.png'))# коли натискається клавіша пробіл до нашого списку куль додається нова куля
    scr.blit(fon,(0,0))# задаємо задній фон
    scr.blit(player.img_new, player.rect)# відмальовуємо нашу ракету
    player.control(W)# метод класу який відповідає за керування ракетою
    for el in enemy_list:# відмальовуємо всіх ворогів 5 шт
        scr.blit(el.img_new,(el.rect.x,el.rect.y))
        el.rect.y+=el.speed# застосовуємо випадкуву швидкість до кординати y
        if el.rect.bottom>=H:# умова що буде якщо ворог торкнувся нижньої межі ми задаємо йому знову координати зверху
            el.rect.x = randint(50, 650)
            el.rect.y = randint(50, 150)
            l+=1# змінємо рахунок пропущених ворогів
        for ell in bul_list:# перебираємо список зі всіма кулями

            scr.blit(ell.img_new, (ell.rect.x+player.w//2 ,ell.rect.y))# відмальовуємо
            ell.rect.y -=1# рух кулі вверх

            if ell.rect.colliderect(el.rect):# описуємо що буде якщо наша куля зіштовхнеться з противником el - це противник ell це куля
                el.rect.x = randint(50, 650)# перемііщуємо противника на задані координати
                el.rect.y = randint(50, 150)
                s+=1# змінюємо рахунок score
                bul_list.remove(ell)# видалємо кулю зі списку таким чином вона зникає і не відмальовується
    #scr.blit(bul.img_new,(player.rect.x +player.w//2 -bul.w//2,player.rect.y))
    text = "Score: " +str(s)# - змінна для відображення рахунку
    text_score = pygame.font.SysFont('Arial',30).render(text,True,(77,11,155))
    text1 = "Loose: " +str(l)
    text_loose = pygame.font.SysFont('Arial', 30).render(text1, True, (77, 11, 155))
    text3 = "health:" +str(health)# змінна для життя

    text3_health = pygame.font.SysFont('Arial',30).render(text3,True,(77,11,155))
    scr.blit(text3_health, (300, 10))# відмальовуємо текст життя
    scr.blit(text_score,(10,30))# текст перемоги
    scr.blit(text_loose, (10, 65))# текст поразки
    if asteroid_count<=4:
        print(asteroid_count)
        for el in asteroids:# перебираємо список з нашими астероїдами і відмальовуємо їх el - це один астероїд
            scr.blit(el.image,(el.rect.x,el.rect.y))
            el.update()# функція коли астероїд торкається низу зявляться знову зверху
            if el.rect.colliderect(player.rect):
                el.rect.y = -10
                el.rect.x = randint(30, 650)
                health -=1



    fps.tick(45)
    loose(enemy_list,bul_list,scr)# виклик функції поразки
    win(enemy_list,bul_list,scr)# виклик функції перемоги сюди аргументами предеємо список ворогів список куль і екран на якому відмальовуємо це все
    pygame.display.update()
