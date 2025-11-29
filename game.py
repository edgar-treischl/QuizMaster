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
player_radius = 8  # corner radius for rounded rectangle

# --- Obstacles ---
obstacles = []  # list of [x, y, type] where type='red' or 'green'
obstacle_width = 30
obstacle_height = 30
obstacle_radius = 6  # corner radius

# --- Game stats ---
score = 0
high_score = 0
lives = 3
max_lives = 5

# --- Difficulty variables ---
fall_speed = 5
spawn_rate = 30

# --- Game state ---
game_state = 'start'  # 'start', 'playing', 'gameover'

# --- Helper function: draw rounded rectangle ---
def draw_rounded_rect(x, y, width, height, color, radius):
    # center rectangle
    screen.draw.filled_rect(Rect((x + radius, y), (width - 2*radius, height)), color)
    screen.draw.filled_rect(Rect((x, y + radius), (width, height - 2*radius)), color)
    # four corner circles
    screen.draw.filled_circle((x + radius, y + radius), radius, color)
    screen.draw.filled_circle((x + width - radius, y + radius), radius, color)
    screen.draw.filled_circle((x + radius, y + height - radius), radius, color)
    screen.draw.filled_circle((x + width - radius, y + height - radius), radius, color)

# --- Spawn an obstacle or power-up ---
def spawn_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = 0
    block_type = 'green' if random.randint(1, 5) == 1 else 'red'
    obstacles.append([x, y, block_type])

# --- Update function ---
def update():
    global player_x, score, high_score, fall_speed, spawn_rate, lives, game_state

    if game_state != 'playing':
        return

    if keyboard.left and player_x > 0:
        player_x -= player_speed
    if keyboard.right and player_x < WIDTH - player_width:
        player_x += player_speed

    if random.randint(1, spawn_rate) == 1:
        spawn_obstacle()

    for obs in obstacles[:]:
        obs[1] += fall_speed
        if obs[1] > HEIGHT:
            if obs[2] == 'red':
                score += 1
            obstacles.remove(obs)

    player_rect = (player_x, player_y, player_width, player_height)
    for obs in obstacles[:]:
        obs_rect = (obs[0], obs[1], obstacle_width, obstacle_height)
        if rects_collide(player_rect, obs_rect):
            if obs[2] == 'red':
                lives -= 1
                if lives <= 0:
                    if score > high_score:
                        high_score = score
                    game_state = 'gameover'
            elif obs[2] == 'green':
                lives = min(max_lives, lives + 1)
            obstacles.remove(obs)

    if score > 0 and score % 10 == 0:
        fall_speed = 5 + score // 10
        spawn_rate = max(10, 30 - score // 5)

# --- Collision check ---
def rects_collide(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

# --- Reset game ---
def reset_game():
    global obstacles, score, lives, fall_speed, spawn_rate, player_x
    obstacles.clear()
    score = 0
    lives = 3
    fall_speed = 5
    spawn_rate = 30
    player_x = WIDTH // 2

# --- Handle key presses ---
def on_key_down(key):
    global game_state
    if key == keys.SPACE:
        if game_state == 'start' or game_state == 'gameover':
            game_state = 'playing'
            reset_game()

# --- Draw everything ---
def draw():
    screen.clear()
    if game_state == 'start':
        screen.draw.text("DODGE THE BLOCKS", center=(WIDTH//2, HEIGHT//2 - 30),
                         fontsize=50, color="white")
        screen.draw.text("Press SPACE to start", center=(WIDTH//2, HEIGHT//2 + 30),
                         fontsize=30, color="yellow")
    elif game_state == 'playing':
        draw_rounded_rect(player_x, player_y, player_width, player_height, 'blue', player_radius)
        for obs in obstacles:
            color = 'red' if obs[2] == 'red' else 'green'
            draw_rounded_rect(obs[0], obs[1], obstacle_width, obstacle_height, color, obstacle_radius)
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"High Score: {high_score}", (10, 40), fontsize=30, color="yellow")
        screen.draw.text(f"Lives: {lives}", (10, 70), fontsize=30, color="red")
    elif game_state == 'gameover':
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 30),
                         fontsize=50, color="red")
        screen.draw.text(f"Score: {score}", center=(WIDTH//2, HEIGHT//2 + 10),
                         fontsize=40, color="white")
        screen.draw.text("Press SPACE to restart", center=(WIDTH//2, HEIGHT//2 + 60),
                         fontsize=30, color="yellow")
