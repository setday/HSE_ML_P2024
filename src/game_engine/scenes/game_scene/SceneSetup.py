import random

from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import *
from src.game_engine.scenes.game_scene.EnvGeneration import ReadPositions
from src.game_engine.entities.ParkingPlace import ParkingPlace

def TightSceneSetup(scene):
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


def WideSceneSetup(scene):
    for i in range(-5, 5):
        scene.traffic_cones.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type='movable_obstacle',
                position=(70 * i, -170),
                movable_obstacle_model='cone'
            )
        )

    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * -5 - 35, -70),
        movable_obstacle_model='cone'
    ))
    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * -5 - 40, -100),
        movable_obstacle_model='cone'
    ))
    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * -5 - 35, -130),
        movable_obstacle_model='cone'
    ))

    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * 4 + 35, -70),
        movable_obstacle_model='cone'
    ))
    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * 4 + 40, -100),
        movable_obstacle_model='cone'
    ))
    scene.traffic_cones.append(ObjectFactory.create_object(
        scene.render_group, scene.space, 'movable_obstacle', (70 * 4 + 35, -130),
        movable_obstacle_model='cone'
    ))

    for i in range(-5, 5):
        ObjectFactory.create_object(
            scene.top_render_group, scene.space, 'static_obstacle', (70 * i, -10),
            static_obstacle_model='tree'
        )

    ###
    # Parking lots
    ###

    for i in range(-5, 5):
        ParkingPlace(scene.down_render_group, scene.space, (70 * i, -100))
    for i in range(-5, 4):
        ObjectFactory.create_object(
            scene.render_group, scene.space, 'static_obstacle', (70 * i + 35, -100), 90,
            static_obstacle_model='metal_pipe'
        )
    for i in range(-5, 5):
        ObjectFactory.create_object(
            scene.render_group, scene.space, 'static_obstacle', (70 * i, -45),
            static_obstacle_model='rubbish_line'
        )

    ###
    # Barriers
    ###

    ObjectFactory.create_object(
        scene.render_group, scene.space, 'static_obstacle', (0, 1000),
        static_obstacle_model='x_barrier'
    )
    ObjectFactory.create_object(
        scene.render_group, scene.space, 'static_obstacle', (0, -2000),
        static_obstacle_model='x_barrier'
    )
    ObjectFactory.create_object(
        scene.render_group, scene.space, 'static_obstacle', (3500, 0),
        static_obstacle_model='y_barrier'
    )
    ObjectFactory.create_object(
        scene.render_group, scene.space, 'static_obstacle', (-3500, 0),
        static_obstacle_model='y_barrier'
    )

    ParkingPlace(scene.down_render_group, scene.space, (0, -300), angle=0.4)
