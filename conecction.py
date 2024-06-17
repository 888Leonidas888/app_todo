import mysql.connector
from mysql.connector import Error
from os import getenv

class DBStorage:
    connection = ''

    def __init__(self, user, password, database) -> None:
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            database=self.database,
            user=self.user,
            password=self.password)
        print('starting connection')

    def disconnect(self):
        self.connection.close()
        print('close connection')

    def read(self):
        try:
            records = ''
            cursor = self.connection.cursor()
            cursor.execute('select * from table_todo')
            records = cursor.fetchall()
            cursor.close()
            self.disconnect()
            return records
        except Error as err:
            print(err)
            return False

    def create(self, title, description, status):
        record = (title, description, status)
        sql = '''
                insert into table_todo(title, description, status) 
                values(%s,%s,%s)
            '''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, record)
            self.connection.commit()
            cursor.close()
            self.disconnect()
            return True
        except Error as err:
            print(err)
            return False

    def delete(self, id):
        sql = '''
            delete from table_todo where id = %s
        '''
        try:

            cursor = self.connection.cursor()            
            cursor.execute(sql, (id,))
            self.connection.commit()
            cursor.close()
            self.disconnect()
            return True
        except Error as err:
            print(err)
            return False

    def update(self, id, title=None, description=None, status=None):
        fields = []
        values = []

        sql = '''
            update table_todo set
            '''
        if title is not None:
            fields.append('title = %s')
            values.append(title)

        if description is not None:
            fields.append('description = %s')
            values.append(description)

        if status is not None:
            fields.append('status = %s')
            values.append(status)

        values.append(id)

        sql = sql + f'{", ".join(fields)}' + ' where id = %s'
        # print(sql)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, tuple(values))
            self.connection.commit()
            cursor.close
            self.disconnect()
            return True
        except Error as err:
            print(err)
            return False


# cnn = DBStorage('root', getenv('mysql_pass'), 'todo_db')
# cnn.connect()

# 1 Read
# records = cnn.read()
# for r in records:
#     print(r)

# 2 Create
# result = (cnn.create('quinta entrada', 'quinta descripcion', True))
# if result:
#     print('data ingresada')
# else:
#     print('Error ver la consola.')

# 3 Delete
# result = (cnn.delete(3))
# if result:
#     print('Succesful')
# else:
#     print('Failed')

# 4 Update
# result = (cnn.update(2,description='hi peru', status=False))
# if result:
#     print('Succesful')
# else:
#     print('Failed')
