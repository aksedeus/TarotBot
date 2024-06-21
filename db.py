import sqlite3
from datetime import datetime, timedelta
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            registered BOOLEAN
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            active BOOLEAN,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            currency TEXT,
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_usage (
            user_id INTEGER UNIQUE,
            uses_remaining INTEGER DEFAULT 5,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, registered) VALUES (?, ?, ?)', (user_id, username, True))
    cursor.execute('INSERT OR IGNORE INTO bot_usage (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_payment(user_id, amount, currency):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payments (user_id, amount, currency) VALUES (?, ?, ?)', (user_id, amount, currency))
    cursor.execute('UPDATE bot_usage SET uses_remaining = uses_remaining + 25 WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()

def get_payment_count(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM payments WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_bot_uses_remaining(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT uses_remaining, last_updated FROM bot_usage WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        uses_remaining, last_updated_str = result
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S.%f")


        if datetime.now() - last_updated >= timedelta(days=1):
            # If more than 24 hours have passed, update uses_remaining
            increment_usage_daily()
            return get_bot_uses_remaining(user_id)  # Recursively get updated uses_remaining

        return uses_remaining
    else:
        return 0  # Return 0 if record not found


def decrease_bot_uses(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bot_usage SET uses_remaining = uses_remaining - 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def increment_usage_daily():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, last_updated FROM bot_usage')
    results = cursor.fetchall()

    for user_id, last_updated_str in results:
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_updated >= timedelta(days=1):
            cursor.execute(
                'UPDATE bot_usage SET uses_remaining = uses_remaining + 5, last_updated = ? WHERE user_id = ?',
                (datetime.now(), user_id))

    conn.commit()
    conn.close()

init_db()
