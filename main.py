import os
import sys
import time

# ---------------------------------------------------------------------------
# Lab 1, variant 1: France / pattern a / y = x^2 /
# condition: count of numbers less than 0 and greater than 0.
# Needed next to this file: sequence.txt
# ---------------------------------------------------------------------------

ESC = "\033"
RESET = ESC + "[0m"

# 256-colour palette codes are fixed (they do not depend on the terminal theme),
# unlike the basic 30-47 codes that themes often remap.
BLACK_BG = ESC + "[48;5;16m"    # pure black   (0, 0, 0)
WHITE_BG = ESC + "[48;5;231m"   # pure white   (255, 255, 255)
BLUE_BG = ESC + "[48;5;19m"     # French blue
RED_BG = ESC + "[48;5;196m"     # French red


def setup_console():
    # Make the console understand UTF-8 output and ANSI escape sequences.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    # On Windows, running any command enables ANSI processing in the console.
    os.system("")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_flag():
    blue = BLUE_BG + "   " + RESET
    white = WHITE_BG + "   " + RESET
    red = RED_BG + "   " + RESET

    print("Flag of France")
    for _ in range(5):
        print(blue + white + red)


def print_pattern():
    # Pattern a (X shape): black cells in the corners and in the center.
    black_cell = BLACK_BG + "    " + RESET
    white_cell = WHITE_BG + "    " + RESET

    print("\nPattern a")
    pattern = [
        [black_cell, white_cell, black_cell],
        [white_cell, black_cell, white_cell],
        [black_cell, white_cell, black_cell],
    ]

    # In the assignment picture the five black squares sit on a white
    # background. A white margin reproduces that, and it keeps the black
    # cells visible even on a pure-black terminal (for example in VS Code).
    frame_bg = WHITE_BG
    side = frame_bg + "  " + RESET
    edge = frame_bg + " " * (4 * 3 + 4) + RESET

    print(edge)
    for row in pattern:
        # Each cell is 4 columns wide, so every row is printed twice
        # to make the cells look square.
        line = side + "".join(row) + side
        print(line)
        print(line)
    print(edge)


def animate_cursor():
    # 4 frames; every frame is drawn with cursor-control escape sequences:
    #   ESC[2J      clear the screen
    #   ESC[H       move the cursor to the top-left corner
    #   ESC[row;colH  move the cursor to a given position
    #   ESC[?25l / ESC[?25h  hide / show the real cursor
    frames = ["O----", "-O---", "--O--", "---O-"]

    # Start from a clean screen (ESC[3J also erases the scrollback).
    print(ESC + "[2J" + ESC + "[3J" + ESC + "[H", end="")
    print(ESC + "[?25l", end="")
    try:
        for frame in frames:
            # Home the cursor, then erase from there to the end of the screen:
            # the frame is redrawn in place, old frames are not pushed up.
            print(ESC + "[H" + ESC + "[J", end="")
            print("Cursor animation")
            print(ESC + "[4;5H" + frame, end="", flush=True)
            time.sleep(0.5)
    finally:
        print(ESC + "[?25h", end="")

    print(ESC + "[6;1H" + "Animation finished.")


def find_sequence_file():
    # Look next to this script first (works when started from an editor),
    # then in the current working directory.
    script_folder = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_folder, "sequence.txt"),
        os.path.join(os.getcwd(), "sequence.txt"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("\n".join(candidates))


def read_numbers():
    path = find_sequence_file()
    # utf-8-sig also handles files saved with a BOM.
    with open(path, "r", encoding="utf-8-sig") as file:
        return [float(value) for value in file.read().split()]


def make_bar(percent, width=50):
    # One cell = 2 %, partial blocks give 1/8-cell precision,
    # so 49.60 % and 50.40 % are visibly different.
    partial = " ▏▎▍▌▋▊▉"
    eighths = round(percent / 100 * width * 8)
    full, rest = divmod(eighths, 8)
    return "█" * full + (partial[rest] if rest else "")


def print_percentage_chart():
    try:
        numbers = read_numbers()
    except FileNotFoundError as error:
        print("\nError: sequence.txt was not found. Looked here:")
        print(error)
        print("Put sequence.txt in the same folder as main.py.")
        return
    except ValueError:
        print("\nError: sequence.txt contains invalid data.")
        return

    # Variant 1: how many numbers are less than 0 and how many are greater
    # than 0 (zeros belong to neither group). The two counts make 100 %.
    negative_count = sum(number < 0 for number in numbers)
    positive_count = sum(number > 0 for number in numbers)
    total = negative_count + positive_count

    print("\nNumber statistics")
    print("Negative numbers (< 0):", negative_count)
    print("Positive numbers (> 0):", positive_count)

    if total == 0:
        print("There are no positive or negative numbers.")
        return

    negative_percent = negative_count / total * 100
    positive_percent = positive_count / total * 100

    print("\nPercentage chart (100 % = 50 cells)")
    print(f"Negative {negative_percent:6.2f}% |{make_bar(negative_percent)}")
    print(f"Positive {positive_percent:6.2f}% |{make_bar(positive_percent)}")
    print(f"Total    {negative_percent + positive_percent:6.2f}%")


def print_function_graph():
    # Extra task: first quadrant of y = x^2, 10 rows high (y = 0 ... 9).
    # The picture is generated with cursor-positioning escape sequences,
    # not printed line by line:
    #   ESC 7 / ESC 8   save / restore the cursor position
    #   ESC[nB          move the cursor n rows down
    #   ESC[nG          move the cursor to column n
    max_y = 9
    max_x = 3
    x_scale = 8                 # columns per unit of x
    axis_col = 4                # column of the y axis
    rows = max_y + 3            # title + 10 graph rows + labels row

    def put(row, col, text):
        # row is counted from the saved position (0 = first reserved line)
        return ESC + "8" + (ESC + f"[{row}B" if row else "") + ESC + f"[{col}G" + text

    # Reserve free lines under the existing output, go back up, remember place.
    print("\n" * rows, end="")
    print(ESC + f"[{rows}A" + "\r" + ESC + "7", end="")

    out = [put(0, 1, "Extra task: y = x^2 (first quadrant)")]
    axis_row = 1 + max_y        # row of y = 0

    # y axis with labels
    for y in range(max_y + 1):
        out.append(put(axis_row - y, 1, f"{y:2}"))
        out.append(put(axis_row - y, axis_col, "|"))

    # x axis with labels
    out.append(put(axis_row, axis_col, "+" + "-" * (max_x * x_scale + 2) + "> x"))
    for x in range(max_x + 1):
        out.append(put(axis_row + 1, axis_col + x * x_scale, str(x)))

    # the curve (green *); slope < 1 row per column, so it has no gaps
    steps = 200
    for i in range(steps + 1):
        x = max_x * i / steps
        y = x ** 2
        row = axis_row - round(y)
        col = axis_col + round(x * x_scale)
        out.append(put(row, col, ESC + "[32m*" + RESET))

    # leave the cursor below the picture
    out.append(ESC + "8" + ESC + f"[{rows}B" + "\r")
    print("".join(out), end="", flush=True)


def main():
    setup_console()

    clear_screen()
    print_flag()
    print_pattern()

    input("\nPress Enter to start the animation...")
    animate_cursor()

    input("\nPress Enter to show the percentage chart...")
    print_percentage_chart()

    input("\nPress Enter to show the extra function graph...")
    print_function_graph()


if __name__ == "__main__":
    main()
