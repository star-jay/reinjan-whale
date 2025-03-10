# Starwars API

This project is a Django REST API where you can manage a team of Star Wars characters and fight the dark side.

It was built by **Reinjan Ergo** as a technical hiring challenge.

## Requirements

### To run the project

- Docker

### To contribute

- **pipenv** to manage our virtual env and dependencies: `pip install pipenv`
- Docker

## Getting started

- Clone the repo
- Create your .env file by copying the sample `cp .env.sample .env`.
- Update the `.env` file to have meaningful values.
- Run `./scripts/build` to get started, this will set up the Docker containers (web & PostgreSQL).

## Additional commands

When the containers are running, we can run the following commands:

- Migrate the database:
```bash
docker exec -it reinjan-starwars-web python manage.py migrate
```

- Create a superuser to authenticate with:
```bash
docker exec -it reinjan-starwars-web python manage.py createsuperuser (--no-input)
```

- Load the character information:
```bash
docker exec -it reinjan-starwars-web python manage.py import_characters starwars-data.json
```

- Create an API token your user. Store it as the {{token}} variable in PostMan.

```bash
docker exec -it reinjan-starwars-web python manage.py drf_create_token <email>
```

## Data

- The character data was provided by an [external API](https://akabab.github.io/starwars-api/).
- The field names were renamed to `snake_case` to make them pythonic. In a later stage, this can easily be rendered in camelCase if wanted with the [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) module.

Import the characters with the following command:

```bash
docker exec -it reinjan-starwars-db python manage.py import_characters starwars-data.json (--reset)
```

To output a quick data analysis used to process the data run:
```bash
docker exec -it reinjan-starwars-db python manage.py import_characters starwars-data.json --analysis
```

## Usage

The API is available at `http://localhost:8000/`.
The endpoints are paginated and can be browsed with the `limit` and `offset` query params.

You can access the following endpoints:

- `/affiliations/`: List affiliations
- `/characters/`: List characters
- `/teams/`: List and teams
- `/team-memberships/`: List and manage teams.
- `/teams/<team_pk>/members/<character_pk>/`: Add (POST) and remove (DELETE) teammembers.
- `/characters/<character_pk>/teams/<team_id>/`: Add (POST) and remove (DELETE) teammembers.
- `/characters/attribute_list/`: Get a list of extra attributes for a character


## Postman

The postman collection authenticates to the API using the {{token}} variable.
- It lists the characters, fetches 7 different characters based on different traits.
- It adds 5 team members. But fails when trying to add an "evil" character.
- Fails when adding a 6th.
- Removes a team member.
- Adds a new team member.

# Contributing

## Running Tests

To run the tests, use the following command:

```bash
./scripts/test
```

## Linting

To run the linter, use the following command:

```bash
./scripts/lint
```

## Updating the Database

To update the database, use the following command:

```bash
./scripts/update
```

## Next steps

  - Upgrade the API tokens to the [knox](https://github.com/jazzband/django-rest-knox) package.
  - Add groups and permissions to create characters or modify teams.
  - Replace auto_increment PK's with a uuid field.
  - Extend the authentication features with registration, groups and permissions.
  - Provide simple jwt endpoints and allow users to auth with access and refresh tokens.
  - generate an openapi spec with [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) and provide a `/schema/` endpoint.
