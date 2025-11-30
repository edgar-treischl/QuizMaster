import pgzrun
import random

WIDTH = 400
HEIGHT = 600

player_width = 50
player_height = 30
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed = 5

lives = 3
max_lives = 5
player_effect = {"type": None, "timer": 0}

obstacles = []
obstacle_width = 30
obstacle_height = 30
fall_speed = 5
spawn_rate = 30

game_state = "start"

def spawn_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    color = "red" if random.randint(1, 2) == 1 else "green"
    obstacles.append([x, 0, color])

def draw():
    screen.clear()
    
    if game_state == "start":
        screen.draw.text("DODGE THE BLOCKS", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="white")
        screen.draw.text("Press SPACE to start", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="yellow")
    elif game_state == "playing":
        if player_effect["timer"] > 0:
            # Color the hit
            color = "red" if player_effect["type"] == "hit" else "green"
            player_effect["timer"] -= 1
        else:
            color = "blue"
        screen.draw.filled_rect(Rect((player_x, player_y), (player_width, player_height)), color)
        
        for obs in obstacles:
            screen.draw.filled_rect(Rect((obs[0], obs[1]), (obstacle_width, obstacle_height)), obs[2])
        
        screen.draw.text(f"Lives: {lives}", (10, 10), fontsize=30, color="red")

def update():
    global player_x, lives, player_effect, game_state
    
    if game_state != "playing":
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
            obstacles.remove(obs)
            continue
        
        # --- Collision detection ---
        # We check if the player rectangle overlaps with the obstacle rectangle.
        # player_rect = (player_x, player_y, player_width, player_height)
        # obs_rect = (obs_x, obs_y, obstacle_width, obstacle_height)
        #
        # Step by step:
        # 1. player_rect[0] < obs_rect[0] + obs_rect[2]
        #    → Player's left side is left of obstacle's right side
        # 2. player_rect[0] + player_rect[2] > obs_rect[0]
        #    → Player's right side is right of obstacle's left side
        # 3. player_rect[1] < obs_rect[1] + obs_rect[3]
        #    → Player's top is above obstacle's bottom
        # 4. player_rect[1] + player_rect[3] > obs_rect[1]
        #    → Player's bottom is below obstacle's top
        #
        # If all 4 are true, rectangles overlap → collision detected.
        # Example values:
        # Player: x=100, y=500, w=50, h=30 → left=100, right=150, top=500, bottom=530
        # Obstacle: x=120, y=520, w=30, h=30 → left=120, right=150, top=520, bottom=550
        # Overlap occurs: horizontal 120–150, vertical 520–530
        player_rect = (player_x, player_y, player_width, player_height)
        obs_rect = (obs[0], obs[1], obstacle_width, obstacle_height)

        if (player_rect[0] < obs_rect[0] + obs_rect[2] and
            player_rect[0] + player_rect[2] > obs_rect[0] and
            player_rect[1] < obs_rect[1] + obs_rect[3] and
            player_rect[1] + player_rect[3] > obs_rect[1]):
            
            # Red obstacle → player takes damage
            if obs[2] == "red":
                lives -= 1
                player_effect["type"] = "hit"
                player_effect["timer"] = 10
                if lives <= 0:
                    lives = 0
                    game_state = "gameover"
            
            # Green obstacle → player heals
            elif obs[2] == "green":
                lives = min(max_lives, lives + 1)
                player_effect["type"] = "heal"
                player_effect["timer"] = 10
            
            obstacles.remove(obs)

def on_key_down(key):
    global game_state, lives
    if key == keys.SPACE:
        if game_state == "start":
            game_state = "playing"
        elif game_state == "gameover":
            lives = 3
            obstacles.clear()
            player_effect["type"] = None
            player_effect["timer"] = 0
            game_state = "playing"

pgzrun.go()
