import time
from .game import Game, SeekerException, HiderException
from .hider import Hider
from .seeker import Seeker
import random


class Match:
    DEFAULT_NUM_GAMES = 15
    MAX_INIT_TIME = 3

    def __init__(self, SeekerClass, HiderClass, games=DEFAULT_NUM_GAMES, render=False, frame_delay=0.2):
        self._count = 0
        self._render = render
        self._frame_delay = frame_delay
        self._valid_seeds = [1, 2, 5, 6, 7, 8, 11, 12, 14, 16, 19, 20, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 35, 38, 39, 41, 43, 45,
                    47, 48, 49, 51, 53, 55, 62, 63, 67, 69, 70, 71, 72, 75, 77, 79, 81, 82, 84, 86, 87, 90, 91, 92, 93, 95,
                    96, 97, 99, 101, 103, 107, 108, 112, 113, 114, 115, 117, 121, 122, 123, 128, 129, 131, 132, 134, 135,
                    138, 139, 146, 149, 153, 155, 157, 159, 161, 163, 166, 167, 168, 170, 171, 172, 175, 179, 181, 184, 190,
                    191, 192, 196, 198, 199]

        self._valid_seeds = random.sample(self._valid_seeds, games)

        self._SeekerClass = SeekerClass
        self._seeker_points = 0
        self._seeker_errors = 0
        self._seeker_info = []
        
        self._HiderClass = HiderClass
        self._hider_points = 0
        self._hider_errors = 0
        self._hider_info = []

    def run(self):
        for i, seed in enumerate(self._valid_seeds):
            print(f"------------- Game {i}/{len(self._valid_seeds)} -------------")
            try:
                start = time.time()
                hider = self._HiderClass()
                end = time.time()
                if (end-start) > self.MAX_INIT_TIME:
                    raise Exception(f"Hider took too long to initialize: {(end-start):.4f} seconds")
            except Exception as e:
                print(e)
                self._hider_errors += 1
                continue
        
            try: 
                start = time.time()
                seeker = self._SeekerClass()
                end = time.time()
                if (end-start) > self.MAX_INIT_TIME:
                    raise Exception(f"Seeker took too long to initialize: {(end-start):.4f} seconds")
            except Exception as e:
                print(e)
                self._seeker_errors += 1
                continue

            try:            
                start = time.time()
                game = Game(hider, seeker, seed, render=self._render, frame_delay=self._frame_delay)
                winner, timesteps = game.game_loop()
                seeker_score = game.max_turns - timesteps
                hider_score = timesteps
                self._seeker_points += seeker_score
                self._hider_points += hider_score
                self._seeker_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, Seeker Score {seeker_score}, Hider Score {hider_score}")
                self._hider_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, Seeker Score {seeker_score}, Hider Score {hider_score}")
                finish_time = time.time()
                print("Total time (sec):", finish_time - start)
                print(f"seeker_game score: {seeker_score}")
                print(f"seeker_total score: {self._seeker_points}")
                print(f"hider_game score: {hider_score}")
                print(f"hider_total score: {self._hider_points}")
                print(f"turn count: {timesteps}")
                print(f"seconds/turn: {(finish_time - start)/timesteps:.3f}")
            except SeekerException as e:
                self._seeker_errors += 1
                self._seeker_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, {e}")
                self._hider_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, Seeker got error. Hider not penalized")
            except HiderException as e:
                self._hider_errors += 1
                self._hider_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, {e}")
                self._seeker_info.append(f"Game {i}, Seed {self._valid_seeds[i]}, Hider got error. Seeker not penalized")


    def get_result(self):
        result = {
            "seeker_points": self._seeker_points,
            "hider_points": self._hider_points,
            "seeker_errors": self._seeker_errors,
            "hider_errors": self._hider_errors,
            "seeker_info": self._seeker_info,
            "hider_info": self._hider_info,
        }
        return result

    def get_bad_launch(type, msg):
        result = {
            "seeker_points": 0,
            "hider_points": 0,
            "seeker_errors": Match.DEFAULT_NUM_GAMES if type == Game.SEEKER else 0,
            "hider_errors": Match.DEFAULT_NUM_GAMES if type == Game.HIDER else 0,
            "seeker_info": f"{msg}. {'Does not affect seeker score' if type != Game.SEEKER else ''}",
            "hider_info": f"{msg}. {'Does not affect hider score' if type != Game.HIDER else ''}",
        }
        return result