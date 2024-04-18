from processor.databasesetup import DatabaseManager
from config import DATABASE_NAME

def initialize_database():
    print(DATABASE_NAME)
    db = DatabaseManager(DATABASE_NAME)
    db.create_tables()
    print('Tables created successfully')

if __name__ == '__main__':
    initialize_database()