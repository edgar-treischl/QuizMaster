import pgzrun
import random

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

# --- Obstacles (falling blocks) ---
obstacles = []  # This list will hold all obstacles currently on screen
# Each obstacle is a list: [x_position, y_position, color]
# Example: [150, 0, "red"] → a red block at x=150, y=0 (top of the screen)

# Size of each obstacle rectangle
obstacle_width = 30
obstacle_height = 30

fall_speed = 5   # How many pixels each obstacle moves down every frame

# spawn_rate controls how often new obstacles appear
# Smaller numbers → more frequent spawning, bigger numbers → less frequent
spawn_rate = 30  

# -------------------------
# Function to create a new obstacle
# -------------------------
def spawn_obstacle():
    # Choose a random x position so the obstacle can appear anywhere horizontally
    x = random.randint(0, WIDTH - obstacle_width)

    # Choose the obstacle color randomly:
    # 50% chance to be red (danger) and 50% chance to be green (heal)
    if random.randint(1, 2) == 1:
        color = "red"
    else:
        color = "green"

    # Add the new obstacle to the list
    # It starts at the top of the screen (y=0) with the chosen x and color
    obstacles.append([x, 0, color])

def draw():
    screen.clear()
    
    if game_state == "start":
        screen.draw.text("DODGE THE BLOCKS", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="white")
        screen.draw.text("Press SPACE to start", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="yellow")
    elif game_state == "playing":
        # Draw player
        screen.draw.filled_rect(Rect((player_x, player_y), (player_width, player_height)), "blue")
        
        # Draw obstacles
        for obs in obstacles:
            screen.draw.filled_rect(Rect((obs[0], obs[1]), (obstacle_width, obstacle_height)), obs[2])

def update():
    global player_x
    
    if game_state != "playing":
        return
    
    # Move player
    if keyboard.left and player_x > 0:
        player_x -= player_speed
    if keyboard.right and player_x < WIDTH - player_width:
        player_x += player_speed
    
    # Spawn obstacles randomly
    if random.randint(1, spawn_rate) == 1:
        spawn_obstacle()
    
    # Move obstacles down
    for obs in obstacles[:]:
        obs[1] += fall_speed
        # Remove obstacles that go off screen
        if obs[1] > HEIGHT:
            obstacles.remove(obs)

def on_key_down(key):
    global game_state
    if key == keys.SPACE and game_state == "start":
        game_state = "playing"

pgzrun.go()
