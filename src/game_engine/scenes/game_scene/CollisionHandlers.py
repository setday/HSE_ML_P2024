import random

from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle


def collision_car_with_car(arbiter, _, data):
    car1: Car = arbiter.shapes[0].super
    car2: Car = arbiter.shapes[1].super
    delta_score = 10 # (car1.car_model.body.velocity - car2.car_model.body.velocity).get_length_sqrd() / 30
    data["score"][0] -= delta_score

    if car1.car_model.body.velocity.get_length_sqrd() > 10:
        data["debris_emitter"](random.choice(arbiter.contact_point_set.points).point_a)

    health_decreation = delta_score
    car1.health -= health_decreation
    car2.health -= health_decreation
    return True


def collision_car_with_obstacle(arbiter, _, data):
    car = arbiter.shapes[0].super
    cone = arbiter.shapes[1].super
    if isinstance(cone, Car):
        car, cone = cone, car
    if isinstance(cone, StaticObstacle):
        delta_score = health_decreation = 10  # car.car_model.body.velocity.get_length_sqrd() / 50
        data["score"][0] -= delta_score
        data["debris_emitter"](arbiter.contact_point_set.points[0].point_a)
        car.health -= health_decreation
        return True
    delta_score = health_decreation = 5
    data["score"][0] -= delta_score
    cone.health -= health_decreation
    if cone.health <= 0:
        data["debris_emitter"](arbiter.contact_point_set.points[0].point_a)
        cone.remove()
    return True
