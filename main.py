import pygame as pg

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

BUTTON_WIDTH = 200
BUTTON_HEIGHT= 60

fond = pg.font.Font(None, 40)
mini_fond = pg.font.Font(None, 15)


ICON_SIZE = 80
PADDING = 5

def load_image(file, widht, height):
    image = pg.image.load(file).convert_alpha()
    image= pg.transform.scale(image, (widht, height))
    return image

def text_render(text):
    return fond.render(str(text), True, 'black')

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_fond=fond, func=None):
        self.func = func
        self.idle_image = load_image('images/button.png', width, height)
        self.pressed_image = load_image('images/button_clicked.png', width, height)
        self.image = self.idle_image
        self.rect =self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_fond = text_fond
        self.text = self.text_fond.render(str(text), True, 'black')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.is_pressed = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func

        self.func


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.health = 100
        self.satiely = 100
        self.happiness = 100
        self.money = 100
        self.coins_per_second = 1
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}

        self.backgrond = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happiness_image = load_image('images/happiness.png', ICON_SIZE, ICON_SIZE)
        self.satiely_image = load_image('images/satiety.png',ICON_SIZE, ICON_SIZE)
        self.health_image = load_image('images/health.png', ICON_SIZE, ICON_SIZE)
        self.money_image = load_image('images/money.png', ICON_SIZE, ICON_SIZE)
        self.dog = load_image('images/dog.png', 310, 500)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING
        self.eat_button = Button('Еда', button_x, PADDING + BUTTON_HEIGHT)
        self.clothes_button = Button('Одежда',button_x , PADDING * 2 + BUTTON_HEIGHT + ICON_SIZE)
        self.play_button = Button("Игра",button_x, PADDING * 3 + ICON_SIZE + BUTTON_HEIGHT * 2.3 )

        self.upgrade_button = Button('Улучшить', SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_fond=mini_fond, func=self.increase_money)

        # self.buttons = [self.eat_button, self.play_button, self.clothes_button]

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def increase_money(self):
        print('incre')
        for cost, check in self.costs_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            self.eat_button.is_clicked(event)
            self.clothes_button.is_clicked(event)
            self.play_button.is_clicked(event)
            self.upgrade_button.is_clicked(event)


            if event.type == self.INCREASE_COINS:
                self.money +=1



    def update(self):
        self.eat_button.update()
        self.clothes_button.update()
        self.play_button.update()
        self.upgrade_button.update()


    def draw(self):
        self.screen.blit(self.backgrond, (0, 0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiely_image, (PADDING, PADDING + 80))
        self.screen.blit(self.health_image, (PADDING, PADDING + 160))
        self.screen.blit(self.money_image, (PADDING + 800, PADDING))
        self.screen.blit(self.dog, (300, 100))

        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING *6))
        self.screen.blit(text_render(self.satiely), (PADDING + ICON_SIZE, PADDING +110))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING + 185))
        self.screen.blit(text_render(self.money), (PADDING + 775, PADDING + 30))

        self.eat_button.draw(self.screen)
        self.clothes_button.draw(self.screen)
        self.play_button.draw(self.screen)
        self.upgrade_button.draw(self.screen)

        pg.display.flip()


if __name__ == "__main__":
    Game()
