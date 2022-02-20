def polygonal(points: list[tuple], center: float):
    """

    :param points: list of (x, y)
    :param center: center x coordinate
    :return: corresponding y coordinate
    """
    if center == 0 and points[0][0] > 0:
        return 0
    for i in range(len(points) - 1):
        if points[i][0] <= center <= points[i + 1][0]:
            return interpolate(center, *points[i], *points[i + 1])
    return points[-1][1]


def interpolate(center: float, left_x: int, left_y: float, right_x: int, right_y: float):
    return (center - left_x) * (right_y - left_y) / (right_x - left_x) + left_y
