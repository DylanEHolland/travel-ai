## Backend

    *   Setup DB
        *   Run docker compose `docker-compose up -d`

        *   Install pg-vector `psql $DATABASE_URL -f setup.sql`

    *   Setup Environment

        *   Setup env `python3 -m venv environment`

        *   Install requirements `pip3 install -r requirements.txt`

    *   Run
        *   Run `python3 -m travelapi

## Frontend

    *   Install deps `yarn install`

    *   Run `yarn dev`
