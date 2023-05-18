from attrs import define

from Game.chessboard import Chessboard
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from threading import Event


@define
class RlPlayerConfig:
    c_board: Chessboard
    color: int
    NN: NeuralNetwork


@define
class GAPlayerConfig:
    c_board: Chessboard
    color: int
    genotype: dict[str, int]


@define
class SFPlayerConfig:
    c_board: Chessboard
    color: int


@define
class PlayerDef:
    type: str
    config: RlPlayerConfig | GAPlayerConfig | SFPlayerConfig


@define
class RunConfig:
    cooldown: float
    max_episodes: int
    base_board: list[int]
    ga_genotype: dict[str, int]
    time_out: int
    nn_win_reward: int
    discount_factor: float
    verbose: bool
