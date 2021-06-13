# Файл с настройками игры
import src.ipgetter as ipgetter
# Настройки, информция

VERSION = 'beta 9.2.8' # версия
COPYRIGHT = 'Mark Kim 2021' # автор, год создания
DEVELOP_MODE = False # не включаем режим разроботчика
DEFAULT_IP = '127.0.0.1' # IP по умолчанию
IP_USER = ipgetter.myip() # IP пользователя
DEFAULT_PORT = '1337' # Порт по умолчанию

DEFAULT_SERVER = DEFAULT_IP + ':' + DEFAULT_PORT # сервер по умолчанию
SERVER_USER = IP_USER + ':' + DEFAULT_PORT # айпи и порт сервера, если его создаст игрок

LEVEL1 = './levels/maps/Default/level1.txt' # первый уровень
LEVEL2 = './levels/maps/Default/level2.txt' # второй уровень
LEVEL3 = './levels/maps/Default/level3.txt' # третий уровень

# шрифты
arial = './fonts/arial.ttf' # arial шрифт
doom_font = './fonts/doom_font.ttf' # doom font шрифт
ubunutumonobi = './fonts/UbuntuMono-BI.ttf' # UbunutuMono-BI шрифт
iAWriterDuoSBold = './fonts/iAWriterDuoS-Bold.ttf' # да что вы от меня хотите? сами видите как переменная называется, значит такой шрифт
VictorMonoBoldItalic = './fonts/VictorMono-BoldItalic.ttf' #  VictorMono-BoldItalic шрифт
