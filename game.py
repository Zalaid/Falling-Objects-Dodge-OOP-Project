import pygame
import random
import sys

pygame.init()

# Set up the game window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dodge the Raindrops")

# Load images with appropriate dimensions
player_img = pygame.image.load("player.png")
player_width = 50
player_height = 50
player_img = pygame.transform.scale(player_img, (player_width, player_height))

raindrop_img1 = pygame.image.load("obj1.png")
raindrop_width = 30
raindrop_height = 30
raindrop_img1 = pygame.transform.scale(raindrop_img1, (raindrop_width, raindrop_height))

raindrop_img2 = pygame.image.load("obj2.png")
raindrop_img2 = pygame.transform.scale(raindrop_img2, (raindrop_width, raindrop_height))

raindrop_img3 = pygame.image.load("obj3.png")
raindrop_img3 = pygame.transform.scale(raindrop_img3, (raindrop_width, raindrop_height))

raindrop_img4 = pygame.image.load("obj4.png")
raindrop_img4 = pygame.transform.scale(raindrop_img4, (raindrop_width, raindrop_height))

# Load sound effects
collision_sound = pygame.mixer.Sound("collision.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

# Define falling object class
class Raindrop(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
            self.speed_y = random.randint(3, 7)

def reset_game():
    global score, game_over
    score = 0  # Reset score to 0
    game_over = False  # Reset game over flag

# Create sprite groups
all_sprites = pygame.sprite.Group()
raindrops = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game variables
score = 10  # Initial score
font = pygame.font.Font(None, 36)
game_over = False

# Main game loop
while True:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Generate falling objects
        if len(raindrops) < 10:
            random_raindrop_img = random.choice([raindrop_img1, raindrop_img2, raindrop_img3, raindrop_img4])
            new_raindrop = Raindrop(random_raindrop_img)
            raindrops.add(new_raindrop)
            all_sprites.add(new_raindrop)

        # Update sprites
        all_sprites.update()

        # Check for collisions
        collisions = pygame.sprite.spritecollide(player, raindrops, True)
        if collisions:
            collision_sound.play()
            score -= 1  # Subtract 1 from score for each collision

        # Draw sprites
        all_sprites.draw(window)

        # Draw score
        score_text = font.render("Score: " + str(score), True, RED)
        window.blit(score_text, (10, 10))

        # Check for game over
        if score <= 0:
            game_over = True
            game_over_sound.play()

    else:
        # Display game over message
        game_over_text = font.render("Game Over! Final Score: " + str(score), True, RED)
        window.blit(game_over_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))
        reset_game()  # Reset game variables

    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Limit frame rate
