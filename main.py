import json
import random

import pygame as pg

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

BUTTON_WIDTH = 200
BUTTON_HEIGHT= 60

DOG_WIDTH = 310
DOG_HEIGHT = 500

DOG_Y = 100

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

fond = pg.font.Font(None, 40)
mini_fond = pg.font.Font(None, 15)
fond_maxi = pg.font.Font(None, 200)

ICON_SIZE = 80
PADDING = 5

FOOD_SIZE = 200

TOY_SIZE = 100

FPS = 60



def load_image(file, widht, height):
    image = pg.image.load(file).convert_alpha()
    image= pg.transform.scale(image, (widht, height))
    return image

def text_render(text):
    return fond.render(str(text), True, "black")

class Item:
    def __init__(self, name, price, file, is_bought, is_put_on):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on

        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT// 1.7)
        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []
        for item in data:
            self.items.append(Item(*item.values()))

        self.current_item = 0

        self.items_rect = self.items[0].image.get_rect()
        self.items_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.back_button = Button("Назад", MENU_NAV_XPAD + 30, SCREEN_HEIGHT-MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH), height=int(BUTTON_HEIGHT), func=self.to_back)

        self.puton_button = Button("Надеть", MENU_NAV_XPAD + 30, SCREEN_HEIGHT-MENU_NAV_YPAD - 50 - PADDING,
                                  width=int(BUTTON_WIDTH), height=int(BUTTON_HEIGHT), func=self.use_item)

        self.buy_button =  Button("Купить", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                  SCREEN_HEIGHT // 1.5 + 10,
                                  width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                  func=self.buy)

        self.price_text =text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH -150, 130)

        self.byu_text = text_render("Куплено")
        self.byu_text_rect = self.byu_text.get_rect()
        self.byu_text_rect.midright = (SCREEN_WIDTH - 140, 200)

    def to_back(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)


    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def use_item(self):
        self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on


    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.puton_button.update()
        self.buy_button.update()


    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.puton_button.is_clicked(event)
        self.buy_button.is_clicked(event)


    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money-= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))

        screen.blit(self.items[self.current_item].image, self.items_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

        if self.items[self.current_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.puton_button.draw(screen)
        self.buy_button.draw(screen)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.byu_text, self.byu_text_rect)

class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_power=medicine_power
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Food("Яблоко",20, "images/food/apple.png", 5),
                      Food("Косточка", 45, "images/food/bone.png", 5),
                      Food("Корм обычный", 60,"images/food/dog food.png", 15),
                      Food("Корм элитный", 130, "images/food/dog food elite.png", 20, medicine_power= 5),
                      Food("Мясо", 80, "images/food/meat.png", 25),
                      Food("Лекарство", 200, "images/food/medicine.png", 0, medicine_power=25)]
        self.current_item = 0

        self.items_rect = self.items[0].image.get_rect()
        self.items_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.back_button = Button("Назад", MENU_NAV_XPAD + 30, SCREEN_HEIGHT-MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH), height=int(BUTTON_HEIGHT), func=self.to_back)

        self.buy_button =  Button("Съесть", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                  SCREEN_HEIGHT // 1.5 + 10,
                                  width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                  func=self.buy)

        self.price_text =text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_back(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)


    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)


    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.buy_button.update()


    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.buy_button.is_clicked(event)


    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money-= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety >100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))

        screen.blit(self.items[self.current_item].image, self.items_rect)



        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.buy_button.draw(screen)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)

class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.ball = load_image("images/toys/ball.png", TOY_SIZE, TOY_SIZE)
        self.blue_bone = load_image("images/toys/blue bone.png", TOY_SIZE, TOY_SIZE)
        self.red_bone = load_image("images/toys/red bone.png", TOY_SIZE, TOY_SIZE)

        file = random.choice(("images/toys/ball.png", "images/toys/blue bone.png","images/toys/red bone.png"))
        self.image = load_image(file, TOY_SIZE, TOY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - TOY_SIZE)
        self.rect.y = 30

    def update(self):
        self.rect.y += 2


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/dog.png", DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.rect = self.image.get_rect()
        self.rect.center =  (SCREEN_WIDTH//2, SCREEN_HEIGHT - MENU_NAV_YPAD - 10)


    def update(self):
        dog_key = pg.key.get_pressed()
        if dog_key[pg.K_a]:
            self.rect.x -= 2
        if dog_key[pg.K_d]:
            self.rect.x += 2



class MiniGame:
    def __init__(self, game):
        self.game = game

        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 15

    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 15

    def update(self):

        if random.randint(0, 100) == 0:
            self.toys.add(Toy())
        self.toys.update()
        self.dog.update()
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time>self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))


        screen.blit(self.dog.image, self.dog.rect)

        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))

        self.toys.draw(screen)





