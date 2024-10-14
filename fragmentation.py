class Line:
    def __init__(self, path: tuple[tuple[int, int], tuple[int, int]]):
        self.path = path
        self.childs: list[Line] = []

    def add_child(self, path: tuple[tuple[int, int], tuple[int, int]]):
        self.childs.append(Line(path))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Line):
            return False
        return self.path == value.path

    def __str__(self, level: int = 1) -> str:
        tabs = level * "\t"
        return f'{self.path}{': \n' + tabs + f'{', \n'+tabs if level >= 1 else ''}'.join([child.__str__(level + 1) for child in self.childs]) if self.childs else ''}'


def make_fragments(
    path: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[list[tuple[tuple[int, int], tuple[int, int]]]]:
    
    fragments: list[list[tuple[tuple[int, int], tuple[int, int]]]] = []
    step_y = 2

    for i_way in range(len(path)):
        fragment = []
        fragment.append(path[i_way])

        for i in range(i_way + 1, len(path)):
            if path[i_way][0][1] + step_y == path[i][0][1]:
                if (
                    path[i_way][0][0] in range(path[i][0][0], path[i][1][0] + 1)
                    or path[i_way][1][0] in range(path[i][0][0], path[i][1][0] + 1)
                    or path[i][0][0] in range(path[i_way][0][0], path[i_way][1][0] + 1)
                    or path[i][1][0] in range(path[i_way][0][0], path[i_way][1][0] + 1)
                ):
                    fragment.append(path[i])
            elif path[i_way][0][1] + step_y < path[i][0][1]:
                break

        fragments.append(fragment)

    for fragment in fragments:
        for way in fragment:
            for j in range(len(fragments)):
                if way in fragments[j] and fragment != fragments[j]:
                    fragments[j].remove(way)
                    for j_way in fragments[j]:
                        if j_way not in fragment:
                            fragment.append(j_way)
    res = []
    for fragment in fragments:
        if fragment:
            res.append(fragment)

    return res

def make_fragments_lines(
    path: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[Line]:
    fragments = make_fragments(path)
    res = []
    for fragment in fragments:
        head = Line(fragment[0])
        find_childs(head, fragment)
        res.append(head)
    return res


def find_childs(line: Line, path:list[tuple[tuple[int, int], tuple[int, int]]]):
    step_y = 2
    #   print(path)
    for i in reversed(range(len(path))):
        if line.path[0][1] + step_y == path[i][0][1]:
            if (
                line.path[0][0] in range(path[i][0][0], path[i][1][0] + 1)
                or line.path[1][0] in range(path[i][0][0], path[i][1][0] + 1)
                or path[i][0][0] in range(line.path[0][0], line.path[1][0] + 1)
                or path[i][1][0] in range(line.path[0][0], line.path[1][0] + 1)
            ):
                line.add_child(path[i])
                del path[i]

    for child in line.childs:
        find_childs(child, path)


def make_tests() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    path = [
        ((10, 1), (100, 1)),
        ((200, 1), (240, 1)),
        ((6, 3), (105, 3)),
        ((200, 3), (240, 3)),
        ((4, 5), (30, 5)),
        ((60, 5), (109, 5)),
        ((115, 5), (160, 5)),
        ((200, 5), (240, 5)),
        ((1, 7), (10, 7)),
        ((20, 7), (80, 7)),
        ((90, 7), (120, 7)),
        ((200, 7), (240, 7)),
        ((5, 9), (110, 9)),
        ((10, 13), (100, 13)),
        ((6, 15), (105, 15)),
        ((4, 17), (30, 17)),
        ((60, 17), (109, 17)),
        ((115, 17), (160, 17)),
        ((1, 19), (10, 19)),
        ((20, 19), (80, 19)),
        ((90, 19), (120, 19)),
        ((5, 21), (110, 21)),
    ]
    return path


def main():
    # fragments = make_fragments(make_tests())
    # print(*fragments, sep="\n")
    # line = Line(((10, 1), (100, 1)))
    # line.add_child(((200, 1), (240, 1)))
    # line.add_child(((4, 5), (30, 5)))
    # for child in line.childs:
    #     child.add_child(((6, 3), (105, 3)))
    #     child.add_child(((200, 3), (240, 3)))
    print(*make_fragments_lines(make_tests()), sep='\n')
    # print(line)
    # print(fragments)
    # lines_traversal(line)


if __name__ == "__main__":
    main()
