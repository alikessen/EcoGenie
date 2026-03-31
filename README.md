# EcoGenie

EcoGenie is a Flask web app that estimates a user's carbon footprint (diet, energy, transportation) and shows practical reduction recommendations.

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy and configure environment variables:

```bash
cp .env.example .env
```

`app.py` loads `.env` automatically for local development.

## Environment Variables

- `FLASK_SECRET_KEY`: Flask session secret key.
- `FLASK_DEBUG`: `1` for debug mode, `0` for production-like local runs.
- `DB_HOST`: MySQL host.
- `DB_PORT`: MySQL port.
- `DB_USER`: MySQL username.
- `DB_PASSWORD`: MySQL password.
- `DB_NAME`: MySQL database name.

## Run

```bash
python app.py
```

App runs at `http://127.0.0.1:5000`.

## Test

```bash
pytest -q
```

## Architecture Summary

- `app.py`: Flask routes, auth flow, session orchestration.
- `modules/form_parsers.py`: form parsing + normalization + validation.
- `modules/*_module.py`: footprint and recommendation logic.
- `modules/db.py`: MySQL access functions.
- `templates/`: Jinja templates.
- `data/carbon_data.csv`: emission factors.


