# The Dodge Blocks Game in Concepts

## 1. Variables and Data Types
- `player_x`, `player_y`, `player_width`, `lives`, etc.
- Learn to store values and understand numbers, strings, lists, and dictionaries (`player_effect = {"type": None, "timer": 0}`).

## 2. Functions
- `spawn_obstacle()`, `update()`, `draw()`, `on_key_down()`
- Learn how to define reusable blocks of code and call them.
- Example: `spawn_obstacle()` handles one task repeatedly.

## 3. Control Flow
- **If statements**: movement, collision detection, game state checks if ...
- **For loops**: iterate over obstacles to move and check collisions. As long as ...
- Learn decision-making logic and applying actions to multiple items.

## 4. Lists and Iteration
- `obstacles = []` stores all falling blocks.
- Each obstacle is `[x, y, color]`.
- List manipulation: appending, removing, iterating, slicing.

## 5. Dictionaries
- `player_effect = {"type": None, "timer": 0}`
- Introduces key-value pairs to track multiple attributes of an entity.

## 6. Game Loop Concepts
- `update()` → updates game state (movement, collisions)
- `draw()` → renders visuals on screen

## 7. Randomness
- `random.randint()` used for spawning obstacles
- Introduces unpredictability in games.

## 8. Collision Logic
- Rectangle overlap check (`player_rect` vs `obs_rect`)
- Teaches geometric reasoning, logical AND/OR conditions, and step-by-step debugging.

## 9. State Management
- `game_state = "start" / "playing" / "gameover"`
- Learn tracking the state of a program, a foundational programming skill.



# Web

## Install streamlit

```
python3 -m venv quiz_env
source quiz_env/bin/activate   # macOS/Linux
# OR on Windows: quiz_env\Scripts\activate
python -m pip install --upgrade pip
pip install streamlit
```


## Run the app via

```
streamlit run quiz_app.py
````



````
source quiz_env/bin/activate
pip install jupyter ipywidgets pyyaml
```


```
pgzrun game.py
```
