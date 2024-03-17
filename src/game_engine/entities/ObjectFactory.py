from pyglet.math import Vec2 as Vector2D
from pymunk import Space

from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.render.RenderGroup import RenderGroup


class ObjectFactory:
    @staticmethod
    def create_object(render_group: RenderGroup,
                      space: Space,
                      object_type: str = 'car',
                      position: Vector2D = (0, 0),
                      angle: float = 0,
                      **kwargs) -> Car | MovableObstacle | StaticObstacle:
        if object_type == 'car':
            return ObjectFactory.create_car(render_group, space, position, angle, kwargs.get('car_model', 'blue_car'))
        elif object_type == 'movable_obstacle':
            return ObjectFactory.create_movable_obstacle(render_group, space, position, angle,
                                                         kwargs.get('movable_obstacle_model', 'cone'))
        elif object_type == 'static_obstacle':
            return ObjectFactory.create_static_obstacle(render_group, space, position, angle,
                                                        kwargs.get('static_obstacle_model', 'tree'))
        else:
            raise ValueError(f"Invalid object type: {object_type}")

    @staticmethod
    def create_car(render_group: RenderGroup,
                   space: Space,
                   position: Vector2D = (0, 0),
                   angle: float = 0,
                   car_model: str = 'blue_car') -> Car:
        car_model_dict = {
            'random_car': -1,
            'blue_car': 0,
            'red_car': 1,
            'long_car': 2,
        }
        return Car(render_group, space, position, angle, car_model_dict[car_model])

    @staticmethod
    def create_movable_obstacle(render_group: RenderGroup,
                                space: Space,
                                position: Vector2D = (0, 0),
                                angle: float = 0,
                                movable_obstacle_model: str = 'cone') -> MovableObstacle:
        movable_obstacle_model_dict = {
            'cone': 'assets/pic/obstacles/Traffic_Cone.png',
        }
        return MovableObstacle(render_group, space, position, angle,
                               movable_obstacle_model_dict[movable_obstacle_model])

    @staticmethod
    def create_static_obstacle(render_group: RenderGroup,
                               space: Space,
                               position: Vector2D = (0, 0),
                               angle: float = 0,
                               static_obstacle_model: str = 'bush') -> StaticObstacle:
        static_obstacle_model_dict = {
            'bush': 'assets/pic/obstacles/Bush.png',
            'metal_pipe': 'assets/pic/obstacles/parking_barrier_1.png',
            'rubbish_line': 'assets/pic/obstacles/parking_barrier_2.png',
            'tree': 'assets/pic/obstacles/Tree_1.png',
            'x_barrier': None,
            'y_barrier': None,
        }
        shape_type = static_obstacle_model if (
                static_obstacle_model == 'x_barrier' or static_obstacle_model == 'y_barrier'
        ) else 'circle'
        return StaticObstacle(render_group, space, position, angle,
                              static_obstacle_model_dict[static_obstacle_model], shape_type)
