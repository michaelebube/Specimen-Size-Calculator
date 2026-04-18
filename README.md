# CSC442 Question 5 Solution

This project implements all parts of Question 5:

- (a) Python program that calculates real-life size from microscope size.
- (b) Database extension storing username, microscope size, and actual size.
- (c) Python-based GUI (Tkinter).
- (d) Web-based GUI (Flask).
- (e) Free-hosting ready setup using Render (or Railway).

## Formula

Actual size = microscope size / magnification

## Project Files

- `core.py`: Shared logic + SQLite database operations.
- `cli_app.py`: Command-line version (parts a and b).
- `desktop_gui.py`: Tkinter desktop GUI (part c).
- `web_app.py`: Flask web GUI (part d).
- `templates/index.html`: Web interface template.
- `requirements.txt` + `Procfile`: Hosting/deployment support (part e).

## Run Locally

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run command-line app:

```bash
python cli_app.py
```

4. Run desktop GUI:

```bash
python desktop_gui.py
```

5. Run web GUI:

```bash
python web_app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Database

- SQLite file is created automatically at `data/specimens.db`.
- Table name: `specimen_records`
- Stored fields: username, microscope_size, magnification, actual_size, unit, created_at

## Free Hosting (Render Example)

1. Push this project to GitHub.
2. Create a free account on Render.
3. New -> Web Service -> Connect your GitHub repo.
4. Build command:

```bash
pip install -r requirements.txt
```

5. Start command:

```bash
gunicorn web_app:app
```

6. Deploy. Render provides a free public URL.

### Persist Data with Render Postgres (Recommended)

By default, this app uses SQLite locally. In production, it will automatically use PostgreSQL when the `DATABASE_URL` environment variable is available.

On Render:

1. Create a PostgreSQL service.
2. Open your Web Service settings.
3. Add an environment variable:
	- Key: `DATABASE_URL`
	- Value: Use the "Internal Database URL" from your Render Postgres service.
4. Redeploy your Web Service.

The app will then store records in Postgres instead of local SQLite.

## Notes

- If you want all sizes in one unit, keep `unit` as `um`.
- For assignment marking, include screenshots of CLI, desktop GUI, and web GUI outputs.
