import pygame
import sys
import random
from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import PowerUp

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load sounds
brick_hit_sound = pygame.mixer.Sound("assets/sounds/brick_hit.wav")
paddle_hit_sound = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
wall_hit_sound = pygame.mixer.Sound("assets/sounds/wall_hit.wav")
lose_life_sound = pygame.mixer.Sound("assets/sounds/lose_life.wav")
win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

# Game variables
lives = 3
score = 0
ball_attached = True
game_state = "MENU"  # MENU, PLAYING, GAME_OVER, WIN

paddle = Paddle(x=WIDTH//2 - 60, y=HEIGHT - 30, width=120, height=15, color=(255, 255, 255))
balls = [Ball(WIDTH//2, HEIGHT//2, 10, (255, 0, 0))]

powerups = []

def create_bricks():
    bricks = []
    rows = 5
    cols = 10
    brick_width = WIDTH // cols
    brick_height = 30
    for row in range(rows):
        for col in range(cols):
            x = col * brick_width
            y = row * brick_height + 50
            color = (200, 200 - row * 30, 255 - col * 20)
            points = (5 - row) * 10  # Top row gives more points
            bricks.append(Brick(x, y, brick_width, brick_height, color, points))
    return bricks

bricks = create_bricks()

def spawn_powerup(x, y):
    types = ["multi", "big", "life"]
    p_type = random.choice(types)
    powerups.append(PowerUp(x, y, 20, 20, p_type))

def reset_game():
    global lives, score, ball_attached, balls, paddle, bricks, powerups, game_state
    lives = 3
    score = 0
    ball_attached = True
    balls = [Ball(WIDTH//2, HEIGHT//2, 10, (255, 0, 0))]
    paddle = Paddle(x=WIDTH//2 - 60, y=HEIGHT - 30, width=120, height=15, color=(255, 255, 255))
    bricks = create_bricks()
    powerups = []
    game_state = "PLAYING"

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] and action:
            action()
    else:
        pygame.draw.rect(screen, color, rect)
    txt = font.render(text, True, (0, 0, 0))
    screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))

def start_game():
    global game_state
    game_state = "PLAYING"

# ===== GAME LOOP =====
while True:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ===== MENU =====
    if game_state == "MENU":
        title = font.render("CSC222 - Breakout by Group 18", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        draw_button("Start Game", WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50, (255,255,255), (200,200,200), start_game)

    elif game_state == "PLAYING":
        paddle.move(keys, WIDTH)

        if ball_attached:
            balls[0].x = paddle.rect.centerx
            balls[0].y = paddle.rect.top - balls[0].radius
        else:
           for ball in balls:
               ball.move()
               ball.bounce_wall(WIDTH, HEIGHT, wall_hit_sound)
               ball.bounce_paddle(paddle.rect, paddle_hit_sound)

        if keys[pygame.K_SPACE] and ball_attached:
            ball_attached = False

        # Remove balls that fell below screen
        balls = [b for b in balls if b.y - b.radius <= HEIGHT]

        if len(balls) == 0:
            lives -= 1
            lose_life_sound.play()
            ball_attached = True
            if lives <= 0:
                game_over_sound.play()
                game_state = "GAME_OVER"
            else:
                balls = [Ball(WIDTH//2, HEIGHT//2, 10, (255, 0, 0))]

        for ball in balls:
            for brick in bricks:
                if not brick.destroyed and brick.rect.collidepoint(ball.x, ball.y - ball.radius):
                    ball.dy *= -1
                    brick.destroyed = True
                    brick_hit_sound.play()
                    score += 10
                    if random.random() < 0.2:
                        spawn_powerup(brick.rect.x + brick.rect.width//2, brick.rect.y)

        # Powerup collisions
        for powerup in powerups:
            powerup.update()
            if powerup.rect.colliderect(paddle.rect):
               if powerup.type == "multi":
                   for _ in range(2):  # spawn 2 extra balls
                       new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10, 10, (255, 255, 0))
                       new_ball.dx = random.choice([-5, 5])
                       new_ball.dy = -5
                       balls.append(new_ball)
               elif powerup.type == "big":
                    paddle.rect.width = min(paddle.rect.width + 40, 200)
               elif powerup.type == "life":
                    lives += 1
               powerup.active = False

        powerups = [p for p in powerups if p.active]

        if all(brick.destroyed for brick in bricks):
            game_state = "WIN"
            win_sound.play()

        paddle.draw(screen)
        for ball in balls:
            ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))

    elif game_state == "GAME_OVER":
        over = font.render("GAME OVER", True, (255, 0, 0))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 60))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2))
        draw_button("Restart", WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, (255,255,255), (200,200,200), reset_game)

    elif game_state == "WIN":
        win_text = font.render("YOU WIN!", True, (0, 255, 0))
        final_score = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2))
        draw_button("Play Again", WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, (255,255,255), (200,200,200), reset_game)

    pygame.display.flip()
    clock.tick(60)
