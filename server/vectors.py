import csv
import logging
import os
import sqlite3
from typing import List, Union

import numpy as np
from sentence_transformers import SentenceTransformer

from server.scraper import STORAGE_PATH, Sitting
from server.utils import chunk_data

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
LOGGER = logging.getLogger("server")

EMBEDDING_DIMENSIONS = 768


def sitting_factory(cursor, row):
    return Sitting(*row)


class LocalStore:
    """
    Acts as a local equivalent to a vector DB
    Everything is held in memory but saved to disk in case of server failure
    On reset, reads from disk to load data into memory (should be good up to O(100k) entries)
    """

    def __init__(self):
        self.embeddings = np.zeros((0, EMBEDDING_DIMENSIONS))

    def create_record(self, cur, sitting: Sitting, embedding):
        """
        Insert a new record into the dataframe

        Note it is not possible to add to the Storage dynamically (for now)
        """
        try:
            cur.execute(
                "INSERT INTO chunks (meeting_id, title, meeting_date, link, content, embedding) VALUES(?, ?, ?, ?, ?, ?)",
                (
                    sitting.meeting_id,
                    sitting.title,
                    sitting.date,
                    sitting.link,
                    sitting.text,
                    ",".join(str(x) for x in embedding),
                ),
            )
        except sqlite3.Error as error:
            print("Failed to read data from table", error)

    def reset(self, cur):
        """
        Reset is used by init to load in data.

        It is abstracted out so that new data added to the store can also be loaded into memory without reinstantiating the class
        """
        res = cur.execute("SELECT meeting_id, embedding FROM chunks")
        items = res.fetchall()
        self.embeddings = np.array(
            [[float(it) for it in item[1].split(",")] for item in items]
        )
        self.meetings = [item[0] for item in items]

    def similarity_search(self, vector, k_nearest=3) -> List[int]:
        """
        Function to perform cosine similarity search with query vector against in-memory store

        If performance issues become a problem this might need to be shifted to a vector DB.
        Tested at 50,000 array elements it seems to be quite performant :crosses fingers:
        """
        if len(self.embeddings) < k_nearest:
            return self.meetings
        normal_vector = vector / np.linalg.norm(vector, axis=0)
        sim_search = np.einsum("j,ij->i", normal_vector, self.embeddings)
        indices = np.argpartition(sim_search, -k_nearest)[-k_nearest:]
        return [self.meetings[i] for i in indices.tolist()]

    def get_sources(self, cur, embedding):
        meeting_ids = self.similarity_search(embedding)
        string_ids = "SELECT meeting_id, title, meeting_date, link, content FROM chunks WHERE meeting_id IN ("
        string_ids += ",".join([f"'{meeting_id}'" for meeting_id in meeting_ids])
        string_ids += ")"
        sittings = []
        res = cur.execute(string_ids)
        for row in res.fetchall():
            sittings.append(Sitting(*row))
        return sittings


if __name__ == "__main__":
    # Read the list of dumped files
    model = SentenceTransformer("all-MiniLM-L6-v2")
    con = sqlite3.connect(os.path.join(STORAGE_PATH, "database.db"))
    try:
        cur = con.cursor()

        cur.execute("PRAGMA encoding=UTF8")

        with open("./server/sqlite/chunks.sql") as file:
            schema = file.read()
            cur.execute(schema)
            con.commit()

        with open("./server/sqlite/dumps.sql") as file:
            schema = file.read()
            cur.execute(schema)
            con.commit()

        store = LocalStore()

        res = cur.execute(
            "SELECT meeting_id, title, meeting_date, link, content FROM text_dumps"
        )

        # Loop through the files
        for file in res.fetchall():
            # Create a sitting and load the text from the text blob
            sitting = Sitting(file[0], file[1], file[2], file[3], file[4])

            # Chunk the sittings, embed them and store them
            if sitting.text is not None:
                chunked_sittings = chunk_data(sitting)
                for sit in chunked_sittings:
                    embedding = model.encode(sit.text, normalize_embeddings=True)
                    store.create_record(cur, sit, embedding)
                    con.commit()

        store.reset(cur)
        cur.close()
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if con:
            con.close()
            print("The Sqlite connection is closed")
