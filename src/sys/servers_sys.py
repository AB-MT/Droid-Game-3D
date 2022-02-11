# система серверов
def new_server(database, name, port):
    '''добавление нового сервера'''
    database[port] = {'name': name} # добавляем сервер в базу

