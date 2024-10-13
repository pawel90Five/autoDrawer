from PIL import ImageFilter, ImageGrab
import win32api
import win32con
from time import sleep

import fragmentation
# fname = "images/1.png"
# fname = 'images/2.jpg'
resize = (880, 490)


def get_cur():
    while True:
        print(win32api.GetCursorPos())
        sleep(0.5)


def make_path(pixels, size) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    size = (size[0] - 1, size[1] - 1)
    start, end = None, None
    k = 0
    res_path = []
    for y in range(0, size[1], 2):
        for x in range(size[0]):
            if pixels[x, y] == 0:
                if not start:
                    start = (x, y)
            else:
                if start:
                    end = (x - 1, y + k)
                    res_path.append((start, end))
                    start, end = None, None

        if start:
            end = (size[0], y + k)
            res_path.append((start, end))
            start, end = None, None

    return res_path


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def move_to(x, y, speed):
    # win32api.SetCursorPos((x, y))
    cur_pos = win32api.GetCursorPos()
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE, x - cur_pos[0], y - cur_pos[1], 0, 0
    )
    # old_pos = win32api.GetCursorPos()
    # diff_x = x - old_pos[0]
    # diff_y = y - old_pos[1]
    # diff_x = diff_x if diff_x > 0 else -diff_x
    # diff_y = diff_y if diff_y > 0 else -diff_y
    # max_coord = max(diff_x, diff_y)
    # min_coord = min(diff_x, diff_y)

    # aboba_k = max_coord / (min_coord if min_coord != 0 else 1)
    # k = int(aboba_k)
    # remainder = aboba_k - k

    # by_coord_shortest_new = y if diff_y < diff_x else x
    # by_coord_shortest_old = old_pos[1] if by_coord_shortest_new == y else old_pos[0]

    # by_coord_longest_new = x if by_coord_shortest_new == y else y
    # by_coord_longest_old = old_pos[0] if by_coord_longest_new == x else old_pos[1]

    # step_shortest = -1 if by_coord_shortest_old > by_coord_shortest_new else 1
    # step_longest = -1 if by_coord_longest_old > by_coord_longest_new else 1
    # diff = old_pos[1] if by_coord_shortest_new != y else old_pos[0]

    # remainder_to_k = 0
    # add_to_k = 0

    # if diff_x > diff_y:
    #     for i in range(
    #         by_coord_shortest_old, by_coord_shortest_new + step_shortest, step_shortest
    #     ):
    #         remainder_to_k += remainder
    #         if remainder_to_k >= 1:
    #             remainder_to_k -= 1
    #             add_to_k = 1
    #         else:
    #             add_to_k = 0
    #         for _ in range(0, k + add_to_k):
    #             sleep(speed)
    #             win32api.SetCursorPos((diff, i))
    #             diff = diff + step_longest
    # else:
    #     for i in range(
    #         by_coord_shortest_old, by_coord_shortest_new + step_shortest, step_shortest
    #     ):
    #         remainder_to_k += remainder
    #         if remainder_to_k >= 1:
    #             remainder_to_k -= 1
    #             add_to_k = 1
    #         else:
    #             add_to_k = 0
    #         for _ in range(0, k):
    #             sleep(speed)
    #             win32api.SetCursorPos((i, diff))
    #             diff = diff + step_longest

    # win32api.SetCursorPos((x, y))


def drag(x, y, dx, dy, speed):
    
    move_to(x, y, speed)
    sleep(speed)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    move_to(dx, dy, speed)
    sleep(speed)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, dx, dy, 0, 0)


def draw(
    path: list[tuple[tuple[int, int], tuple[int, int]]],
    relative: tuple[int, int] = (0, 0),
    delay: float = 1,
):
    sleep(delay)
    win32api.SetCursorPos((relative[0] + path[0][0][0], relative[1] + path[0][0][1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    for start, end in path:
        drag(
            relative[0] + start[0],
            relative[1] + start[1],
            relative[0] + end[0],
            relative[1] + end[1],
            0.001,
        )
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def main():
    im = ImageGrab.grabclipboard().convert("L")
    # im = Image.open(fname).convert("L")
    # cnt = im.filter(ImageFilter.CONTOUR)
    smooth = im.filter(ImageFilter.SMOOTH_MORE)
    cnt = smooth.filter(ImageFilter.CONTOUR)
    crop = cnt.crop((1, 1, im.size[0] - 1, im.size[1] - 1))
    small = crop.resize(resize)
    res = small.point(lambda x: 255 if x > 230 else 0)

    # res.show()
    pixels = res.load()

    path: list[tuple[tuple[int, int], tuple[int, int]]] = make_path(pixels, resize)

    relative = (1920 + 724, 214)
    fragments = fragmentation.make_fragments(path) 
    click(1920 + 586, 946)  # set tight cursor
    click(relative[0], relative[1])
    
    # path = []
    # for i in range(480): 
    #     if i % 2 == 0:
    #         path.append(((0, i), (800, i+1)))
    #     else:
    #         path.append(((0, i-1), (800, i)))
    print(len(fragments))
    for fragment in fragments:
        draw(fragment, relative)


if __name__ == "__main__":
    main()
