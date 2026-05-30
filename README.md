## Setup

> **Note:** Pygame does not yet support Python 3.14+. This project strictly requires **Python 3.13**.

### 0. Prerequisites
You must have [uv](https://astral.sh) installed. If needed, you can install it via pip:
```bash
pip install uv
```

### 1. Virtual Environment Configuration
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
