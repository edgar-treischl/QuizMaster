import pgzrun  # Pygame Zero library – lets us make simple games

# --- Window size ---
# WIDTH and HEIGHT define the size of the game window in pixels
WIDTH = 400
HEIGHT = 600

# --- Player setup ---
# These define the player's rectangle (position, size, speed)
player_width = 50         # width of the player rectangle
player_height = 30        # height of the player rectangle
player_x = WIDTH // 2     # starting x position (center of the screen)
player_y = HEIGHT - 50    # starting y position (near the bottom)
player_speed = 5          # how many pixels the player moves each frame

# --- Game state ---
# Tracks whether the game is at the start screen, playing, or game over
game_state = "start"

# --- Lives and score ---
score = 0       # the player’s current score
high_score = 0  # highest score achieved in this session
lives = 3       # how many hits the player can take
max_lives = 5   # maximum lives a player can have

# -------------------------
# Draw function
# -------------------------
def draw():
    screen.clear()  # clear the screen each frame

    if game_state == "start":
        # Draw the title text
        screen.draw.text(
            "DODGE THE BLOCKS", 
            center=(WIDTH//2, HEIGHT//2), 
            fontsize=50, 
            color="white"
        )
        # Draw instructions
        screen.draw.text(
            "Press SPACE to start", 
            center=(WIDTH//2, HEIGHT//2 + 50), 
            fontsize=30, 
            color="yellow"
        )
    elif game_state == "playing":
        # Draw the player as a simple rectangle
        # Rect((x, y), (width, height)) defines the rectangle
        screen.draw.filled_rect(
            Rect((player_x, player_y), (player_width, player_height)), 
            "blue"
        )

# -------------------------
# Update function
# -------------------------
def update():
    pass  # nothing moves yet – we'll add movement later

# -------------------------
# Key press handler
# -------------------------
def on_key_down(key):
    global game_state
    # Start the game when SPACE is pressed on the start screen
    if key == keys.SPACE and game_state == "start":
        game_state = "playing"

# Start the game loop
pgzrun.go()
