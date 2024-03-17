from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.Car import Car
import random
from src.game_engine.controllers.Controller import *


def SceneSetup(scene, cone_count=10, car_count=10, rotated_car_count=10):
    trees_positions, cones_positions, cars_positions, rotated_cars_positions = InitPositions()
    for position in trees_positions:
        StaticObstacle(scene.top_render_group, scene.space, position)
    for position in random.choices(cones_positions, k=cone_count):
        scene.traffic_cones.append(MovableObstacle(scene.render_group, scene.space, position))
    for position in random.choices(rotated_cars_positions, k=rotated_car_count):
        car = Car(scene.render_group, scene.space, position, 1, True)
        car.switch_controller(random.choice([AIController(), BrakeController()]))
        scene.cars.append(car)
    for position in random.choices(cars_positions, k=car_count):
        car = Car(scene.render_group, scene.space, position, 1)
        car.switch_controller(random.choice([AIController(), BrakeController()]))
        scene.cars.append(car)


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

    cones_positions = []
    rotated_cars_positions = []
    cars_positions = []
    for x in range(-440, 721, 70):
        trees_positions.append((x, 485))
    for x in range(-264, 700, 63):
        cars_positions.append((x, 390))
        cars_positions.append((x, 590))
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
    return trees_positions, cones_positions, cars_positions, rotated_cars_positions
