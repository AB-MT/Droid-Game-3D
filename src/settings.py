# Файл с настройками игры
import src.ipgetter as ipgetter
# Настройки, информция

VERSION = 'beta 9.1.6' # версия
COPYRIGHT = 'Mark Kim 2021' # автор, год создания
DEVELOP_MODE = False # не включаем режим разроботчика
DEFAULT_IP = '127.0.0.1' # IP по умолчанию
IP_USER = ipgetter.myip() # IP пользователя
DEFAULT_PORT = '1337' # Порт по умолчанию

DEFAULT_SERVER = DEFAULT_IP + ':' + DEFAULT_PORT # сервер по умолчанию
SERVER_USER = IP_USER + ':' + DEFAULT_PORT # айпи и порт сервера, если его создаст игрок

LEVEL1 = './levels/level1.txt' # первый уровень
LEVEL2 = './levels/level2.txt' # второй уровень
