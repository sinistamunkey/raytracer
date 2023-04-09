from raytracer.core.types.entities import BaseMaterial, Light, Primitive, Ray, Scene
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour

PHONG_COEFFICENT = 50


class Shader:
    def shade(self, scene: Scene, obj_hit: Primitive, hit_pos: Point) -> Colour:
        """
        Returns a colour calculated on the light sources interacting with object.

        Runs diffusion and phong shading.
        """
        material = obj_hit.material
        normal = obj_hit.normal(hit_pos)
        colour = material.ambient * Colour.from_hex("#000000")
        to_cam = scene.camera - hit_pos
        for light in scene.lights:
            colour += self._diffuse(
                light=light,
                material=material,
                hit_pos=hit_pos,
                normal=normal,
            )
            colour += self._specular(
                light=light,
                material=material,
                normal=normal,
                hit_pos=hit_pos,
                to_cam=to_cam,
            )
        return colour

    def _diffuse(
        self,
        light: Light,
        material: BaseMaterial,
        hit_pos: Point,
        normal: Point,
    ) -> Colour:
        """
        Handles diffuse shading for non-shiny surfaces

        Uses lambert shading
        """
        to_light = Ray(origin=hit_pos, direction=light.position - hit_pos)
        colour = (
            material.colour_at(hit_pos)
            * material.diffuse
            * max(normal.dot_product(to_light.direction), 0)
        )
        return colour

    def _specular(
        self,
        light: Light,
        material: BaseMaterial,
        normal: Point,
        hit_pos: Point,
        to_cam: Point,
    ) -> Colour:
        """
        Handles specular shading for shiny surfaces

        Uses Blinn-Phong shading
        """
        to_light = Ray(origin=hit_pos, direction=light.position - hit_pos)
        half_vector = (to_light.direction + to_cam).normalize()
        return (
            light.colour
            * material.specular
            * max(normal.dot_product(half_vector), 0) ** PHONG_COEFFICENT
        )
