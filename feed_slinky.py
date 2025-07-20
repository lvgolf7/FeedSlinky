import pygame
import random

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Examples")
pygame.display.set_icon(pygame.image.load("slinky.png"))
clock = pygame.time.Clock()
running = True

dt = 0
score = 0

pygame.mixer.music.load("bg.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

system_font = pygame.font.SysFont("impact", 40)
text = system_font.render("FEED SLINKY", True, "darkblue")
text_rect = text.get_rect()
text_rect.center = (WINDOW_WIDTH // 2, 30)
score_text = system_font.render(f"Score: {score}", True, "darkblue")
score_rect = score_text.get_rect()
score_rect.center = (WINDOW_WIDTH - 100, 30)


bone = pygame.image.load("bone.png")
bone_rect = bone.get_rect()
bone_rect.center = (WINDOW_WIDTH // 2, 400)
dog = pygame.image.load("slinky.png")
dog_rect = dog.get_rect()
dog_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("silver")

    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(dog, dog_rect)
    screen.blit(bone, bone_rect)
    pygame.draw.line(screen, "darkblue", (0, 60), (WINDOW_WIDTH, 60), 5)
    if score >= 10:
        text = system_font.render("YOU WIN!", True, "darkblue")
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        dog_rect.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        dog_rect.y += 300 * dt
    if keys[pygame.K_LEFT]:
        dog_rect.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        dog_rect.x += 300 * dt

    if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
        pos = pygame.mouse.get_pos()
        dog_rect.x = pos[0] - 37
        dog_rect.y = pos[1] - 37

    if dog_rect.left < 0:
        dog_rect.left = 0
    if dog_rect.right > WINDOW_WIDTH:
        dog_rect.right = WINDOW_WIDTH
    if dog_rect.top < 60:
        dog_rect.top = 60
    if dog_rect.bottom > WINDOW_HEIGHT:
        dog_rect.bottom = WINDOW_HEIGHT

    if dog_rect.colliderect(bone_rect):
        bone_rect.x = random.randint(0, WINDOW_WIDTH - bone_rect.width)
        bone_rect.y = random.randint(60, WINDOW_HEIGHT - bone_rect.height)
        pygame.mixer.Sound("bone.mp3").play()
        score += 1
        score_text = system_font.render(f"Score: {score}", True, "darkblue")

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Convert milliseconds to seconds


pygame.quit()
