SHELL:=/usr/bin/env bash

lint:
	ruff check .
	mypy .

lint_django:
	# check migrations graph
	python manage.py makemigrations --dry-run --check
	# lint migrations
	 python manage.py lintmigrations \
	 	--warnings-as-errors
	# run django check
	python manage.py check --fail-level=WARNING

unit:
	pytest \
		--cov=. \
		--junitxml=.tests_reports/junit.xml

lint_package:
	pip check

test: lint lint_django unit lint_package
