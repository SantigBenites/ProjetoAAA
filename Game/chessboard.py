from attrs import define, field

@define
class Chessboard:
    board: list[int] = field(factory=list[int])
    timestamps: list[int] = field(factory=list[int])
    cooldown: int = 0