import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Audio3DManager import Audio3DManager

manager = None
enabled = True

# Специальный класс звуков, которые не теряются на фоне других

class FlatSound(DirectObject):
    def __init__(self, file, volume=1.0):
        if enabled:
            self.sound = loader.loadSfx(file)
        self.filename = file
        self.setVolume(volume)

    def setVolume(self, volume):
        if enabled:
            self.sound.setVolume(volume)

    def getVolume(self):
        if enabled:
            return self.sound.getVolume()
        else:
            return 0.0

    def isPlaying(self):
        if enabled:
            return self.sound.status() == 2
        else:
            return False

    def play(self):
        if enabled:
            self.sound.play()

    def setLoop(self, loop):
        if enabled:
            self.sound.setLoop(loop)

    def stop(self):
        if enabled:
            self.sound.stop()
