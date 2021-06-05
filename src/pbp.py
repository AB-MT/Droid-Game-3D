import math

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

load_prc_file_data("",
"""
framebuffer-multisample true
multisamples 2
"""
)
   
def color_from_temperature(temp):
    # цвет из температуры
    
    temp /= 100
    if temp <= 66:
        red = 255
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.133047592)
        red = max(0, red)
        red = min(255, red)
    if temp <= 66:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
        green = max(0, green)
        green = min(255, green)
    else:
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        green = max(0, green)
        green = min(255, green)
    if temp >= 66:
        blue = 255
    else:
        if temp <= 19:
            blue = 0
        else:
            blue = temp - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
            blue = max(0, blue)
            blue = min(255, blue)
    return (red / 255, green / 255, blue / 255)

class ShadingFramework:
    def __init__(self, root):
        # включаем шейдеры
        self.root = root
        self.root.set_antialias(AntialiasAttrib.MAuto)
        base.task_mgr.add(self.update, "update")

        self.shader = Shader.load(Shader.SL_GLSL, vertex = "./shaders/realistic/shadow.vert", fragment = "./shaders/realistic/shadow.frag")
        self.root.set_shader(self.shader)

    def update(self, task):
        return task.cont
