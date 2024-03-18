

def InitPositions():
    trees_positions = [
        (30, 100),
        (100, 100),
        (-40, 100),
        (-300, 100),
        (-370, 100),
        (-440, 100),
        (370, 100),
        (440, 100),
        (510, 100),
        (370, 30),
        (440, 30),
        (510, 30),
        (510, -40),
        (30, -1060),
        (100, -1060),
        (-40, -1060),
        (-300, -1060),
        (-370, -1060),
        (-440, -1060),
    ]
    vert_barries_positions = []
    hor_barriers_positions = []
    cones_positions = []
    rotated_cars_positions = []
    cars_positions = []
    for x in range(-440, 721, 70):
        trees_positions.append((x, 485))
        trees_positions.append((x, 1000))
    for x in range(-264, 700, 63):
        cars_positions.append((x, 390))
        cars_positions.append((x, 590))
        cars_positions.append((x, 900))
        cars_positions.append((x, 960))
    for x in range(-300, 700, 63):
        vert_barries_positions.append((x, 410))
        vert_barries_positions.append((x, 360))
        vert_barries_positions.append((x, 560))
        vert_barries_positions.append((x, 610))
        vert_barries_positions.append((x, 910))
        vert_barries_positions.append((x, 860))
        vert_barries_positions.append((x, 1060))
        vert_barries_positions.append((x, 1110))
    for y in range(-233, 485, 64):
        cones_positions.append((-667, y))
    for y in range(-350, -800, -128):
        cones_positions.append((-667, y))
    for y in range(-919, 27, 63):
        rotated_cars_positions.append((-300, y))
        cones_positions.append((-240, y))
        rotated_cars_positions.append((-10, y))
        cones_positions.append((190, y))
        rotated_cars_positions.append((80, y))
        rotated_cars_positions.append((-440, y))
        rotated_cars_positions.append((380, y))
    rotated_cars_positions.remove((380, 26))
    for y in range(-1000, 100, 50):
        vert_barries_positions.append((-371, y))
        vert_barries_positions.append((38, y))
        vert_barries_positions.append((446, y))
    for y in range(-1010, 100, 63):
        hor_barriers_positions.append((-710, y))
        hor_barriers_positions.append((-660, y))
        hor_barriers_positions.append((-450, y))
        hor_barriers_positions.append((-400, y))
        hor_barriers_positions.append((-350, y))
        hor_barriers_positions.append((-300, y))
        hor_barriers_positions.append((15, y))
        hor_barriers_positions.append((-35, y))
        hor_barriers_positions.append((65, y))
        hor_barriers_positions.append((115, y))
        hor_barriers_positions.append((375, y))
        hor_barriers_positions.append((425, y))
        hor_barriers_positions.append((475, y))
        hor_barriers_positions.append((525, y))
    return trees_positions, cones_positions, cars_positions, rotated_cars_positions, vert_barries_positions, hor_barriers_positions


def WritePositions():
    for array in InitPositions():
        for position in array:
            print(position, end=';')
        print()


def ReadPositions():
    with open('assets/env.txt') as env:
        arrays = [[tuple(map(int, position[1:-1].split(', '))) for position in array.split(";") if position[1:-1] != ''] \
                  for array in env.readlines()]
    return arrays[0], arrays[1], arrays[2], arrays[3], arrays[4], arrays[5]


if __name__ == "__main__":
    WritePositions()
