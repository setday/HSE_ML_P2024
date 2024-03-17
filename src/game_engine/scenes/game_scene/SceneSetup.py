from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import *


def SceneSetup(scene, cone_count=10, car_count=10, rotated_car_count=10):
    trees_positions, cones_positions, cars_positions, rotated_cars_positions, vert_barrier_positions, hor_barriers_positions = InitPositions()
    for position in trees_positions:
        ObjectFactory.create_object(
            scene.top_render_group,
            scene.space,
            object_type='static_obstacle',
            position=position,
            static_obstacle_model='tree'
        )
    for position in random.choices(cones_positions, k=cone_count):
        scene.traffic_cones.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type='movable_obstacle',
                position=position,
                movable_obstacle_model='cone'
            )
        )
    for position in random.choices(rotated_cars_positions, k=rotated_car_count):
        car = ObjectFactory.create_object(render_group=scene.render_group,
                                          space=scene.space,
                                          object_type='car',
                                          position=position,
                                          car_model='red_car',
                                          angle=random.choice([90, -90]))
        car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
        scene.cars.append(car)
    for position in random.choices(cars_positions, k=car_count):
        car = ObjectFactory.create_object(render_group=scene.render_group,
                                          space=scene.space,
                                          object_type='car',
                                          position=position,
                                          car_model='red_car')
        car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
        scene.cars.append(car)
    for position in vert_barrier_positions:
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type='static_obstacle',
            position=position,
            angle=90,
            static_obstacle_model='metal_pipe'
        )
    for position in hor_barriers_positions:
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type='static_obstacle',
            position=position,
            static_obstacle_model='rubbish_line'
        )

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
