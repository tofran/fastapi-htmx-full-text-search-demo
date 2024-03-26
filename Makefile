help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-21s\033[0m %s\n", $$1, $$2}'

setup-venv: ## Setup a local venv
	python3 -m venv venv

install: ## Install python dependencies for a production server
	pip install -r requirements.txt
	wget -O ./static/htmx.min.js "https://github.com/bigskysoftware/htmx/releases/download/v1.9.10/htmx.min.js"

install-dev: install ## Install python dependencies for development
	pip install -r requirements-dev.txt

dev: # Start the development server
	DEVELOPMENT_MODE=True uvicorn --host "0.0.0.0" --reload text_search_app.app:app

start: # Serve the app with a production ready server
	uvicorn --host "0.0.0.0" text_search_app.app:app

lint: ## Lint the code according to the standards
	ruff check .
	ruff format --check .
	pyright .

format: ## Format the code according to the standards
	ruff check --fix .
	ruff format .
