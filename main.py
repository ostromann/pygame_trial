from cmath import isnan
import pygame
import os
import numpy as np
import math

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2-BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('impact', 40)
WINNER_FONT = pygame.font.SysFont('impact', 100)

FPS = 60
VEL = 5
# ACC = 2  # px/frame^2
# MAX_VEL = 10  # px/frame
BULLET_VEL = 10
MAX_BULLETS = 7
MAX_HEALTH = 3


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

# SPACE = pygame.transform.scale(pygame.image.load(
#     os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# load background image
SPACE = pygame.image.load(os.path.join(
    'Assets', 'space_endless.png')).convert()

STARS = pygame.image.load(os.path.join(
    'Assets', 'stars_endless.png')).convert_alpha()

SHIELD_WIDTH, SHIELD_HEIGHT = 10, 10

YELLOW_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_yellow.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))
RED_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_red.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))

EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 70, 70
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'explosion.png')), (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))

EXPLOSION_TIMEOUT = 5

ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'asteroid.png')), (ASTEROID_WIDTH, ASTEROID_HEIGHT))


class Ammo(pygame.Rect):
    def __init__(self, x=WIDTH, y=0, width=30, height=30)):
        print(y)
        self.x=x
        self.y=y
        self.width=width
        self.height=height

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self)


class Asteroid(pygame.Rect):
    def __init__(self, x = WIDTH, y = 0, width = 70, height = 70, vel = np.array([0.0, 0.0])):
        print(y)
        self.x=x
        self.y=np.random.uniform(20, HEIGHT-20)
        self.width=width
        self.height=height
        self.vel=np.array([-5.0, np.random.uniform(-2.0, 2.0)])
        self.drop_rate=0.5

    def handle_movement(self, asteroids):
        self.x += self.vel[0]
        self.y += self.vel[1]

        if self.x < 0:
            asteroids.remove(self)

    def draw(self, win):
        win.blit(ASTEROID, (self.x, self.y))


class Explosion(pygame.Rect):
    def __init__(self, x, y, width, height, duration):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.duration=duration

        BULLET_HIT_SOUND.play()

    def draw(self, win):
        if self.duration > 0:
            win.blit(EXPLOSION, (self.x, self.y))
            self.duration -= 1
            print(f'explosion rendered, duration: {self.duration}')
            return True
        else:
            return False


