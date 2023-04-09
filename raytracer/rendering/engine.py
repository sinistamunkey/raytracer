from typing import Callable, Optional

from raytracer.core.types.entities import Primitive, Ray, Scene
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Canvas, Colour
from raytracer.rendering.constants import SCENE_ABSOLUTE_TOP
from raytracer.rendering.shading import Shader

# We need a small number when calculating reflection to ensure we get a different point
# otherwise we will likely end up reflecting off ourselves all the time.
REFLECTION_DELTA = 0.0001


class RenderEngine:
    def __init__(self, shader: Shader, max_depth: int = 6) -> None:
        self.shader = shader
        self.max_depth = max_depth

    def render(
        self, scene: Scene, update_func: Optional[Callable[[int], None]] = None
    ) -> Canvas:
        scene_width = scene.width
        scene_height = scene.height
        scene_top, _ = scene.get_aspect_boundries()
        horizontal_step, vertical_step = scene.get_horizontal_and_vertical_steps()

        camera = scene.camera
        canvas = Canvas(width=scene_width, height=scene_height)

        for scene_y in range(scene_height):
            y = scene_top + scene_y * vertical_step
            for scene_x in range(scene_width):
                x = SCENE_ABSOLUTE_TOP + scene_x * horizontal_step
                ray = Ray(camera, Point(x=x, y=y, z=0) - camera)
                canvas.paint(
                    x=scene_x, y=scene_y, pixel=self._render_pixel(ray=ray, scene=scene)
                )
                if update_func is not None:
                    update_func(1)
        return canvas

    def _render_pixel(self, ray: Ray, scene: Scene, depth: int = 0) -> Colour:
        pixel = Colour(r=0, g=0, b=0)
        distance, object = self._find_nearest(ray=ray, scene=scene)
        if object is None or distance is None:
            # The ray isn't hitting at any object that needs rendering.
            # Return black (nothing)
            return pixel
        position = ray.origin + ray.direction * distance
        normal = object.normal(position)
        pixel += self.shader.shade(scene=scene, obj_hit=object, hit_pos=position)
        if depth <= self.max_depth:
            # Calculate reflections
            ray_position = position + normal * REFLECTION_DELTA
            ray_direction = (
                ray.direction - 2 * ray.direction.dot_product(normal) * normal
            )
            reflection = Ray(origin=ray_position, direction=ray_direction)
            pixel += (
                self._render_pixel(ray=reflection, scene=scene, depth=depth + 1)
                * object.material.reflection
            )
        return pixel

    def _find_nearest(
        self, ray: Ray, scene: Scene
    ) -> tuple[Optional[float], Optional[Primitive]]:
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return dist_min, obj_hit
