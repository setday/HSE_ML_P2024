from src.game_engine.Core import Core
from src.game_engine.entities.Car import Car
from src.game_engine.controllers.Controller import KeyboardController
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.render.screen_elements.Indicator import Indicator
from src.render.screen_elements.ScoreDisplay import ScoreDisplay


def test_core():
    core = Core()
    assert hasattr(core, "scene"), "Game must have scene"
    assert hasattr(core, "window"), "Game must have window"


def test_main_car():
    core = Core()
    assert hasattr(core.scene, "car_m"), "Game must have main character"
    assert isinstance(core.scene.car_m, Car), "Main character must be a car"
    assert hasattr(core.scene.car_m, "health"), "Main car must have a health"
    assert (
        core.scene.car_m.health == 100
    ), "Main character's health must be equal 100 in the begin"
    assert hasattr(core.scene.car_m, "controller"), "Main car must have a controller"
    assert isinstance(
        core.scene.car_m.controller, KeyboardController
    ), "Controller must be keyboard"


def test_object_factory():
    core = Core()
    car = ObjectFactory.create_object(
        render_group=core.scene.render_group,
        space=core.scene.space,
        object_type="car",
        position=(0, -100),
        car_model="blue_car",
    )
    assert isinstance(car, Car), "Object factory must return car"
    assert hasattr(car, "health"), "Car must have health"
    assert car.health >= 0, "Health must be non-negative"
    assert hasattr(car, "car_model"), "Car must have physics model"
    assert (
        car.car_model.body in core.scene.space.bodies
    ), "Car must be added to the physics scene"
    assert hasattr(car, "car_view"), "Car must have view"
    # assert car.car_view in core.scene.render_group, 'Car must be added to the game scene'
    cone = ObjectFactory.create_object(
        render_group=core.scene.render_group,
        space=core.scene.space,
        object_type="movable_obstacle",
        position=(70, -170),
        movable_obstacle_model="cone",
    )
    assert isinstance(
        cone, MovableObstacle
    ), "Object factory must return movable obstacle"
    assert hasattr(cone, "health"), "Cone must have health"
    assert cone.health >= 0, "Health must be non-negative"
    assert hasattr(cone, "obstacle_model"), "Cone must have physics model"
    assert (
        cone.obstacle_model.body in core.scene.space.bodies
    ), "Cone must be added to the physics scene"
    assert hasattr(cone, "obstacle_view"), "Cone must have view"
    # assert cone.obstacle_view in core.scene.render_group, 'Cone must be added to the game scene'
    for model in ["tree", "rubbish_line", "metal_pipe", "x_barrier", "y_barrier"]:
        obj = ObjectFactory.create_object(
            core.scene.top_render_group,
            core.scene.space,
            "static_obstacle",
            (70, -10),
            static_obstacle_model=model,
        )
        assert isinstance(
            obj, StaticObstacle
        ), "Object factory must return static obstacle"
        assert not hasattr(obj, "health"), f"{model} must not have health"
        assert hasattr(obj, "obstacle_model"), f"{model} must have physics model"
        assert (
            obj.obstacle_model.body in core.scene.space.bodies
        ), f"{model} must be added to the physics scene"
        assert hasattr(obj, "obstacle_view"), f"{model} must have view"
        if model == "x_barrier" or model == "y_barrier":
            assert obj.obstacle_view is None, f"{model} view must be None"


def test_scene_setup():
    core = Core()
    assert hasattr(core.scene, "cars"), "Game must have at least one car"
    for car in core.scene.cars:
        assert isinstance(car, Car), "Only cars should be in list with cars"
    assert hasattr(core.scene, "traffic_cones"), "GameScene must have list with cones"
    for cone in core.scene.traffic_cones:
        assert isinstance(
            cone, MovableObstacle
        ), "Only cones should be in list with cones"
    assert hasattr(core.scene, "indicator")
    assert isinstance(core.scene.indicator, Indicator)
    assert core.scene.indicator.owner is core.scene.car_m
    assert core.scene.indicator.target_health == 2 * core.scene.car_m.health
    # это нормально с точки зрения логики?
    assert hasattr(core.scene, "score_board")
    assert isinstance(core.scene.score_board, ScoreDisplay)
    assert core.scene.score_board.target_score == core.scene.score[0]
