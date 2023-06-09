import sqlite3

# Connect to ride tracking database
connection = sqlite3.connect("ride_tracker.db")

cursor = connection.cursor()


def create_table():
    # Create a table that holds a user's ID and the attractions they are tracking
    cursor.execute("""CREATE TABLE rides_tracked (user_id integer,
                       park_id integer,
                       ride_id integer,
                       wait_threshold integer,
                       reached_threshold integer
                   )""")
    connection.commit()


def insert_ride(user_id, park_id, ride_id, wait_threshold):
    # Check if an entry already exists
    # with the same user_id, park_id and ride_id
    # If it does, update the wait_threshold

    cursor.execute("""SELECT * FROM rides_tracked WHERE user_id = ? AND
                   park_id = ? AND ride_id = ?""", (user_id, park_id, ride_id))

    if cursor.fetchall():
        cursor.execute(
            """UPDATE rides_tracked SET wait_threshold = ? WHERE
            user_id = ? AND park_id = ? AND ride_id = ?""",
            (wait_threshold, user_id, park_id, ride_id)
        )
    else:
        cursor.execute("""INSERT INTO rides_tracked VALUES (?, ?, ?, ?, 0)""",
                       (user_id, park_id, ride_id, wait_threshold))
    connection.commit()
    

def update_reached_threshold(user_id, park_id, ride_id, reached_threshold):
    cursor.execute("""UPDATE rides_tracked SET reached_threshold = ? WHERE
                   user_id = ? AND park_id = ? AND ride_id = ?""",
                   (reached_threshold, user_id, park_id, ride_id))
    connection.commit()
    
    
def delete_ride(user_id, park_id, ride_id):
    cursor.execute("""DELETE FROM rides_tracked WHERE user_id = ? AND
                   park_id = ? AND ride_id = ?""", (user_id, park_id, ride_id))
    connection.commit()
    

def delete_all_rides(user_id):
    cursor.execute("""DELETE FROM rides_tracked WHERE user_id = ?""",
                   (user_id,))
    connection.commit()


def select_rides(user_id=None, park_id=None, ride_id=None):
    data = []
    if user_id is not None:
        data.append(user_id)
    if park_id is not None:
        data.append(park_id)
    if ride_id is not None:
        data.append(ride_id)

    cursor.execute(("SELECT * FROM rides_tracked" +
                    (" WHERE user_id = ?" if user_id is not None else "") +
                    (" AND park_id = ?" if park_id is not None else "") +
                    (" AND ride_id = ?" if ride_id is not None else "")),
                   tuple(data))

    return cursor.fetchall()
