import tempfile
from typing import Iterator

import pytest


@pytest.fixture
def temp_directory() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def scene_data() -> dict:
    return {
        "camera": {"x": 0, "y": -0.35, "z": -1},
        "objects": [
            {
                "type": "Sphere",
                "attributes": {
                    "name": "Blue ball",
                    "centre": {"x": 0.75, "y": -0.1, "z": 1},
                    "radius": 0.6,
                    "material": {
                        "type": "Material",
                        "attributes": {
                            "colour": "#0000FF",
                            "ambient": 0.05,
                            "diffuse": 1.0,
                            "specular": 1.0,
                            "reflection": 0.6,
                        },
                    },
                },
            }
        ],
        "lights": [
            {"position": {"x": 1.5, "y": -0.5, "z": -10.0}, "colour": "#FFFFFF"}
        ],
    }
