import src.game_engine.controllers.Controller as Controller
from pyglet.math import Vec2 as Vector2D
from src.game_engine.entities.ObjectFactory import ObjectFactory
from assets.maps.EnvGeneration import ReadPositions
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.render.sprites.BasicSprite import BasicSprite
import random


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
        position=(0, -100),
        car_model="blue_car",
    )

    scene.car_m.switch_controller(Controller.KeyboardController())
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
    cars = random.choices(
        config.get("cars_positions", []), k=10
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
    controllers = [
        {"type": "sklearn", "path": "models_bin/CEM.pkl"},
        {"type": "pytorch", "path": "models_bin/torch.pt"},
        {"type": "stable_baselines", "policy": "DQN", "path": "models_bin/DQN"},
        {"type": "stable_baselines", "policy": "A2C", "path": "models_bin/A2C"},
        {"type": "stable_baselines", "policy": "PPO", "path": "models_bin/PPO"},
    ]
    for car in scene.cars[1:]:
        car.switch_controller(
            Controller.AIController(controllers[-1]) if scene.mode == "survive"
            else random.choice(
                [
                    Controller.RandomController(),
                    Controller.AIController(random.choice(controllers)),
                    Controller.BrakeController(),
                ]
            )
        )
        if scene.mode == "survive":
            car.health = 1000
    for x, y, angle in config.get("barriers_positions", []):
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="static_obstacle",
            position=(x, y),
            angle=angle,
            static_obstacle_model="metal_pipe",
        )
    for x, y, angle in config.get("parking_positions", []):
        ParkingPlace(scene.down_render_group, scene.space, (x, y), angle=angle)
    for _ in range(20):
        ObjectFactory.create_object(
            render_group=scene.render_group,
            space=scene.space,
            object_type="movable_obstacle",
            position=(random.randint(-1000, 1000), random.randint(-1000, 1000)),
            movable_obstacle_model="coin",
        )
