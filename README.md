# Hansard GPT

A vector-based search system for the Government's Hansard data set

## Installing

On the server side, you will need to install dependencies. You can do this with the following:

```
pip install -r server/requirements.txt
pip install -r server/requirements-dev.txt
```

There are three backend processes in operation:
1. scraper.py - used to scrape the web for Hansard data
2. vectors.py - provides a class that acts like a local instance of a vector DB, holding embeddings in memory and providing a utility for adding embeddings and performing vector search
3. main.py - entrypoint for the FastAPI service that handles user queries. Gets embeddings of the query, searches for similar embeddings from the memory store and then makes a call to GPT for an answer that it returns to the user

## Scraping

You can scrape data by running:

```
python server/scraper.py
```

This will take some time, and will dump the data in a sqlite file at a path of your choice.

## Chunking and Embedding

To operate the app, we need the data split into smaller chunks and embedded as vectors. The script to do this is run with the command:

```
python server/vectors.py
```

This will also take time and dumps the data in the same sqlite DB. Note that the vectors.py file also provides a class that acts as an in-memory vector store for the app.

## Run the API

You can run the api with a command as follows:

```
python -m uvicorn server.main:app --reload
```

A sample request to the server might look something like:

```
curl --location --request GET 'localhost:8000/answers?q=who%20am%20I?'
```