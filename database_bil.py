import sqlite3

def create_billing_database():
    connection = sqlite3.connect('billing_database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER UNIQUE,
            room_type TEXT NOT NULL,
            days_stayed INTEGER NOT NULL,
            season TEXT NOT NULL,
            daily_rate REAL NOT NULL,
            total_bill REAL NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_billing_database()

