from typing import Optional

from raytracer.core.types.entities import Primitive, Ray, Scene
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Canvas, Pixel

MAX_TOP = -1.0
MAX_BOTTOM = 1.0


class RenderEngine:
    def render(self, scene: Scene) -> Canvas:
        scene_width = scene.width
        scene_height = scene.height
        aspect_ratio = scene_width / scene_height
        scene_top = -1.0 / aspect_ratio
        scene_bottom = 1.0 / aspect_ratio

        # Due to aspect ratio we may not be working with a square.
        # Calculate the "step" for each iteration of the scene axis
        horizontal_step = (MAX_BOTTOM - MAX_TOP) / (scene_width - 1)
        vertical_step = (scene_bottom - scene_top) / (scene_height - 1)

        camera = scene.camera
        canvas = Canvas(width=scene_width, height=scene_height)

        for scene_y in range(scene_height):
            y = scene_top + scene_y * vertical_step
            for scene_x in range(scene_width):
                x = MAX_TOP + scene_x * horizontal_step
                ray = Ray(camera, Point(x=x, y=y, z=0) - camera)
                canvas.paint(
                    x=scene_x, y=scene_y, pixel=self._render(ray=ray, scene=scene)
                )
        return canvas

    def _render(self, ray: Ray, scene: Scene) -> Pixel:
        pixel = Pixel(r=0, g=0, b=0)
        distance, object = self._find_nearest(ray=ray, scene=scene)
        if object is None or distance is None:
            return pixel
        position = ray.origin + ray.direction * distance
        pixel += self._colour_at(object, position, scene)
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

    def _colour_at(self, obj_hit: Primitive, hit_pos: Point, scene: Scene) -> Pixel:
        return obj_hit.material
