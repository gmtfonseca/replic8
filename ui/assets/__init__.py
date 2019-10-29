from pathlib import Path

IMAGES_PATH = Path(__file__).parent / 'images/'


def image(name):
    return (IMAGES_PATH / name).as_posix()
