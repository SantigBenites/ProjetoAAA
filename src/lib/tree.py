class Tree:
    def __init__(self, data, parent: Tree) -> None:
        self.data = data
        self.children: list[Tree] = []
