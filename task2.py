
import sqlite3
import re
import csv
import os

DB_NAME = "cloud_deduplication.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL
)
""")
conn.commit()


def valid_record(name, email, city):
    if not name.strip() or not city.strip():
        return False
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False
    return True


def add_record(name, email, city):
    name = name.strip()
    email = email.strip().lower()
    city = city.strip()

    if not valid_record(name, email, city):
        print("Invalid record! Please check the details.")
        return

    try:
        cursor.execute(
            "INSERT INTO records (name, email, city) VALUES (?, ?, ?)",
            (name, email, city)
        )
        conn.commit()
        print("Record saved successfully!")
    except sqlite3.IntegrityError:
        print("Duplicate record! Not saved.")


def view_records():
    cursor.execute("SELECT name, email, city FROM records")
    rows = cursor.fetchall()

    print("\n--- UNIQUE RECORDS ---")
    if not rows:
        print("No records found.")
    for row in rows:
        print("Name:", row[0], "| Email:", row[1], "| City:", row[2])


def export_csv():
    cursor.execute("SELECT name, email, city FROM records")
    rows = cursor.fetchall()

    with open("unique_records.csv", "w",
              newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "City"])
        writer.writerows(rows)

    print("Unique records exported to unique_records.csv")


def menu():
    while True:
        print("\n=== CLOUD DATA DEDUPLICATION SYSTEM ===")
        print("1. Add record")
        print("2. View unique records")
        print("3. Export records to CSV")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            city = input("Enter city: ")
            add_record(name, email, city)

        elif choice == "2":
            view_records()

        elif choice == "3":
            export_csv()

        elif choice == "4":
            conn.close()
            print("Thank you!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
