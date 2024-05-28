import random

from pyglet.math import Vec2 as Vector2D

import src.game_engine.controllers.Controller as Controller
from assets.maps.EnvGeneration import ReadPositions
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.render.sprites.BasicSprite import BasicSprite


def SceneSetup(scene, path):
    config = ReadPositions(path)
    scene.background = BasicSprite(config["background"], Vector2D(0, 0))
    scene.background.update_scale(config["scale"])
    scene.down_render_group.add(scene.background)
    scene.traffic_cones = []
    scene.car_m = ObjectFactory.create_object(
        render_group=scene.render_group,
        space=scene.space,
        object_type="car",
        position=(random.randint(-500, 500), random.randint(-500, 500)) if scene.train else (0, -100),
        car_model="blue_car",
    )

    scene.car_m.switch_controller(Controller.KeyboardController())
    scene.render_group.camera.snap_to_sprite(scene.car_m.car_view)

    scene.cars = [scene.car_m]
    trees = [tuple(elem) for elem in config["trees_positions"]]
    for position in set(trees):
        ObjectFactory.create_object(
            scene.top_render_group,
            scene.space,
            object_type="static_obstacle",
            position=position,
            static_obstacle_model="tree",
        )
    cones = [tuple(elem) for elem in config["cones_positions"]]
    for position in set(random.choices(cones, k=random.randint(0, len(cones)))):
        scene.traffic_cones.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type="movable_obstacle",
                position=position,
                movable_obstacle_model="cone",
            )
        )
        scene.traffic_cones[-1].apply_friction()
        scene.traffic_cones[-1].sync()
    cars = random.choices(
        config["cars_positions"], k=random.randint(0, len(config["cars_positions"]))
    )
    for x, y, angle in set([tuple(car) for car in cars]):
        scene.cars.append(
            ObjectFactory.create_object(
                render_group=scene.render_group,
                space=scene.space,
                object_type="car",
                position=(x, y),
                car_model="red_car",
                angle=angle,
            )
        )

    for x, y, angle in config["barriers_positions"]:
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="static_obstacle",
            position=(x, y),
            angle=angle,
            static_obstacle_model="metal_pipe",
        )
    for x, y, angle in config["parking_positions"]:
        ParkingPlace(scene.down_render_group, scene.space, (x, y), angle=angle)
