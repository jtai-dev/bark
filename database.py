import sqlite3

'''
CREATE TABLE IF NOT EXISTS bookmarks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title, TEXT NOT NULL,
    url, TEXT NOT NULL,
    notes, TEXT,
    date_added, TEXT NOT NULL
)
'''

'''
INSERT INTO bookmarks
(title, url, notes, date_added)
VALUES ('GitHub', 'http://github.com', 'A place to store repositories and code',
        '2019092091T8:46:32.125467')
'''

'''
DELETE FROM bookmarks
WHERE ID = 3;
'''

'''
SELECT * FROM bookmarks
WHERE bookmark_id = 1
ORDER BY title
'''


class DatabaseManager:

    #Creates and stores a connection to the database for later use
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    #Cleans up the connection when done, to be safe
    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()

            #Executes the statement providing any passed in values to the placeholders
            cursor.execute(statement, values or [])
            return cursor

    #'C' of the CRUD
    def create_table(self, table_name, columns):
        #Converts columns - type(dict)- into a list of items for concatenation
        column_with_types = [
        f'{column_name} {data_type}' for column_name, data_type in columns.items()
        ]

        self._execute(
        f'''
        CREATE TABLE IF NOT EXISTS {table_name}
        ({','.join(column_with_types)});
        '''
        )

    #'U' of the CRUD
    def add(self, table_name, data):
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())

        self._execute(
        f'''
        INSERT INTO {table_name}
        ({column_names})
        VALUES ({placeholders});
        ''',
        tuple(data.values())
        )

    #'D' of the CRUD
    def delete(self, table_name, criteria):
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)

        self._execute(
        f'''
        DELETE FROM {table_name}
        WHERE {delete_criteria};
        ''',
        tuple(criteria.values())
        )

    #'R' of the CRUD
    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f'WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'

        return self._execute(
            query,
            tuple(criteria.values())
        )
