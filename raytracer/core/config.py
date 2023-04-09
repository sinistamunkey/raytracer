import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "out")
SCENE_DIR = os.path.join(BASE_DIR, "scenes")
MAX_REFLECTION_DEPTH = 6
