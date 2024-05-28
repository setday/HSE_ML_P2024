import random

import pymunk

from src.game_engine.entities.Car import Car
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle


def skip_collision(___, _, __) -> bool:
    return False


def collision_car_with_car(arbiter: pymunk.Arbiter, _, data: dict) -> bool:
    car1: Car = arbiter.shapes[0].super
    car2: Car = arbiter.shapes[1].super

    delta_score: float = (
        car1.car_model.body.velocity - car2.car_model.body.velocity
    ).get_length_sqrd() / 30
    data["score"][0] -= delta_score

    if car1.car_model.body.velocity.get_length_sqrd() > 10:
        data["debris_emitter"].add_burst(
            random.choice(arbiter.contact_point_set.points).point_a,
            [
                ":resources:images/pinball/pool_cue_ball.png",
                ":resources:images/space_shooter/meteorGrey_big2.png",
            ],
        )

    health_decreation: float = delta_score
    car1.change_health(-health_decreation)
    car2.change_health(-health_decreation)

    return True


def collision_car_with_base_parking_place(arbiter: pymunk.Arbiter, _, __) -> bool:
    car: Car | ParkingPlace = arbiter.shapes[0].super
    parking_place: ParkingPlace | Car = arbiter.shapes[1].super

    if isinstance(parking_place, Car):
        car, parking_place = parking_place, car

    car.inside_parking_place += 1
    return False


def end_collision_car_with_base_parking_place(arbiter: pymunk.Arbiter, _, __) -> bool:
    car: Car | ParkingPlace = arbiter.shapes[0].super
    parking_place: Car | ParkingPlace = arbiter.shapes[1].super

    if isinstance(parking_place, Car):
        car, parking_place = parking_place, car

    car.inside_parking_place -= 1
    return False


def collision_car_with_dead_parking_place(arbiter: pymunk.Arbiter, _, __) -> bool:
    car: Car | ParkingPlace = arbiter.shapes[0].super
    parking_place: Car | ParkingPlace = arbiter.shapes[1].super

    if isinstance(parking_place, Car):
        car, parking_place = parking_place, car

    car.dead_zones_intersect += 1
    return False


def end_collision_car_with_dead_parking_place(arbiter: pymunk.Arbiter, _, __) -> bool:
    car: Car | ParkingPlace = arbiter.shapes[0].super
    parking_place: Car | ParkingPlace = arbiter.shapes[1].super

    if isinstance(parking_place, Car):
        car, parking_place = parking_place, car

    car.dead_zones_intersect -= 1
    return False


def collision_car_with_obstacle(arbiter: pymunk.Arbiter, _, data: dict) -> None:
    car = arbiter.shapes[0].super
    cone = arbiter.shapes[1].super

    if isinstance(cone, Car):
        car, cone = cone, car

    if isinstance(cone, StaticObstacle):
        delta_score = health_decreation = (
            car.car_model.body.velocity.get_length_sqrd() / 50
        )

        data["score"][0] -= delta_score
        data["debris_emitter"].add_burst(
            random.choice(arbiter.contact_point_set.points).point_a,
            [
                ":resources:images/pinball/pool_cue_ball.png",
                ":resources:images/space_shooter/meteorGrey_big2.png",
            ],
        )

        car.change_health(-health_decreation)

        return True

    health_decreation: int = 33
    delta_score: int = 5
    data["score"][0] -= delta_score
    cone.health -= health_decreation

    if cone.health <= 0:
        data["debris_emitter"].add_burst(
            random.choice(arbiter.contact_point_set.points).point_a,
            [
                ":resources:images/pinball/pool_cue_ball.png",
                ":resources:images/space_shooter/meteorGrey_big2.png",
            ],
        )

        cone.remove()

    return True
