import sqlite3
import random

DATABASE_NAME = 'blooddonor.db'  # SQLite database file for the blood donation app

def reset_back_to_start() -> None:
    """
    Reset the database to the initial state.

    This function drops the existing 'donors' table and recreates it.

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    print("[WARNING!] You need admin privilege to clear and reset the data! Are you sure? (y/n/yes/no)")
    a = input()
    c.execute("DROP TABLE IF EXISTS donors")
    if a in ("y", "yes"):
        c.execute('''CREATE TABLE IF NOT EXISTS donors
                    (uid INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     dob TEXT NOT NULL,
                     adhar TEXT NOT NULL,
                     nationality TEXT NOT NULL,
                     state TEXT NOT NULL,
                     address TEXT NOT NULL,
                     blood_type TEXT NOT NULL,
                     contact_phone TEXT NOT NULL
                     )''')

    conn.commit()
    conn.close()

def update_donor(uid, name=None, dob=None, adhar=None, nationality=None, state=None,
                  address=None, blood_type=None, contact_phone=None) -> None:
    """
    Update donor information in the database.

    Args:
        uid: User ID of the donor to update.
        name: New name (optional).
        dob: New date of birth (optional).
        adhar: New Aadhaar number (optional).
        nationality: New nationality (optional).
        state: New state (optional).
        address: New address (optional).
        blood_type: New blood type (optional).
        contact_phone: New contact phone (optional).

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    update_fields = []

    if name is not None:
        update_fields.append(("name", name))
    if dob is not None:
        update_fields.append(("dob", dob))
    if adhar is not None:
        update_fields.append(("adhar", adhar))
    if nationality is not None:
        update_fields.append(("nationality", nationality))
    if state is not None:
        update_fields.append(("state", state))
    if address is not None:
        update_fields.append(("address", address))
    if blood_type is not None:
        update_fields.append(("blood_type", blood_type))
    if contact_phone is not None:
        update_fields.append(("contact_phone", contact_phone))

    if len(update_fields) > 0:
        update_query = "UPDATE donors SET "
        update_query += ", ".join(f"{field} = ?" for field, _ in update_fields)
        update_query += " WHERE uid = ?"
        values = [value for _, value in update_fields]
        values.append(uid)
        c.execute(update_query, values)

    conn.commit()
    conn.close()

def generate_uid() -> int:
    """
    Generate a random 6-digit UID.

    Returns:
        int: Randomly generated UID.
    """
    return random.randint(100000, 999999)

def insert_donor(name, dob, adhar, nationality, state, address, blood_type, contact_phone) -> None:
    """
    Insert a new donor into the database.

    Args:
        name: Name.
        dob: Date of birth.
        adhar: Aadhaar number.
        nationality: Nationality.
        state: State.
        address: Address.
        blood_type: Blood type.
        contact_phone: Contact phone.

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    uid = generate_uid()

    c.execute("INSERT INTO donors (uid, name, dob, adhar, nationality, state, address, blood_type, "
              "contact_phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (uid, name, dob, adhar, nationality, state, address, blood_type, contact_phone))

    conn.commit()
    conn.close()

def read_donor(uid=-1) -> list:
    """
    Read donor details from the database.

    Args:
        uid: User ID to retrieve. If -1, retrieve all donors.

    Returns:
        list: Donor details as a list of dictionaries.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    if uid != -1:
        c.execute("SELECT * FROM donors WHERE uid = ?", (uid,))
        result = c.fetchone()
        donor_dict = {
            "uid": result[0],
            "name": result[1],
            "dob": result[2],
            "adhar": result[3],
            "nationality": result[4],
            "state": result[5],
            "address": result[6],
            "blood_type": result[7],
            "contact_phone": result[8]
        }
        return donor_dict

    else:
        c.execute("SELECT * FROM donors")
        result = c.fetchall()

    donor_list = []
    for row in result:
        donor_dict = {
            "uid": row[0],
            "name": row[1],
            "dob": row[2],
            "adhar": row[3],
            "nationality": row[4],
            "state": row[5],
            "address": row[6],
            "blood_type": row[7],
            "contact_phone": row[8]
        }
        donor_list.append(donor_dict)

    conn.close()

    return donor_list
