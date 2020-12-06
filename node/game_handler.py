import config

white_points: int = 0
black_points: int = 0
red_points: int = 0


def process_arg(arg: str):
    global white_points
    global red_points
    global black_points

    if arg == config.WHITE_POINT_INCREMENT:
        white_points += 1
    elif arg == config.BLACK_POINT_INCREMENT:
        black_points += 1
    elif arg == config.RED_POINT_INCREMENT:
        red_points += 1
    elif arg == config.CLEAR_POINTS:
        white_points = 0
        red_points = 0
        black_points = 0


def get_final() -> int:
    global white_points
    global red_points
    global black_points

    if red_points > max(white_points, black_points):
        return 1
    elif black_points > max(white_points, red_points):
        return 2
    else:
        return 0
