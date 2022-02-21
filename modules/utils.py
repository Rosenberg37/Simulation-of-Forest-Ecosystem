import matplotlib.pyplot as plt


def polygonal(points: list[tuple], center: float):
    """

    :param points: list of (x, y)
    :param center: center x coordinate
    :return: corresponding y coordinate
    """
    points = sorted(points, key=lambda a: a[0])
    if center == 0 and points[0][0] > 0:
        return 0
    for i in range(len(points) - 1):
        if points[i][0] <= center <= points[i + 1][0]:
            return interpolate(center, *points[i], *points[i + 1])
    return points[-1][1]


def interpolate(center: float, left_x: int, left_y: float, right_x: int, right_y: float):
    return (center - left_x) * (right_y - left_y) / (right_x - left_x) + left_y


def draw(points: list[tuple], x: list, name: str, color: str):
    y = [polygonal(points, i) for i in x]
    plt.plot(x, y, color=color, linewidth=2, linestyle='-', label=name)
    plt.legend(loc='best')
    return x, y


def draw_growth():
    growth = {
        'Pine': {
            'age': [0, 15, 20, 25, 30, 35, 40, 45, 50, 200],
            'CAI': [0, 8.9, 20.4, 18.5, 21.8, 15.4, 16.1, 10.8, 10.9, 3.6]
        },
        'Oak': {
            'age': [1, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 200],
            'CAI': [0.0, 3.4, 4.6, 6.9, 6.5, 8.0, 6.6, 7.6, 5, 3.5, 3, 2.5, 2.5]
        },
        'spruce': {
            'age': [0, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 140],
            'CAI': [0.2, 6, 17.2, 19.2, 19.4, 19.4, 19.1, 18.6, 18.1, 17.4, 17, 16.4, 15.8, 15.2, 14.6, 14.4, 13.8, 13.2, 12.6, 12.1,
                    11.6,
                    11, 10.6, 8],
        }
    }
    plt.xlabel('Age')
    plt.ylabel('Current Annual Increment')

    colors = ['red', 'yellow', 'green', 'blue', 'purple']
    x = list(range(220))
    for i, (name, dic) in enumerate(growth.items()):
        draw(list(zip(*dic.values())), x, name, colors[i])

    plt.show()


def draw_relative():
    growth = {
        'Foliage': {
            'age': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'CAI': [1, .8, .5, .4, .35, .35, .4, .45, .5, .7, .8]
        },
        'Oak': {
            'age': [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'CAI': [1, .8, .7, .5, .45, .4, .4, .45, .5, .55, .55]
        },
        'spruce': {
            'age': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'CAI': [1, .9, .7, .5, .5, .55, .55, .55, .6, .65, .7],
        }
    }
    plt.xlabel('Age')
    plt.ylabel('Relative Growth')

    colors = ['green', 'blue', 'purple']
    x = list(range(110))
    for i, (name, dic) in enumerate(growth.items()):
        draw(list(zip(*dic.values())), x, name, colors[i])

    plt.show()


def draw_influence():
    plt.xlabel('Bio/BioMax')
    plt.ylabel('Influence Coefficient')

    bio = [0.00, 0.25, 0.50, 0.75, 1.00]
    dic = {
        'canopy': [1.000, 1.200, 0.900, 0.5, 0.000],
        'intermediate': [1.000, 1.0, 0.75, 0.5, 0.000],
        'understory': [1.000, 1.0, 0.75, 0.250, 0.000]
    }
    steps = 100
    x = list(map(lambda a: a / 100, range(steps)))
    colors = ['red', 'blue', 'yellow']
    for i, (name, factors) in enumerate(dic.items()):
        points = list(zip(bio, factors))
        draw(points, x, name, colors[i])

    plt.show()


def draw_manage():
    volume = [2, 15, 30]
    start = [0.1, 0.3, .5]
    impact = [8, 10, 12]

    plt.xlabel('Year')
    plt.ylabel('Management Mortality')
    colors = ['red', 'purple', 'yellow']
    for c, (v, s, m) in enumerate(zip(volume, start, impact)):
        x = list(range(max(impact) + 1))
        y = [max(s * (m - i), 0) / m for i in x]
        plt.plot(x, y, color=colors[c], linewidth=2, linestyle='-')
        plt.legend(loc='best')

    plt.show()


def draw_mortality():
    mortality = {
        'Teak': {
            'age': [0, 25, 100, 200],
            'mortality': [0.1, 0.1, 0.2, 0.7]
        },
        'Spruce': {
            'age': [0, 10, 20, 70, 120],
            'mortality': [.05, .4, .4, .15, .2]
        },
        'Understory': {
            'age': [0, 10, 20, 100, 200],
            'mortality': [0.020, 0.030, 0.020, 0.10, 0.9],
        },
        'Canopy': {
            'age': [0, 25, 100, 200],
            'mortality': [0.1, 0.2, 0.2, 1.00],
        }
    }
    plt.xlabel('Age')
    plt.ylabel('Mortality')

    colors = ['red', 'green', 'purple', 'orange']
    x = list(range(220))
    for i, (name, dic) in enumerate(mortality.items()):
        draw(list(zip(*dic.values())), x, name, colors[i])

    plt.show()


if __name__ == '__main__':
    draw_mortality()