class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_fond=fond, func=None):
        self.func = func
        self.idle_image = load_image("images/button.png", width, height)
        self.pressed_image = load_image("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect =self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_fond = text_fond
        self.text = self.text_fond.render(str(text), True, "black")
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
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False




class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        with open("save.json", "r",  encoding="utf-8") as f:
            data = json.load(f)
        print(data)
        self.health = data["health"]
        self.satiety = data["satiety"]
        self.happiness = data["happiness"]
        self.money = data["money"]
        self.coins_per_second = data["coins_per_second"]
        self.costs_of_upgrade = {}
        for key, value in data["costs_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value



        self.mode = "Main"

        self.backgrond = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)
        self.satiely_image = load_image("images/satiety.png",ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)
        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)
        self.dog = load_image("images/dog.png", DOG_WIDTH, DOG_HEIGHT)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING
        self.eat_button = Button("Еда", button_x, PADDING + BUTTON_HEIGHT, func=self.food_menu_on)

        self.clothes_button = Button("Одежда",button_x , PADDING * 2 + BUTTON_HEIGHT + ICON_SIZE,
                                     func=self.clothes_menu_on)

        self.play_button = Button("Игра",button_x, PADDING * 3 + ICON_SIZE + BUTTON_HEIGHT * 2.3, func=self.game_on )

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_fond=mini_fond, func=self.increase_money)

        self.buttons = [self.eat_button, self.play_button, self.clothes_button]
        self.clothes_menu = ClothesMenu(self, data["clothes"])

        self.food_menu = FoodMenu(self)

        self.DECREASE = pg.USEREVENT +2
        pg.time.set_timer(self.DECREASE, 1000)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.mini_game = MiniGame(self)

        self.clock = pg.time.Clock()

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def increase_money(self):
        print("incre")
        for cost, check in self.costs_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = {
                        "health": 100,
                        "satiety": 100,
                        "happiness": 100,
                        "money": 1,
                        "coins_per_second": 1,
                        "costs_of_upgrade": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "clothes": [
                            {
                                "name": "Синяя футболка",
                                "price": 30,
                                "image": "images/items/blue t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Ботинки",
                                "price": 70,
                                "image": "images/items/boots.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Бантик",
                                "price": 45,
                                "image": "images/items/bow.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Кепка",
                                "price": 55,
                                "image": "images/items/cap.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Золотая Цепочка",
                                "price": 220,
                                "image": "images/items/gold chain.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Шляпа",
                                "price": 80,
                                "image": "images/items/hat.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Красная футболка",
                                "price": 35,
                                "image": "images/items/red t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Серебряная Цепочка",
                                "price": 150,
                                "image": "images/items/silver chain.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Солнцезащитные очки",
                                "price": 65,
                                "image": "images/items/sunglasses.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Жёлтая футболка",
                                "price": 35,
                                "image": "images/items/yellow t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            }
                        ]
                    }
                else:
                    data = {
                        "health": self.health,
                        "satiety": self.satiety,
                        "happiness": self.happiness,
                        "money": self.money,
                        "coins_per_second": self.coins_per_second,
                        "costs_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]
                        },
                        "clothes": []
                    }

                    for item in self.clothes_menu.items:
                        print(item.image, 1)
                        print(item.is_bought, 2)

                        data["clothes"].append({"name":item.name,
                                          "price": item.price,
                                          "image": item.image,
                                          "is_bought" :item.is_bought,
                                          "is_put_on":item.is_put_on})

                with open("save1.json", "w", encoding="utf-8") as f:
                    json.dump(data, f)


                pg.quit()
                exit()

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"
                    print("main")


            if event.type == self.INCREASE_COINS:
                self.money +=1

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)
                if chance<=5:
                    self.satiety -=1
                elif 5<chance<9:
                    self.happiness -= 1
                else:
                    self.health -=1

            if self.mode == "Main":
                for button in self.buttons:
                    button.is_clicked(event)
            elif self.mode == "Clothes menu":
                self.clothes_menu.is_clicked(event)
            elif self.mode == "Food menu":
                self.food_menu.is_clicked(event)



    def update(self):
        if self.mode == "Mini game":
            self.mini_game.update()
        elif self.mode == "Clothes menu":
            self.clothes_menu.update()
        elif self.mode == "Food menu":
            self.food_menu.update()
        else:
            for button in self.buttons:
                button.update()

        if self.happiness <= 0 or self.satiety <= 0 or self.health <= 0:
            self.mode = "Game over"



    def draw(self):
        self.screen.blit(self.backgrond, (0, 0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiely_image, (PADDING, PADDING + 80))
        self.screen.blit(self.health_image, (PADDING, PADDING + 160))
        self.screen.blit(self.money_image, (PADDING + 800, PADDING))
        self.screen.blit(self.dog, (SCREEN_WIDTH // 2 - 170, DOG_Y))

        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING *6))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING +110))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING + 185))
        self.screen.blit(text_render(self.money), (PADDING + 775, PADDING + 30))

        self.eat_button.draw(self.screen)
        self.clothes_button.draw(self.screen)
        self.play_button.draw(self.screen)
        self.upgrade_button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, (SCREEN_WIDTH // 2 - 170, DOG_Y))


        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)

        if self.mode == "Mini game":
            self.mini_game.draw(self.screen)

        if self.mode == "Game over":
            text = fond_maxi.render("ПРОИГРЫШ", True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    Game()
