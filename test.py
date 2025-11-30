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
player_radius = 8  # not used for simple rectangle
player_effect = {"type": None, "timer": 0}  # blink effect

# --- Obstacles ---
obstacles = []  # [x, y, type]
obstacle_width = 30
obstacle_height = 30

# --- Game stats ---
score = 0
high_score = 0
lives = 3
max_lives = 5

# --- Difficulty ---
fall_speed = 5
spawn_rate = 30

# --- Game state ---
game_state = "start"
game_over_triggered = False
can_restart = False

# -------------------------
# Spawn obstacle
# -------------------------
def spawn_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    block_type = "green" if random.randint(1, 5) == 1 else "red"
    obstacles.append([x, 0, block_type])

# -------------------------
# Reset game
# -------------------------
def reset_game():
    global obstacles, score, lives, fall_speed, spawn_rate, player_x
    global player_effect, game_over_triggered, can_restart
    obstacles.clear()
    score = 0
    lives = 3
    fall_speed = 5
    spawn_rate = 30
    player_x = WIDTH // 2
    player_effect = {"type": None, "timer": 0}
    game_over_triggered = False
    can_restart = False
    music.stop()
    music.play("background")
    music.set_volume(0.5)

# -------------------------
# Enable restart
# -------------------------
def enable_restart():
    global can_restart
    can_restart = True

# -------------------------
# Collision check
# -------------------------
def rects_collide(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

# -------------------------
# Update function
# -------------------------
def update():
    global player_x, score, lives, fall_speed, spawn_rate, game_state
    global player_effect, game_over_triggered, high_score

    if game_state != "playing":
        return

    # Move player
    if keyboard.left and player_x > 0:
        player_x -= player_speed
    if keyboard.right and player_x < WIDTH - player_width:
        player_x += player_speed

    # Spawn obstacles
    if random.randint(1, spawn_rate) == 1:
        spawn_obstacle()

    # Move obstacles and check collisions
    for obs in obstacles[:]:
        obs[1] += fall_speed

        # Missed red obstacle
        if obs[1] > HEIGHT:
            if obs[2] == "red":
                score += 1
            obstacles.remove(obs)
            continue

        # Player collision
        player_rect = (player_x, player_y, player_width, player_height)
        obs_rect = (obs[0], obs[1], obstacle_width, obstacle_height)
        if rects_collide(player_rect, obs_rect):
            if obs[2] == "red":
                lives -= 1
                player_effect["type"] = "hit"
                player_effect["timer"] = 10
                if lives <= 0 and not game_over_triggered:
                    lives = 0
                    game_state = "gameover"
                    game_over_triggered = True
                    if score > high_score:
                        high_score = score
                    music.set_volume(0.2)
                    sounds.gameover.play()
                    clock.schedule_unique(enable_restart, 0.6)
            elif obs[2] == "green":
                lives = min(max_lives, lives + 1)
                player_effect["type"] = "heal"
                player_effect["timer"] = 10
            obstacles.remove(obs)

    # Difficulty scaling
    fall_speed = 5 + score // 10
    spawn_rate = max(10, 30 - score // 5)

# -------------------------
# Key press handler
# -------------------------
def on_key_down(key):
    global game_state
    if key == keys.SPACE:
        if game_state == "start":
            game_state = "playing"
            reset_game()
        elif game_state == "gameover" and can_restart:
            game_state = "playing"
            reset_game()

# -------------------------
# Draw function
# -------------------------
def draw():
    screen.clear()

    if game_state == "start":
        screen.draw.text("DODGE THE BLOCKS", center=(WIDTH//2, HEIGHT//2 - 30),
                         fontsize=50, color="white")
        screen.draw.text("Press SPACE to start", center=(WIDTH//2, HEIGHT//2 + 30),
                         fontsize=30, color="yellow")

    elif game_state == "playing":
        # Player blink effect
        if player_effect["timer"] > 0:
            color = "red" if player_effect["type"] == "hit" else "green"
            player_effect["timer"] -= 1
        else:
            color = "blue"
        screen.draw.filled_rect(Rect((player_x, player_y), (player_width, player_height)), color)

        # Draw obstacles
        for obs in obstacles:
            c = "red" if obs[2] == "red" else "green"
            screen.draw.filled_rect(Rect((obs[0], obs[1]), (obstacle_width, obstacle_height)), c)

        # Draw HUD
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"High Score: {high_score}", (10, 40), fontsize=25, color="yellow")
        screen.draw.text(f"Lives: {lives}", (10, 70), fontsize=25, color="red")

    elif game_state == "gameover":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 30),
                         fontsize=60, color="red")
        screen.draw.text(f"Score: {score}", center=(WIDTH//2, HEIGHT//2 + 20),
                         fontsize=40, color="white")
        screen.draw.text("Press SPACE to restart", center=(WIDTH//2, HEIGHT//2 + 80),
                         fontsize=30, color="yellow")
