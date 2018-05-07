# SimpleLog

## Developing

Create a Virtual Environment and install coverage

    python3 -m venv venv
    . venv/bin/activate
    pip install coverage

### Coverage

    coverage run --include=simplelog/* test.py
    coverage html -d docs/coverage
