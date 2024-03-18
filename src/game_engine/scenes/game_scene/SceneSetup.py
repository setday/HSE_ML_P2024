import random

from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import *
from src.game_engine.scenes.game_scene.EnvGeneration import ReadPositions


def SceneSetup(scene):
    trees_positions, cones_positions, cars_positions, \
        rotated_cars_positions, vert_barrier_positions, hor_barriers_positions = ReadPositions()
    for position in set(trees_positions):
        ObjectFactory.create_object(
            scene.top_render_group,
            scene.space,
            object_type='static_obstacle',
            position=position,
            static_obstacle_model='tree'
        )
    for position in set(random.choices(cones_positions, k=random.randint(10, 40))):
        scene.traffic_cones.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type='movable_obstacle',
                position=position,
                movable_obstacle_model='cone'
            )
        )
    for position in set(random.choices(rotated_cars_positions, k=random.randint(5, 10))):
        car = ObjectFactory.create_object(render_group=scene.render_group,
                                          space=scene.space,
                                          object_type='car',
                                          position=position,
                                          car_model='red_car',
                                          angle=random.choice([90, -90]))
        car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
        scene.cars.append(car)
    for position in set(random.choices(cars_positions, k=random.randint(5, 10))):
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
