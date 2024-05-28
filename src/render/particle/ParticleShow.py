from typing import Tuple, List

import arcade


particles_on = True


class ParticleShow:
    def __init__(self) -> None:
        self.emitters: list = []

    def update(self) -> None:
        if not particles_on:
            for emitter in self.emitters:
                emitter.kill()
              
        for emitter in self.emitters:
            emitter.update()
        while len(self.emitters) > 0 and self.emitters[0].get_count() == 0:
            self.emitters.pop(0)

    def draw(self) -> None:
        if not particles_on:
            return
          
        for emitter in self.emitters:
            emitter.draw()

    def add_burst(
        self, center_xy: Tuple[int, int], textures: List[str]
    ) -> arcade.Emitter | None:
        if not particles_on:
            return None
        x, y = center_xy

        emitter = arcade.make_burst_emitter(
            center_xy=(x, -y),
            filenames_and_textures=textures,
            particle_count=5,
            particle_speed=0.3,
            particle_lifetime_min=0.75,
            particle_lifetime_max=1.25,
            particle_scale=0.13,
            fade_particles=True,
        )

        self.emitters.append(emitter)

        return emitter
