# Dino Game (name WIP)

## About

A dinosaur-themed game built with Pygame, connected to a Flask API and MySQL database. 
Players choose a unique username for the dinosaur and aim to jump over obstacles for as long as possible. 
Scores are saved automatically to a leaderboard so players can track and compare their performances across sessions.

## Notes for Developers

> [!IMPORTANT]
>Remember to work on your individual branches. When pushing code and opening a PR remember to pull from `main` branch first. 


## Setup

> **Note:** Pygame does not yet support Python 3.14+. This project uses Python 3.13.

### Prerequisites
You must have [uv](https://astral.sh) installed. If needed, you can install it via pip, which will install it globally:
```bash
pip install uv
```
### Project Structure
``` Code
.
├── assets
│   ├── audio
│   │   ├── game-music.mp3
│   │   ├── game-over.mp3
│   │   └── jump.mp3
│   ├── ground.png
│   ├── noon.png
│   ├── sky.png
│   ├── tree.png
│   └── trex.png
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   ├── backend
│   │   ├── api.py
│   │   ├── config_template.py
│   │   ├── config.py
│   │   ├── db
│   │   │   └── schema.sql
│   │   └── db_utils.py
│   ├── frontend
│   │   ├── api_client.py
│   │   ├── button.py
│   │   ├── constants.py
│   │   ├── dinogame.py
│   │   ├── displayfunctions.py
│   │   ├── gamerun.py
│   │   ├── gamestate.py
│   │   ├── local_scores.py
│   │   ├── obstacle.py
│   │   ├── obstaclefield.py
│   │   └── player.py
├── tests
│   ├── test_api.py
│   ├── test_dino_game.py
│   └── test_local_scores.py
└── uv.lock



```

### Virtual Environment & Project Dependencies Configuration
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
   
3. Installing Dependencies with uv

After activating your virtual environment, install all project dependencies using:
   ```bash
   uv sync
   ```
This command installs all dependencies listed in `pyproject.toml` and ensures all developers running this project use the same environment, downloading Python 3.13 if needed.

## Database Setup
1. Copy `config_template.py` and rename it to `config.py`.
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

Terminal 1 - start the API:
```bash
uv run api
```

Terminal 2 - start the game:
```bash
uv run dinogame
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/players` | Creates a new player with a username |
| POST | `/game_runs` | Starts a new game run for a player |
| PUT | `/game_runs/<id>` | Updates the score and end time of a game run |
| GET | `/leaderboard` | Fetches the top 10 scores |
| DELETE | `/game_runs/<id>` | Deletes a specific game run |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/[name-of-feature-branch]`)
3. Commit your changes (`git commit -m 'Add some [name-of-feature]'`)
4. Push to the branch (`git push origin feature/[name-of-feature-branch]`)
5. Open a Pull Request

## Credits

Developed by Anna Zhang, Boon Chin Look, Julia Kaczmarek, Katrina Griffard, May Tedros, Ogechi Izegbune - 2026.

This project was developed as part of a coding bootcamp to demonstrate practical software engineering skills, including Pygame, Python, Flask, SQL, and Version Control.
All images and videos included are used strictly for educational purposes.
