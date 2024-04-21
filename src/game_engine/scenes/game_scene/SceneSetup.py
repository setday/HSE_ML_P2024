import random
from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import *
from src.game_engine.scenes.game_scene.EnvGeneration import ReadPositions
from src.game_engine.entities.ParkingPlace import ParkingPlace


def SceneSetup(scene, path):
    positions = ReadPositions(path)
    for position in set([tuple(elem) for elem in positions['trees_positions']]):
        ObjectFactory.create_object(
            scene.top_render_group,
            scene.space,
            object_type='static_obstacle',
            position=position,
            static_obstacle_model='tree'
        )
    for position in set([tuple(elem) for elem in random.choices(positions['cones_positions'], k=random.randint(0, len(positions['cones_positions'])))]):
        scene.traffic_cones.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type='movable_obstacle',
                position=position,
                movable_obstacle_model='cone'
            )
        )
    for (x, y, angle) in set([tuple(elem) for elem in random.choices(positions['cars_positions'], k=random.randint(0, len(positions['cars_positions'])))]):
        car = ObjectFactory.create_object(render_group=scene.render_group,
                                          space=scene.space,
                                          object_type='car',
                                          position=(x, y),
                                          car_model='red_car',
                                          angle=angle)
        car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
        scene.cars.append(car)
    for (x, y, angle) in positions['barriers_positions']:
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type='static_obstacle',
            position=(x, y),
            angle=angle,
            static_obstacle_model='metal_pipe'
        )
    for (x, y, angle) in positions['parking_positions']:
        ParkingPlace(
            scene.down_render_group,
            scene.space,
            (x, y),
            angle=angle
        )
