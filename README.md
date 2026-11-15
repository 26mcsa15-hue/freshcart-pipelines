# freshcart-pipelines

Data Engineering assignment "From Git to Gold". The repo holds three small data pipelines and the CI that checks them.

## Folders

- `elt/` : Part B. FreshCart ELT notebook for Snowflake. Raw web and mobile orders are loaded into bronze, cleaned in silver, and published to a gold fact table. Bad rows go to a quarantine table.
- `iris_project/` : Part C. Mage pipeline `iris_classifier`. It runs `load_iris → validate_data → prepare_data → train_model`, then splits into `save_results` and `evaluate_model`. Each block has a `@test`, and a failing test stops the downstream blocks.
- `stream/` : Part D. RabbitMQ dispatcher and driver scripts using a topic exchange.
- `tests/` : pytest tests. `test_prepare_data.py` checks the 80/20 split.
- `.github/workflows/ci.yml` : GitHub Actions workflow. On every push it installs `requirements.txt` and runs pytest.

## Run the Mage pipeline

    mage run iris_project iris_classifier --test

To try a different tree depth:

    mage run iris_project iris_classifier --test --runtime-vars '{"max_depth": 3}'

## Run the tests

    pip install -r requirements.txt
    python -m pytest
