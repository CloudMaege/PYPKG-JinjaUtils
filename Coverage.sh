poetry run coverage run -m --omit=tests/* --source=. pytest tests/test_jinja.py
poetry run coverage html --omit=tests/* -i
