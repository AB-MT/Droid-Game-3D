# Установщик
# Примечание : Если вы запускайте скомпилированный файл .exe а не .py, то
# вам не понадобится запускать этот файл установки.
from setuptools import setup

setup(
    name="Droid Game 3D",
    options = {
        "build_apps": {
            "gui_apps": {"DroidGame": "main.py"},
            "include_patterns": ["**/*"],
            "plugins": ["pandagl"],
            'platforms': [
                'manylinux1_x86_64',
                'macosx_10_6_x86_64',
                'win_amd64'
            ]
        }
    }
)
