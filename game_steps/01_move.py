import pgzrun

# --- Window size ---
WIDTH = 400
HEIGHT = 600

# --- Player setup ---
player_width = 50
player_height = 30
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed = 5

# --- Game state ---
game_state = "start"

def draw():
    screen.clear()
    
    if game_state == "start":
        screen.draw.text("DODGE THE BLOCKS", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="white")
        screen.draw.text("Press SPACE to start", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="yellow")
    elif game_state == "playing":
        screen.draw.filled_rect(Rect((player_x, player_y), (player_width, player_height)), "blue")

def update():
    global player_x  # We need to modify the global variable player_x (player's horizontal position)

    # Only update the game if it is currently in the "playing" state.
    # If the game hasn't started or is over, we don't move the player or update anything.
    if game_state != "playing":
        return  # Stop running the rest of the update function

    # --- Move player left ---
    # If the left arrow key is pressed AND the player is not already at the left edge of the screen:
    if keyboard.left and player_x > 0:
        player_x -= player_speed  # Move the player to the left by subtracting player_speed from x

    # --- Move player right ---
    # If the right arrow key is pressed AND the player is not already at the right edge of the screen:
    if keyboard.right and player_x < WIDTH - player_width:
        player_x += player_speed  # Move the player to the right by adding player_speed to x

def on_key_down(key):
    global game_state
    if key == keys.SPACE and game_state == "start":
        game_state = "playing"

pgzrun.go()
