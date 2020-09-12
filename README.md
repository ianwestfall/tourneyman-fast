# tourneyman-fast
A basic tournament management application built with:
- Backend 
  - [Python 3.7](https://www.python.org/)
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [SQLAlchemy](https://www.sqlalchemy.org/)
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/)
  - [pytest](https://docs.pytest.org/en/stable/)
- Frontend
  - [VueJS](https://vuejs.org/)
  - [Mocha](https://mochajs.org/) + [Chai](https://www.chaijs.com/)
  - [ESLint](https://eslint.org/)
  - [Cypress](https://www.cypress.io/)
 - [PostgreSQL 12](https://www.postgresql.org/)
 - [Docker](https://www.docker.com/)
 
## To run
Checkout the project and run `docker-compose up` from `./`. You'll see:
- The API on port `8000`
  - [Cool interactive docs](http://localhost:8000/docs#/)
- The FE on port `8080`
  - [Home page](http://localhost:8080/)
- The DB on port `5432`
- pgAdmin on port `5050`
  - [Login](http://localhost:5050/browser/)

*Note: This is just a dev setup and should probably not be used for anything but that.*

## Tests
### Backend
From `./` run `pytest`

### Frontend 
From `./frontent`:
- run `npm run test:unit` for unit tests
- run `npm run test:e2e` for E2E tests
