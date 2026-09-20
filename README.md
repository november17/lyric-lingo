# lyric-lingo

A RESTful API and relational database for managing, annotating, and querying multilingual song lyrics, regional slang, and indigenous vocabulary.

## Features

- **Relational Line-Level Schema:** Maps raw lyrics down to individual lines, associating specific words or phrases with regional slang tags and literal/contextual translations.
- **Full-Text Search:** Query lyrics and term glossaries by language, country/region of origin, dialect, or custom tags.
- **RESTful API:** Clean JSON endpoints built with FastAPI for CRUD operations on tracks, lines, regional glossaries, and vocabulary origins.

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL / SQLite
- **ORM:** SQLAlchemy v2.0 (Async)

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## License

MIT
