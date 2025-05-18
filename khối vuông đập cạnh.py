import pygame
import random
import math
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Game: Full Logic")

# Kích thước vùng chơi (2/3 cửa sổ, nằm giữa)
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = int(SCREEN_WIDTH * 2 / 3), int(SCREEN_HEIGHT * 2 / 3)
PLAY_AREA_X, PLAY_AREA_Y = (SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2, (SCREEN_HEIGHT - PLAY_AREA_HEIGHT) // 2

# Màu sắc
WHITE = (255, 255, 255)
YELLOW = (200, 200, 100)
BROWN = (150, 75, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Thông số khối
INITIAL_BLOCK_SIZE = 50
INITIAL_SPEED = 5
HEALTH = 10

# Hàm tạo vị trí ngẫu nhiên đảm bảo hai khối không trùng nhau
def generate_random_position():
    while True:
        x1 = random.randint(PLAY_AREA_X, PLAY_AREA_X + PLAY_AREA_WIDTH - INITIAL_BLOCK_SIZE)
        y1 = random.randint(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_HEIGHT - INITIAL_BLOCK_SIZE)
        x2 = random.randint(PLAY_AREA_X, PLAY_AREA_X + PLAY_AREA_WIDTH - INITIAL_BLOCK_SIZE)
        y2 = random.randint(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_HEIGHT - INITIAL_BLOCK_SIZE)
        block1 = pygame.Rect(x1, y1, INITIAL_BLOCK_SIZE, INITIAL_BLOCK_SIZE)
        block2 = pygame.Rect(x2, y2, INITIAL_BLOCK_SIZE, INITIAL_BLOCK_SIZE)
        if not block1.colliderect(block2):  # Đảm bảo không trùng nhau
            return block1, block2

block1, block2 = generate_random_position()

# Hàm tạo vận tốc với góc ±45 độ
def generate_fixed_velocity():
    angle = random.choice([45, 135, 225, 315])
    speed_x = INITIAL_SPEED * math.cos(math.radians(angle))
    speed_y = INITIAL_SPEED * math.sin(math.radians(angle))
    return [speed_x, speed_y]

block1_velocity = generate_fixed_velocity()
block2_velocity = generate_fixed_velocity()

block1_health = HEALTH
block2_health = HEALTH

font = pygame.font.SysFont(None, 30)

# Thời gian trò chơi
GAME_TIME = 60  # Giới hạn thời gian (giây)
start_time = time.time()

# Hàm kiểm tra và xử lý va chạm giữa hai khối
def handle_collision(block1, block1_velocity, block2, block2_velocity):
    if block1.colliderect(block2):  # Nếu hai khối chạm nhau
        # Bật khối 1 góc 90 độ
        block1_velocity[0], block1_velocity[1] = -block1_velocity[1], block1_velocity[0]
        # Bật khối 2 góc 90 độ
        block2_velocity[0], block2_velocity[1] = -block2_velocity[1], block2_velocity[0]

# Hàm kiểm tra va chạm và mất máu
def check_and_reduce_health():
    global block1_health, block2_health
    if block1.colliderect(block2):
        if (
            block2.right >= block1.left and block2.left < block1.centerx
        ) or (
            block2.left <= block1.right and block2.right > block1.centerx
        ):  # Khối 2 chạm cạnh bên của khối 1
            block2_health -= 1
        elif (
            block1.top <= block2.bottom and block1.bottom > block2.centery
        ) or (
            block1.bottom >= block2.top and block1.top < block2.centery
        ):  # Khối 1 chạm cạnh trên/dưới của khối 2
            block1_health -= 1

# Game loop
running = True
winner = None
while running:
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cập nhật thời gian
    elapsed_time = time.time() - start_time
    if elapsed_time >= GAME_TIME:  # Kết thúc khi hết thời gian
        winner = "Khối 1" if block1_health > block2_health else "Khối 2"
        break

    # Di chuyển khối
    block1.move_ip(block1_velocity)
    block2.move_ip(block2_velocity)

    # Xử lý va chạm với cạnh vùng chơi
    for block, velocity in [(block1, block1_velocity), (block2, block2_velocity)]:
        if block.left < PLAY_AREA_X or block.right > PLAY_AREA_X + PLAY_AREA_WIDTH:
            velocity[0] = -velocity[0]
        if block.top < PLAY_AREA_Y or block.bottom > PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            velocity[1] = -velocity[1]

    # Xử lý va chạm giữa hai khối và bật ra góc 90°
    handle_collision(block1, block1_velocity, block2, block2_velocity)

    # Xử lý mất máu khi va chạm
    check_and_reduce_health()

    # Kết thúc trò chơi nếu một khối hết máu
    if block1_health <= 0 or block2_health <= 0:
        winner = "Khối 1" if block1_health > 0 else "Khối 2"
        break

    # Vẽ màn hình
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT), 5)

    # Vẽ khối
    pygame.draw.rect(screen, YELLOW, block1)
    pygame.draw.rect(screen, BROWN, block2)

    # Vẽ thanh máu
    for i in range(block1_health):
        pygame.draw.rect(screen, GREEN, (10 + i * 20, SCREEN_HEIGHT - 30, 18, 18))
    for i in range(block2_health):
        pygame.draw.rect(screen, GREEN, (10 + i * 20, SCREEN_HEIGHT - 60, 18, 18))

    # Hiển thị thời gian
    time_text = font.render(f"Time: {int(GAME_TIME - elapsed_time)}", True, WHITE)
    screen.blit(time_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Hiển thị người thắng cuộc
while True:
    screen.fill(BLACK)
    result_text = font.render(f"Game Over! {winner} Wins!", True, WHITE)
    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
