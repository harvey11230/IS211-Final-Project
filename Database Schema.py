import sqlite3

def main():
    with sqlite3.connect("database.db") as d:

        c = d.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS books(
        ISBN INTEGER PRIMARY KEY,
        Title TEXT,
        Authors TEXT,
        PageCount TEXT,
        AverageRating TEXT)
        """)

    d.commit()

if __name__ == '__main__':
    main()