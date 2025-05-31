import pyxel
from model import GameModel
from view import GameView

class GameController:
    def __init__(self, model: GameModel, view: GameView):
        self._model = model
        self._view = view

    def start(self):
        model = self._model

        self._view.start(model.fps, self, self)

    def update(self):
        if self._model.waiting_for_egghancement:
            if self._view.pressing_key_1():
                self._model.apply_egghancement(1)
            elif self._view.pressing_key_2():
                self._model.apply_egghancement(2)
            elif self._view.pressing_key_3():
                self._model.apply_egghancement(3)
        else:
            self._model.update(
                self._view.pressing_left_key(),
                self._view.pressing_right_key(),
                self._view.pressing_up_key(),
                self._view.pressing_down_key(),
                self._view.pressing_attack_key(),
                self._view.pressing_restart_key()
            )


    def draw(self):
        pyxel.cls(0)
            
        self._view.draw_egg(self._model.egg)
        self._view.draw_egg_stats(self._model.egg)
        self._view.draw_eggnemies(self._model.normal_eggnemies)
        self._view.draw_eggnemies_hp(self._model.normal_eggnemies)
        self._view.draw_world_border(self._model.egg.relative_x, self._model.egg.relative_y)
        self._view.draw_eggnemies_defeated(self._model.eggnemies_defeated)
        self._view.draw_leaderboard(self._model.leaderboard, self._model.fps)
        self._view.draw_time_passed(self._model.total_frames_passed, self._model.fps)

        for boss in self._model.bosses:
            self._view.draw_boss(boss)
            self._view.draw_boss_hp(boss)

        if self._model.game_over_loss:
            self._view.draw_restart_option_message()

        if self._model.waiting_for_egghancement:
            self._view.draw_egghancement_prompt()

        

