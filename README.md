## Notes for Developers

> [!IMPORTANT]
>Remember to work on your individual branches. When pushing code and opening a PR remember to pull from `main` branch first. 

## Setup

> **Note:** Pygame does not yet support Python 3.14+. This project uses Python 3.13.

### Prerequisites
You must have [uv](https://astral.sh) installed. If needed, you can install it via pip:
```bash
pip install uv
```

### Virtual Environment Configuration
1. Clone the repository and navigate into it:
   ```bash
   git clone <this-repo>
   cd <this-repo>
   ```

If using PyCharm, you may simply open the repository folder in PyCharm. PyCharm will automatically detect your configuration and handle creating and managing the virtual environment via `uv` for you.

2. If using the terminal, create your virtual environment (uv will automatically download Python 3.13 if your system lacks it):
   ```bash
   uv venv
   ```
3. Activate the virtual environment:
   * **macOS / Linux:** `source .venv/bin/activate`
   * **Windows (Command Prompt):** `.venv\Scripts\activate`


## Database Setup
1. Copy `config_template.py` and rename it to `config.py`
2. Fill in your MySQL password and database name:
```python
   db_config = {
       "host": "localhost",
       "user": "root",
       "password": "your_password_here",
       "database": "dino_game"
   }
```
3. Run the SQL schema to create the database and tables:
```bash
   mysql -u root -p < Pygame_DB.sql
```

## Running the Application
Open two separate terminals and run:

Terminal 1 — start the API:
```bash
uv run api.py
```

Terminal 2 — start the game:
```bash
uv run dino-game.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/players` | Creates a new player with a username |
| POST | `/game_runs` | Starts a new game run for a player |
| PUT | `/game_runs/<id>` | Updates the score and end time of a game run |
| GET | `/leaderboard` | Fetches the top 10 scores |
| DELETE | `/game_runs/<id>` | Deletes a specific game run |