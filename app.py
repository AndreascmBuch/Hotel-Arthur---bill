import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Database connection for accessing billing database
def get_db_connection():
    try:
        conn = sqlite3.connect('billing_database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

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

def parse_dates(checkin, checkout):
    try:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
        return checkin_date, checkout_date
    except ValueError:
        return None, None

@app.route('/bills/update/<int:booking_id>', methods=['POST'])
def update_billing(booking_id):
    data = request.get_json()
    
    if not data or 'room_type' not in data or 'checkin' not in data or 'checkout' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    room_type = data['room_type']
    checkin = data['checkin']
    checkout = data['checkout']
    
    # Parse dates
    checkin_date, checkout_date = parse_dates(checkin, checkout)
    if checkin_date is None or checkout_date is None:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Calculate billing details
    days_stayed = (checkout_date - checkin_date).days
    if days_stayed <= 0:
        return jsonify({'error': 'Check-out date must be after check-in date'}), 400
    
    season = determine_season(checkin_date)
    daily_rate = room_rates.get(room_type)
    
    if not daily_rate:
        return jsonify({'error': 'Invalid room type'}), 400

    total_bill = days_stayed * daily_rate[season]

    # Insert or update billing record
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO billing (booking_id, room_type, days_stayed, season, daily_rate, total_bill)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(booking_id) DO UPDATE SET
            room_type=excluded.room_type,
            days_stayed=excluded.days_stayed,
            season=excluded.season,
            daily_rate=excluded.daily_rate,
            total_bill=excluded.total_bill
    ''', (booking_id, room_type, days_stayed, season, daily_rate[season], total_bill))

    conn.commit()
    conn.close()
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
def get_bill_by_id(id):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM billing WHERE id = ?', (id,))
        bill = cursor.fetchone()

    if not bill:
        return jsonify({'error': 'Bill not found'}), 404

    return jsonify(dict(bill))

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')

