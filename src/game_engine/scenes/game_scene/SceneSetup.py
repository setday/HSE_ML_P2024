import json
import random

from pyglet.math import Vec2 as Vector2D  # type: ignore[import-untyped]

from src.game_engine.controllers import (
    KeyboardController,
    RandomController,
    AIController,
    BrakeController,
)
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.render.sprites import BasicSprite


def scene_v1_to_v2(scene_path):
    """
    Upgrade scene from version 1 to version 2
    """
    with open(scene_path) as file:
        scene_v1 = json.load(file)

    cars = []
    if "cars_positions" in scene_v1:
        for car in scene_v1["cars_positions"]:
            cars.append({"pos": car[:2], "ang": car[2], "mdl": "red_car"})
    if "main_car_pos" in scene_v1:
        cars.append(
            {
                "pos": scene_v1["main_car_pos"],
                "is_main_car": True,
            }
        )

    for car in cars:
        if "ang" in car and car["ang"] == 0:
            car.pop("ang")

    static_obstacles = []
    if "barriers_positions" in scene_v1:
        for obstacle in scene_v1["barriers_positions"]:
            static_obstacles.append(
                {"pos": obstacle[:2], "ang": obstacle[2], "mdl": "metal_pipe"}
            )
    if "big_barriers_positions" in scene_v1:
        for obstacle in scene_v1["big_barriers_positions"]:
            static_obstacles.append(
                {"pos": obstacle[:2], "ang": obstacle[2], "mdl": "big_bush"}
            )
    if "trees_positions" in scene_v1:
        for obstacle in scene_v1["trees_positions"]:
            static_obstacles.append({"pos": obstacle[:2], "mdl": "tree"})
    for obstacle in static_obstacles:
        if "ang" in obstacle and obstacle["ang"] == 0:
            obstacle.pop("ang")

    parking_places = []
    if "parking_positions" in scene_v1:
        for place in scene_v1["parking_positions"]:
            parking_places.append({"pos": place[:2], "ang": place[2]})
    for place in parking_places:
        if "ang" in place and place["ang"] == 0:
            place.pop("ang")

    movable_obstacles = []
    if "cones_positions" in scene_v1:
        for obstacle in scene_v1["cones_positions"]:
            movable_obstacles.append({"pos": obstacle, "mdl": "cone"})
    if "coins_positions" in scene_v1:
        for obstacle in scene_v1["coins_positions"]:
            movable_obstacles.append({"pos": obstacle, "mdl": "coin"})
    for obstacle in movable_obstacles:
        if "ang" in obstacle and obstacle["ang"] == 0:
            obstacle.pop("ang")

    scene_v2 = {
        "version": "2.0",
        "background": {
            "path": scene_v1["background"],
            "pos": (0, 0),
            "scl": scene_v1["scale"],
        },
    }
    if parking_places:
        scene_v2["parking_places"] = parking_places
    if movable_obstacles:
        scene_v2["movable_obstacles"] = movable_obstacles
    if cars:
        scene_v2["cars"] = cars
    if static_obstacles:
        scene_v2["static_obstacles"] = static_obstacles

    with open(scene_path[:-5] + "_v2.json", "w") as file:
        json.dump(scene_v2, file, indent=2)


def setup_scene_v2(scene, path, is_survive=False, random_remove=True):
    with open(path) as file:
        config = json.load(file)

    if "version" not in config and config["version"] != "2.0":
        raise ValueError(
            "Can't setup scene with not version 2.0 config with setup_scene_v2"
        )

    config.pop("version")

    bg = config["background"]
    scene.background = BasicSprite(bg["path"], bg["pos"], bg["scl"])
    scene.down_render_group.add(scene.background)

    config.pop("background")

    param_translator = {
        "pos": "position",
        "ang": "angle",
        "mdl": "car_model",
        "is_main_car": "is_main_car",
    }

    objs = []

    for model in config:
        model_type = model[:-1]
        for elem in config[model]:
            model_params = {"object_type": model_type}

            for key, value in elem.items():
                model_params[param_translator[key]] = value
            if "car_model" in model_params:
                model_params["movable_obstacle_model"] = model_params["car_model"]
                model_params["static_obstacle_model"] = model_params["car_model"]

            # Skip some models to make scene more interesting
            if (
                random_remove
                and model_type == "movable_obstacle"
                and random.random() < 0.5
            ):
                continue
            if (
                random_remove
                and model_type == "car"
                and not model_params.get("is_main_car", False)
                and random.random() < 0.1
            ):
                continue

            # Trees should be in top render group
            rg = scene.render_group
            if model_type == "tree":
                rg = scene.top_render_group
            if model_type == "parking_place":
                rg = scene.marking_group

            obj = ObjectFactory.create_object(
                render_group=rg, space=scene.space, **model_params
            )

            objs.append(obj)

            if model_type == "car":
                scene.cars.append(obj)

            if model_type == "parking_place":
                scene.parking_places.append(obj)

            if (
                model_type == "movable_obstacle"
                and model_params["movable_obstacle_model"] == "cone"
            ):
                scene.traffic_cones.append(obj)

    ai_controllers = [
        {"type": "sklearn", "path": "models_bin/CEM.pkl"},
        {"type": "pytorch", "path": "models_bin/torch.pt"},
        {"type": "stable_baselines", "policy": "DQN", "path": "models_bin/DQN"},
        {"type": "stable_baselines", "policy": "A2C", "path": "models_bin/A2C"},
        {"type": "stable_baselines", "policy": "PPO", "path": "models_bin/PPO"},
    ]

    # Special logic for cars
    for car in scene.cars:
        car.set_sound_multiplier_getter(scene.get_sound_multiplier)

        if car.is_main_car:
            scene.car_m = car
            scene.car_m.switch_controller(KeyboardController())
            scene.render_group.camera.snap_to_sprite(scene.car_m.car_view)
        else:
            car.switch_controller(
                AIController(ai_controllers[-1])
                if is_survive
                else random.choice(
                    [
                        RandomController(),
                        AIController(random.choice(ai_controllers)),
                        BrakeController(),
                    ]
                )
            )
            if is_survive:
                car.health = 1000

    for obj in objs:
        if hasattr(obj, "apply_friction"):
            obj.apply_friction()
        if hasattr(obj, "sync"):
            obj.sync()

    # To make at least one smart model
    if len(scene.cars) > 1:
        for car in scene.cars:
            if car.is_main_car:
                continue
            car.switch_controller(AIController(ai_controllers[-1]))
            break
