import json
import random

from pyglet.math import Vec2 as Vector2D

from src.game_engine.controllers import (
    KeyboardController,
    RandomController,
    AIController,
    BrakeController,
)
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.render.sprites import BasicSprite


def setup_scene(scene, path, is_survive=False):
    with open(path) as file:
        config = json.load(file)
    scene.background = BasicSprite(config["background"], Vector2D(0, 0))
    scene.background.update_scale(config["scale"])
    scene.down_render_group.add(scene.background)
    scene.car_m = ObjectFactory.create_object(
        render_group=scene.render_group,
        space=scene.space,
        object_type="car",
        position=config.get("main_car_pos"),
        car_model="blue_car",
        is_main_car=True,
    )

    scene.car_m.switch_controller(KeyboardController())
    scene.render_group.camera.snap_to_sprite(scene.car_m.car_view)

    scene.cars = [scene.car_m]
    trees = [tuple(elem) for elem in config.get("trees_positions", [])]
    for position in set(trees):
        ObjectFactory.create_object(
            scene.top_render_group,
            scene.space,
            object_type="static_obstacle",
            position=position,
            static_obstacle_model="tree",
        )
    cones = [tuple(elem) for elem in config.get("cones_positions", [])]
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
    cars = config.get("cars_positions", [])
    cars = random.choices(cars, k=min(len(cars), 10))
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
    controllers = [
        {"type": "sklearn", "path": "models_bin/CEM.pkl"},
        {"type": "pytorch", "path": "models_bin/torch.pt"},
        {"type": "stable_baselines", "policy": "DQN", "path": "models_bin/DQN"},
        {"type": "stable_baselines", "policy": "A2C", "path": "models_bin/A2C"},
        {"type": "stable_baselines", "policy": "PPO", "path": "models_bin/PPO"},
    ]
    for car in scene.cars[1:]:
        car.switch_controller(
            AIController(controllers[-1])
            if is_survive
            else random.choice(
                [
                    RandomController(),
                    AIController(random.choice(controllers)),
                    BrakeController(),
                ]
            )
        )
        car.set_sound_multiplier_getter(scene.get_sound_multiplier)
        if is_survive:
            car.health = 1000
    # Чтобы была хотя бы одна умная модель
    if len(scene.cars) > 1:
        scene.cars[-1].switch_controller(AIController(controllers[-1]))
    for x, y, angle in config.get("barriers_positions", []):
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="static_obstacle",
            position=(x, y),
            angle=angle,
            static_obstacle_model="metal_pipe",
        )
    for x, y, angle in config.get("big_barriers_positions", []):
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="static_obstacle",
            position=(x, y),
            angle=angle,
            static_obstacle_model="big_bush",
        )
    for x, y, angle in config.get("parking_positions", []):
        scene.parking_place = ParkingPlace(
            scene.down_render_group, scene.space, (x, y), angle=angle
        )
    for _ in range(20):
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="movable_obstacle",
            position=scene.car_m.car_model.body.position
            + (random.randint(-200, 200), random.randint(-800, 800)),
            movable_obstacle_model="coin",
        )
