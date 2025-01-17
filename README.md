# TravelAI (Simple Langchain/NextJS Project)

## Demo

https://www.loom.com/share/697764c024a54009afa4c15c6ab2faa1

## Approach

Its a simple nextjs/python-fastapi CRUD app for the most part. Since I have limited time I opted to not engineer any real code patterns or utilize a backend worker etc and just get a working MVP up and running.
I was given two basic tables (destinations, knowledge_base) which in theory could work for RAG but a large knowledge_base would get pretty slow so I opted to add another column (vector) and utilize the `pg_vector`
extension. This sounded simple in theory, since langchain seemed to have support and there's a pre-existing PGVector module. However this didn't work as it only creates and works with its own tables, therefore
I had to create a small retriever class of my own and manually query the database.

For the weather api there's a really simply `pyowm` module I was able to use and it worked pretty easily with langchain (a very solved problem.)

### Considerations

- Due to limited time I didn't do extensive handling of inputs, needed to get something out rather than polish

- The weather api can be finicky, if I ask for the weather in some other place that doesn't exist it will error

### Potential Next Steps

- Use something like auth0 or firebase to add a user system

- Improve RAG utilizing some other module (didn't have a lot of time to deep dive) or some better supported vector database

- Add a thin wrapper around the weather module to ensure it never errors or at least we catch the errors and say we don't know the weather when it does

- Add deletion of destinations, deletion and editing of knowledge base

- Get destinations from e.g. google maps api instead of manually entering

- Improve design

## Setup

### Backend

- Setup DB

  - Run docker compose `docker-compose up -d`

  - Install pg-vector `psql $DATABASE_URL -f setup.sql`

- Setup Environment

  - Setup env `python3 -m venv environment`

  - Install requirements `pip3 install -r requirements.txt`

- Copy `env.example` to `.env` in the `backend` directory and fill in

- Run
  - Run `bash run.sh` (will run a hot-reloading server)

### Frontend

- Install deps `yarn install`

- Copy `env.example` to `.env` in the `frontend` directory and fill in

- Run `yarn dev`
