from attrs import define

from Game.chessboard import Chessboard
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from threading import Event


@define
class RlPlayerConfig:
    c_board: Chessboard
    color: int
    stop: Event
    NN: NeuralNetwork


@define
class GAPlayerConfig:
    c_board: Chessboard
    color: int
    stop: Event
    genotype: dict[str, int]


@define
class SFPlayerConfig:
    c_board: Chessboard
    color: int
    stop: Event


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
