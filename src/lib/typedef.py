from attrs import define

from ReinforcementLearning.NeuralNetwork import NeuralNetwork


@define
class RlPlayerConfig:
    color: int
    NN: NeuralNetwork


@define
class GAPlayerConfig:
    color: int
    genotype: dict[str, int]


@define
class SFPlayerConfig:
    color: int


@define
class PlayerDef:
    type: str
    config: RlPlayerConfig | GAPlayerConfig | SFPlayerConfig


@define
class GameReturn:
    white_x: list[list[int]]
    white_y: list[float]
    black_x: list[list[int]]
    black_y: list[float]
    duration: float
    moves_num: int
    winner: int


@define
class RunConfig:
    cooldown: float
    StockFish_episodes: int
    train_episodes: int
    pop_size: int
    base_board: list[int]
    ga_genotype: dict[str, int]
    time_out: int
    nn_win_reward: int
    discount_factor: float
    verbose: bool
