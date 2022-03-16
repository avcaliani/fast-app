.DEFAULT_GOAL := info

# Project
PROJECT_NAME = "fast-app-api"
CURRENT_VERSION = $(shell git describe --tags `git rev-list --tags --max-count=1` | grep --perl-regexp '\d+' --only-matching)
NEW_VERSION = $(shell expr $(CURRENT_VERSION) + 1 )

info:
	@echo "-----------< project >-----------"
	@echo " name              $(PROJECT_NAME)"
	@echo " current version   v$(CURRENT_VERSION)"
	@echo " new version       v$(NEW_VERSION)"
	@echo ""

install:
	poetry install
	poetry run pre-commit install
	poetry run pre-commit run -a -v

update-deps:
	poetry update
	poetry run pre-commit autoupdate

test:
	poetry run pytest -sx

run:
	# APP_ENV is an environment variable used by Dynaconf
	# to indicate which profile should be used.
	APP_ENV=dev uvicorn main:app --log-config "resources/log-config.yml" --reload

deploy:
	git tag "v$(NEW_VERSION)"
	git push origin "v$(NEW_VERSION)"

.PHONY: info install update-deps test run deploy
