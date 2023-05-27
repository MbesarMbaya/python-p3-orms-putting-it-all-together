import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Initialize id attribute to None

    @classmethod
    def create_table(cls):
        create_query = '''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                breed TEXT
            )
        '''
        CURSOR.execute(create_query)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        drop_query = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(drop_query)
        CONN.commit()

    def save(self):
        insert_query = '''
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        '''
        CURSOR.execute(insert_query, (self.name, self.breed))
        self.id = CURSOR.lastrowid  # Set the id attribute with the last inserted row ID
        CONN.commit()

    @classmethod
    def new_from_db(cls, db_row):
        dog = cls(db_row[1], db_row[2])
        dog.id = db_row[0]
        return dog

    @classmethod
    def get_all(cls):
        select_query = "SELECT * FROM dogs"
        CURSOR.execute(select_query)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        select_query = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(select_query, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        select_query = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(select_query, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        else:
            return cls.create(name, breed)

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    def update(self):
        update_query = '''
            UPDATE dogs SET name = ?, breed = ?
            WHERE id = ?
        '''
        CURSOR.execute(update_query, (self.name, self.breed, self.id))
        CONN.commit()
