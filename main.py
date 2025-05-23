import pyxel
import json
from abc import ABC
import random

with open("settings.json") as f:
    settings = json.load(f)

# Global variables
i_frame: int = settings["fps"]
egg_range: int = 10
eggnemies_defeated: int = 0

class Egg(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = hp
        self.hp = hp

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

class Eggnemy(Egg):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        super().__init__(x, y, width, height, hp)

def is_in_collision(egg: Egg, enemy: Eggnemy) -> bool:
    if egg.right < enemy.left:
        return False
    elif egg.left > enemy.right:
        return False
    else:
        if egg.top > enemy.bottom:
            return False
        elif egg.bottom < enemy.top:
            return False
        else:
            return True

def is_in_range(egg: Egg, enemy: Eggnemy) -> bool:
    if enemy.left - egg.right > egg_range:
        return False
    elif egg.left - enemy.right > egg_range:
        return False
    else:
        if egg.top - enemy.bottom > egg_range:
            return False
        elif enemy.top - egg.bottom > egg_range:
            return False
        else:
            return True

def remove_enemy(enemy: Eggnemy, Eggnemies: list[Eggnemy]):
    Eggnemies.remove(enemy)

# Initialize entities
egg = Egg(
    settings["world_width"] // 2,
    settings["world_height"] // 2,
    settings["egg_width"],
    settings["egg_height"],
    settings["egg_hp"]
)

enemies: list[Eggnemy] = [
    Eggnemy(
        random.randint(0, settings["world_width"]),
        random.randint(0, settings["world_height"]),
        settings["eggnemy_width"],
        settings["eggnemy_height"],
        1,
    )
    for _ in range(settings["eggnemy_count"])
]

def update():
    global i_frame
    global eggnemies_defeated

    speed = 2

    if egg.hp == 0:
        return

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        egg.x = max(0, egg.x - speed)
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        egg.x = min(settings["world_width"] - egg.width, egg.x + speed)
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        egg.y = min(settings["world_height"] - egg.height, egg.y + speed)
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        egg.y = max(0, egg.y - speed)

    for enemy in enemies:
        if enemy.x < egg.x:
            enemy.x += 1
        if enemy.x > egg.x:
            enemy.x -= 1
        if enemy.y < egg.y:
            enemy.y += 1
        if enemy.y > egg.y:
            enemy.y -= 1

    for enemy in enemies:
        if i_frame > 0:
            break
        if is_in_collision(egg, enemy):
            egg.hp -= 1
            i_frame = settings["fps"]

    if i_frame > 0:
        i_frame -= 1

    if pyxel.btn(pyxel.KEY_L):
        for enemy in enemies[:]:
            if is_in_range(egg, enemy):
                enemy.hp -= 1
                remove_enemy(enemy, enemies)
                eggnemies_defeated += 1
                print(eggnemies_defeated)

def draw_egg(egg: Egg):
    pyxel.rect(egg.x, egg.y, egg.width, egg.height, 7)

def draw_egg_hp(egg: Egg):
    pyxel.text(egg.x - 5, egg.y + 10, f"{egg.hp}/{egg.max_hp}", 7)

def draw_range(egg: Egg):
    pyxel.rectb(egg.x - egg_range, egg.y - egg_range, egg.width + 2 * egg_range, egg.height + 2 * egg_range, 1)

def draw_eggnemies(enemies: list[Eggnemy]) -> None:
    for enemy in enemies:
        pyxel.rect(enemy.x, enemy.y, enemy.width, enemy.height, 8)

def draw_eggnemies_defeated(eggnemies_defeated: int):
    pyxel.text(10, 10, f'{eggnemies_defeated}', 7)

def draw_eggnemies_hp(enemies: list[Eggnemy]) -> None:
    for enemy in enemies:
        pyxel.text(enemy.x - 5, enemy.y + 10, f"{enemy.hp}/{enemy.max_hp}", 7)

def draw():
    pyxel.cls(0)
    draw_egg(egg)
    draw_egg_hp(egg)
    draw_range(egg)
    draw_eggnemies(enemies)
    draw_eggnemies_defeated(eggnemies_defeated)
    draw_eggnemies_hp(enemies)

def main():
    pyxel.init(settings["world_width"], settings["world_height"], fps=settings["fps"])
    pyxel.run(update, draw)

if __name__ == "__main__":
    main()
