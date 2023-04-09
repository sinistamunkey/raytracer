# Raytracer

Making a raytracer in Python because... reasons.

Following: https://www.youtube.com/playlist?list=PL8ENypDVcs3H-TxOXOzwDyCm5f2fGXlIS

## Getting started

You will need to install [Poetry](https://python-poetry.org/).

### MacOS/ Linux

```shell
cd raytracer
poetry install
```

### Windows
```powershell
cd raytracer
py -m poetry install
```

## Running rendering commands

At present this only supports rendering a single sphere to a canvas using the PPM format.

### MacOS/ Linux
```shell
poetry run raytracer rendering render-scene
```

### Windows
```powershell
py -m poetry run raytracer rendering render-scene
```

The above command will create a new file in the `out` directory.  You can specify scenes defined in the `scenes` directory.

![scene_1](scene_1.jpeg)