class Bullet(pygame.Rect):
    def __init__(self, x, y, width, height, color, owner):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.owner=owner  # owner is immune to damage from this Bullet

        BULLET_FIRE_SOUND.play()

    def handle_movement(self, spaceships, bullets, asteroids, explosions):
        if self.color == YELLOW:
            self.x += BULLET_VEL
        elif self.color == RED:
            self.x -= BULLET_VEL
        else:
            raise ValueError

        for collision in self.collidelistall(spaceships):
            if spaceships[collision] != self.owner:
                self.owner.bullets.remove(self)
                bullets.remove(self)
                pygame.event.post(pygame.event.Event(
                    spaceships[collision].hit_event))

        for collision in self.collidelistall(asteroids):
            if asteroids[collision] != self.owner:
                print(self.owner.bullets)
                explosion=Explosion(asteroids[collision].x + asteroids[collision].width//2 - EXPLOSION_WIDTH//2, asteroids[collision].y + asteroids[collision].height //
                                      2 - EXPLOSION_HEIGHT//2, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, EXPLOSION_TIMEOUT)
                asteroids.remove(asteroids[collision])
                explosions.append(explosion)

                self.owner.bullets.remove(self)
                bullets.remove(self)
                break

        if self.is_out_of_bounds():
            self.owner.bullets.remove(self)
            bullets.remove(self)

    def is_out_of_bounds(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            return True
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self)


class Spaceship(pygame.Rect):
    def __init__(self, x, y, width, height, color, key_up, key_down, key_left, key_right, key_shoot, hit_event):
        # self.rect = pygame.Rect(x, y, width, height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.vel=np.array([0.0, 0.0])
        self.max_vel=20  # px/frame
        self.acc=0.8  # px/frame^2
        self.friction=0.9  # px/frame^2
        self.max_health=5
        self.health=self.max_health
        self.max_bullets=3
        self.bullets=[]
        self.bullet_vel=10
        self.key_up=key_up
        self.key_down=key_down
        self.key_right=key_right
        self.key_left=key_left
        self.key_shoot=key_shoot
        self.hit_event=hit_event

    def handle_acceleration(self, keys_pressed):
        acc_direction=np.array([0.0, 0.0])

        if keys_pressed[self.key_left]:  # LEFT
            print('LEFT')
            acc_direction[0] -= 1.0
        if keys_pressed[self.key_right]:  # RIGHT
            print('RIGHT')
            acc_direction[0] += 1.0
        if keys_pressed[self.key_up]:  # UP
            print('UP')
            acc_direction[1] -= 1.0
        if keys_pressed[self.key_down]:  # DOWN
            print('DOWN')
            acc_direction[1] += 1.0

        # if no key pressed, apply friction
        if acc_direction[0] == 0.0 and acc_direction[1] == 0.0:
            self.vel=np.array([0.0, 0.0]) if np.linalg.norm(
                self.vel) < 0.01 else self.vel * self.friction

        # apply acceleration
        else:
            # normalize acceleration to unit vector
            acc_direction = acc_direction / np.linalg.norm(acc_direction)
            acc_direction = np.where(np.isnan(acc_direction), 0, acc_direction)

            self.vel += acc_direction * self.acc

        # limit velocity
        if np.linalg.norm(self.vel) > self.max_vel:
            print('reached max vel')
            v_hat = self.vel / np.linalg.norm(self.vel)
            print('unit vector', v_hat)
            self.vel = v_hat * self.max_vel
            print('limited', self.vel)

    def handle_movement(self, keys_pressed):
        self.handle_acceleration(keys_pressed)

        self.x += self.vel[0]
        self.y += self.vel[1]

        # check boundary collision
        if self.x < 0:
            self.x = 0
            self.vel[0] = 0.0
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
            self.vel[0] = 0.0
        if self.y < 0:
            self.y = 0
            self.vel[1] = 0.0
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height
            self.vel[1] = 0.0

    def handle_collisions(self, asteroids, items):
        for asteroid in asteroids:
            print('checking collisions with', asteroid)
            if self.colliderect(asteroid):
                items.append(Ammo(self.x, self.y))
                asteroids.remove(asteroid)
                pygame.event.post(pygame.event.Event(YELLOW_HIT))

    def draw(self, win):
        # Render spaceship
        if self.color == YELLOW:
            win.blit(YELLOW_SPACESHIP, (self.x, self.y))
        elif self.color == RED:
            win.blit(RED_SPACESHIP, (self.x, self.y))
        else:
            raise ValueError

        # Render available bullets
        for pos, slot in enumerate(range(self.max_bullets - len(self.bullets))):
            slot_width = self.width//self.max_bullets-2
            slot_height = 10
            pygame.draw.rect(WIN, self.color, pygame.Rect(
                self.x + (slot_width + 2)*pos, self.y-slot_height, slot_width, slot_height))

        # Render shields
        for pos, slot in enumerate(range(self.health)):
            if self.color == YELLOW:
                win.blit(YELLOW_SHIELD, (self.x + 10*pos,
                                         self.y + self.height))
            elif self.color == RED:
                win.blit(RED_SHIELD, (self.x + 10*pos,
                                      self.y + self.height))


class Background():
    def __init__(self, image,  scroll_speed):
        self.image = image
        self.tiles = math.ceil(WIDTH / self.image.get_width()) + 1
        self.scroll_speed = scroll_speed
        self.scroll = 0

    def draw(self, win):
        # draw scrolling background
        for i in range(0, self.tiles):
            WIN.blit(self.image, (i * self.image.get_width() + self.scroll, 0))
            # Debugging
            # bg_rect.x = i * self.image.width + self.scroll
            # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

        # scroll background
        self.scroll += self.scroll_speed

        # reset scroll
        if abs(self.scroll) > self.image.get_width():
            self.scroll = 0


def draw_window(backgrounds, spaceships,  bullets, explosions, asteroids, items):

    for background in backgrounds:
        background.draw(WIN)

    for spaceship in spaceships:
        spaceship.draw(WIN)

    for bullet in bullets:
        bullet.draw(WIN)

    for explosion in explosions:
        if not explosion.draw(WIN):
            print('explosion removed')
            explosions.remove(explosion)

    for asteroid in asteroids:
        asteroid.draw(WIN)

    for item in items:
        item.draw(WIN)

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    space_background = Background(SPACE, -1)
    stars_background = Background(STARS, -2)
    yellow = Spaceship(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, YELLOW,
                       pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE, YELLOW_HIT)

    backgrounds = [space_background, stars_background]
    spaceships = [yellow]
    bullets = []
    explosions = []
    asteroids = []
    items = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        if len(asteroids) < 5:
            asteroids.append(Asteroid())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                for spaceship in spaceships:
                    if event.key == spaceship.key_shoot and len(spaceship.bullets) < spaceship.max_bullets:
                        bullet = Bullet(spaceship.x+spaceship.width, spaceship.y +
                                        spaceship.height//2 - 2, 10, 5, spaceship.color, spaceship)
                        bullets.append(bullet)
                        spaceship.bullets.append(bullet)

            # if event.type == RED_HIT:
            #     explosion = Explosion(red.x + red.width//2 - EXPLOSION_WIDTH//2, red.y + red.height //
            #                           2 - EXPLOSION_HEIGHT//2, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, EXPLOSION_TIMEOUT)
            #     explosions.append(explosion)
            #     red.health -= 1

            if event.type == YELLOW_HIT:
                explosion = Explosion(yellow.x + yellow.width//2 - EXPLOSION_WIDTH//2, yellow.y + yellow.height //
                                      2 - EXPLOSION_HEIGHT//2, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, EXPLOSION_TIMEOUT)
                explosions.append(explosion)
                yellow.health -= 1

        winner_text = ""
        if yellow.health <= 0:
            winner_text = "Game Over!"

        if winner_text != "":
            draw_window(backgrounds, spaceships,
                        bullets, explosions, asteroids, items)
            draw_winner(winner_text)
            break

        for bullet in bullets:
            bullet.handle_movement(spaceships, bullets, asteroids, explosions)

        for asteroid in asteroids:
            asteroid.handle_movement(asteroids)

        keys_pressed = pygame.key.get_pressed()
        yellow.handle_movement(keys_pressed)
        yellow.handle_collisions(asteroids, items)

        draw_window(backgrounds, spaceships, bullets,
                    explosions, asteroids, items)

    main()


if __name__ == "__main__":
    main()
