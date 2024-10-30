import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Database connection for accessing billing database
def get_db_connection():
    conn = sqlite3.connect('billing_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Room rates by season
room_rates = {
    'Standard single room': {'high': 1200, 'mid': 1050, 'low': 900},
    'Grand lit room': {'high': 1400, 'mid': 1250, 'low': 1100},
    'Standard dobbeltroom': {'high': 1600, 'mid': 1400, 'low': 1200},
    'Superior room': {'high': 2000, 'mid': 1700, 'low': 1400},
    'Junior suite': {'high': 2500, 'mid': 2150, 'low': 1800},
    'Spa executive room': {'high': 2800, 'mid': 2400, 'low': 2000},
    'Suite room': {'high': 3500, 'mid': 3000, 'low': 2500},
    'Loft room': {'high': 4000, 'mid': 3500, 'low': 3000},
}

def determine_season(checkin_date):
    if checkin_date.month in [6, 7, 8, 12]:
        return 'high'
    if checkin_date.month in [4, 5, 9, 10]:
        return 'mid'
    else:
        return 'low'

@app.route('/bills/update/<int:booking_id>', methods=['POST'])
def update_billing(booking_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT category, checkin, checkout FROM booking WHERE id = ?', (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    room_type, checkin, checkout = booking['category'], booking['checkin'], booking['checkout']
    
    try:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Calculate billing details
    days_stayed = (checkout_date - checkin_date).days
    season = determine_season(checkin_date)
    daily_rate = room_rates[room_type][season]
    total_bill = days_stayed * daily_rate
    
    # Insert or update billing information
    cursor.execute(''' 
        INSERT INTO billing (booking_id, room_type, days_stayed, season, daily_rate, total_bill)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(booking_id) DO UPDATE SET
            room_type=excluded.room_type,
            days_stayed=excluded.days_stayed,
            season=excluded.season,
            daily_rate=excluded.daily_rate,
            total_bill=excluded.total_bill
    ''', (booking_id, room_type, days_stayed, season, daily_rate, total_bill))
    
    db.commit()
    db.close()
    return jsonify({'message': 'Billing updated', 'booking_id': booking_id})

# Access all bills in the database
@app.route('/bills', methods=['GET'])
def get_all_bills():
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM billing')
        bills = cursor.fetchall()
    return jsonify([dict(row) for row in bills])

# Access specific bill in the database by id
@app.route('/bills/<int:id>', methods=['GET'])
def get_bil_by_id(id):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM billing WHERE id = ?', (id,))
        bill = cursor.fetchall()

    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    return jsonify([dict(row) for row in bill])

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
