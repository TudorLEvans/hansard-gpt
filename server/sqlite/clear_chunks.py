import os
# from server.scraper import STORAGE_PATH
import sqlite3

STORAGE_PATH = os.getenv("STORAGE_PATH", "D:\\hansard")
if __name__ == "__main__":
    # Read the list of dumped files
    con = sqlite3.connect(os.path.join(STORAGE_PATH, "database.db"))
    try:
        cur = con.cursor()
        res = cur.execute("DELETE FROM chunks")
        con.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if con:
            con.close()
            print("The Sqlite connection is closed")
