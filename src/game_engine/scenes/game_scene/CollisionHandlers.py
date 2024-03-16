import random

from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle


def collision_car_with_car(arbiter, _, data):
    car1: Car = arbiter.shapes[0].super
    car2: Car = arbiter.shapes[1].super

    delta_score = (car1.car_model.body.velocity - car2.car_model.body.velocity).get_length_sqrd() / 30
    data["score"][0] -= delta_score

    if car1.car_model.body.velocity.get_length_sqrd() > 10:
        data["debris_emitter"].add_burst(random.choice(arbiter.contact_point_set.points).point_a, [
            ":resources:images/pinball/pool_cue_ball.png",
            ":resources:images/space_shooter/meteorGrey_big2.png"
        ])

    health_decreation = delta_score
    car1.health -= health_decreation
    car2.health -= health_decreation

    return True


def collision_car_with_base_parking_place(arbiter, _, data):
    data["parking_place"].touching_cars.add(data["car"])
    return False


def end_collision_car_with_base_parking_place(arbiter, _, data):
    data["parking_place"].touching_cars.remove(data["car"])
    return False


def collision_car_with_dead_parking_place(arbiter, _, data):
    data["parking_place"].num_of_intersect_edges[data["car"]] += 1
    return False


def end_collision_car_with_dead_parking_place(arbiter, _, data):
    data["parking_place"].num_of_intersect_edges[data["car"]] -= 1
    return False


def ignore_collision_car_with_parking_place(arbiter, _, data):
    return False


def collision_car_with_obstacle(arbiter, _, data):
    car = arbiter.shapes[0].super
    cone = arbiter.shapes[1].super

    if isinstance(cone, Car):
        car, cone = cone, car

    if isinstance(cone, StaticObstacle):
        delta_score = health_decreation = car.car_model.body.velocity.get_length_sqrd() / 50

        data["score"][0] -= delta_score
        data["debris_emitter"].add_burst(random.choice(arbiter.contact_point_set.points).point_a, [
            ":resources:images/pinball/pool_cue_ball.png",
            ":resources:images/space_shooter/meteorGrey_big2.png"
        ])

        car.health -= health_decreation

        return True

    health_decreation = 33
    delta_score = 5
    data["score"][0] -= delta_score
    cone.health -= health_decreation

    if cone.health <= 0:
        data["debris_emitter"].add_burst(random.choice(arbiter.contact_point_set.points).point_a, [
            ":resources:images/pinball/pool_cue_ball.png",
            ":resources:images/space_shooter/meteorGrey_big2.png"
        ])

        cone.remove()

    return True
