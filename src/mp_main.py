import multiprocessing as mp


class MpTest:

    def __init__(self, t_size: int):
        self.size = size

    def play(self) -> int:
        return self.size


def get_pairs(size: int) -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    for i in range(size):
        res.append((i, 100+i))
    return res
