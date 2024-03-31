# Python FastAPI HTMX full-text-search demo

This project is a **demo** full-text-search application that compares the results from
[SQLite FT5](https://www.sqlite.org/fts5.html) and 
[Algolia Search platform](https://www.algolia.com/).
 
Conceived as an experimental venture, this project serves as a demonstration of an *unconventional*
monolith tech stack. It features an interactive front-end, using a mix of traditional
Server Side Rendering (SSR) declarative web framework with zero custom JS:

- [FastAPI](https://fastapi.tiangolo.com/) the server framework;
- [Jinja](https://jinja.palletsprojects.com/) for the SSR templating;
- [HTMX](https://htmx.org/) to enable front-end interactivity declaratively directly in the HTML.

## Description and demo

**[Live demo](https://full-text-search-demo.tofran.com/)**

https://github.com/tofran/fastapi-htmx-full-text-search-demo/assets/5692603/43d642fd-52d5-4e5b-836a-6609d0c3d782

The outcome of this project is something very simple and minimal. The served content is **tiny** and
**fast**. There's no initial loading, everything is pre-rendered on the server, and each API request
renders HTML that is injected into the DOM - no need for Hydration, Resumability nor even data
serialization. It is compatible with most browsers, all the way back to IE11, where it struggles a
little with style, but *works*.

![OpenAPI spec (swagger)](https://github.com/tofran/fastapi-htmx-full-text-search-demo/assets/5692603/541f1f1a-fe1d-475c-8723-8f5a13e8f0df)

The application works by serving a full rendered Jinja HTML template when the user navigates to a
Front-End route.
These templates are composed via smaller reusable templates (using `include`).
And then the templates (*components*) are also served, de-coupled from the whole page in the
*HTML API* (`/html-api/...`).
HTMX handles the rest, listens to DOM events and updates it when when necessary.

![Example HTML API request/response](https://github.com/tofran/fastapi-htmx-full-text-search-demo/assets/5692603/8e1aa2a0-53dd-443a-a1d2-caee11cad65c)

## Development

- Create a `.env` file based on the `.env.template`.  
  You will need an Algolia account, should be pretty simple to setup
  (more info in their [Quick start guide](https://www.algolia.com/doc/guides/getting-started/quick-start/)).

- Setup a local environment with `make setup-venv`,
  activate it with `source ./venv/bin/activate`
  (or with your favourite tool).
  
- Install dependencies: `make install-dev`.

- Start the development server: `make dev`.

## Deployment

For deployment one would use the `./Dockerfile` and set the required environment variables.

For running locally a production like build, install the dependencies with `make install`
and run the application with `make start`. That's it.
