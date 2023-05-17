from gym.envs.registration import register
from Game.chess import Game

def _make_env():
    env = Game()

    return env

register(
    id='kungFuChess-v0',
    entry_point='_make_env',
)