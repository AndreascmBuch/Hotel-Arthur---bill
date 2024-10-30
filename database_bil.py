import sqlite3

# Connect to billing database and create the billing table
with sqlite3.connect('billing_database.db') as conn_billing:
    cursor_billing = conn_billing.cursor()
    
    # Create billing table with season column
    cursor_billing.execute(''' 
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            room_type TEXT NOT NULL,
            days_stayed INTEGER NOT NULL,
            season TEXT NOT NULL,
            daily_rate REAL NOT NULL, 
            total_bill REAL NOT NULL, 
            FOREIGN KEY (booking_id) REFERENCES booking(id) 
        ) 
    ''')

    # Save changes are automatically committed when using 'with' context

# No need to explicitly close the connection; it is handled by the context manager.

