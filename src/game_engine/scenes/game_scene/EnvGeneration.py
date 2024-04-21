import json
import random
def Map1InitPositions():
    d = {
        'trees_positions': [],
        'cones_positions': [],
        'cars_positions': [],
        'barriers_positions': [],
        'parking_positions': [(0, -300, 0.4)]
    }
    with open('../../../../assets/json/OnlyPark.json', 'w') as file:
        json.dump(d, file)
    for i in range(-5, 4):
        d['barriers_positions'].append((70 * i + 35, -100, 90))
    for i in range(-5, 5):
        d['barriers_positions'].append((70 * i, -45, 0))
    with open('../../../../assets/json/ParkWithBarriers.json', 'w') as file:
        json.dump(d, file)
    for i in range(-5, 5):
        d['cones_positions'].append((70 * i, -170))
    d['cones_positions'].append((70 * -5 - 35, -70))
    d['cones_positions'].append((70 * -5 - 40, -100))
    d['cones_positions'].append((70 * -5 - 35, -130))
    d['cones_positions'].append((70 * 4 + 35, -70))
    d['cones_positions'].append((70 * 4 + 40, -100))
    d['cones_positions'].append((70 * 4 + 35, -130))
    for i in range(-5, 5):
        d['trees_positions'].append((70 * i, -10))
    with open('../../../../assets/json/ParkWithObstacles.json', 'w') as file:
        json.dump(d, file)
    for i in range(-5, 5):
        if i == 0:
            continue
        d['cars_positions'].append(((70 * i, -100, 90)))
    for i in range(-5, 5):
        d['parking_positions'].append((70 * i, -100, 0))
    with open('../../../../assets/json/ParkWithEnemies.json', 'w') as file:
        json.dump(d, file)

def Map2InitPositions():
    d = {'trees_positions': [
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
    ], 'cones_positions': [], 'cars_positions': [], 'barriers_positions': [], 'parking_positions': []}
    for x in range(-440, 721, 70):
        d['trees_positions'].append((x, 485))
        d['trees_positions'].append((x, 1000))
    for x in range(-264, 700, 63):
        d['cars_positions'].append((x, 390, 0))
        d['cars_positions'].append((x, 590, 0))
        d['cars_positions'].append((x, 900, 0))
        d['cars_positions'].append((x, 960, 0))
    for x in range(-300, 700, 63):
        d['barriers_positions'].append((x, 410, 90))
        d['barriers_positions'].append((x, 360, 90))
        d['barriers_positions'].append((x, 560, 90))
        d['barriers_positions'].append((x, 610, 90))
        d['barriers_positions'].append((x, 910, 90))
        d['barriers_positions'].append((x, 860, 90))
        d['barriers_positions'].append((x, 1060, 90))
        d['barriers_positions'].append((x, 1110, 90))
    for y in range(-233, 485, 64):
        d['cones_positions'].append((-667, y))
    for y in range(-350, -800, -128):
        d['cones_positions'].append((-667, y))
    for y in range(-919, 27, 63):
        d['cars_positions'].append((-300, y, random.choice([90, -90])))
        d['cones_positions'].append((-240, y))
        d['cars_positions'].append((-10, y, random.choice([90, -90])))
        d['cones_positions'].append((190, y))
        d['cars_positions'].append((80, y, random.choice([90, -90])))
        d['cars_positions'].append((-440, y, random.choice([90, -90])))
        d['cars_positions'].append((380, y, random.choice([90, -90])))
        for y in range(-1000, 100, 50):
            d['barriers_positions'].append((-371, y, 90))
            d['barriers_positions'].append((38, y, 90))
            d['barriers_positions'].append((446, y, 90))
    for y in range(-1010, 100, 63):
        d['barriers_positions'].append((-710, y, 0))
        d['barriers_positions'].append((-660, y, 0))
        d['barriers_positions'].append((-450, y, 0))
        d['barriers_positions'].append((-400, y, 0))
        d['barriers_positions'].append((-350, y, 0))
        d['barriers_positions'].append((-300, y, 0))
        d['barriers_positions'].append((15, y, 0))
        d['barriers_positions'].append((-35, y, 0))
        d['barriers_positions'].append((65, y, 0))
        d['barriers_positions'].append((115, y, 0))
        d['barriers_positions'].append((375, y, 0))
        d['barriers_positions'].append((425, y, 0))
        d['barriers_positions'].append((475, y, 0))
        d['barriers_positions'].append((525, y, 0))
    with open('../../../../assets/json/TestMap.json', 'w') as file:
        json.dump(d, file)



def ReadPositions(path):
    with open(path) as file:
        return json.load(file)


if __name__ == "__main__":
    Map1InitPositions()
    Map2InitPositions()
