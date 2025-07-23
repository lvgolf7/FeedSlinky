import pygame
import random

pygame.init()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed Slinky")
pygame.display.set_icon(pygame.image.load("slinky.png"))
clock = pygame.time.Clock()


class Button:
    def __init__(
        self,
        surf,
        msg,
        coords,
        txt_color=(255, 255, 255),
        font="roboto.ttf",
    ):
        self.surf = surf
        self.msg = msg
        self.x, self.y = coords
        self.txt_color = txt_color
        self.font = font
        self.ft30 = pygame.freetype.Font(self.font, 30)
        self.ft34 = pygame.freetype.Font(self.font, 34)
        self.over = False
        self.button = self.ft30.render_to(
            self.surf,
            (self.x - 9 * len(self.msg), self.y - 21),
            self.msg,
            self.txt_color,
        )

    def update(self):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            self.over = True
        else:
            self.over = False
        if self.over and pygame.mouse.get_pressed()[0]:
            return True

    def draw(self):
        if self.over:
            self.button = self.ft34.render_to(
                self.surf,
                (self.x - 10 * len(self.msg), self.y - 22.5),
                self.msg,
                self.txt_color,
            )
        else:
            self.button = self.ft30.render_to(
                self.surf,
                (self.x - 9 * len(self.msg), self.y - 21),
                self.msg,
                self.txt_color,
            )


running = True
game_over = False

dt = 0
score = 0

pygame.mixer.music.load("bg.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

system_font = pygame.font.SysFont("roboto.ttf", 40)
title_text = system_font.render("FEED SLINKY", True, "indigo")
title_text_rect = title_text.get_rect()
title_text_rect.center = (WINDOW_WIDTH // 2, 30)
score_text = system_font.render(f"Score: {score}", True, "indigo")
score_rect = score_text.get_rect()
score_rect.center = (WINDOW_WIDTH - 100, 30)
game_over_text = system_font.render("YOU WIN!", True, "darkblue")
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)


bone = pygame.image.load("bone.png")
bone_rect = bone.get_rect()
bone_rect.center = (WINDOW_WIDTH // 2, 400)
dog = pygame.image.load("slinky.png")
dog_rect = dog.get_rect()
dog_rect.center = (WINDOW_WIDTH // 2 - 9, WINDOW_HEIGHT // 2)


exit_button = Button(
    screen, "Exit", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50), "darkblue"
)
reply_button = Button(
    screen, "Replay", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100), "darkblue"
)


while running:
    # check for exit events, either by clicking the close button or pressing escape
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Clear the screen and draw everything
    screen.fill("silver")
    screen.blit(title_text, title_text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(dog, dog_rect)
    if not game_over:
        screen.blit(bone, bone_rect)
    else:
        if exit_button.update():
            running = False
        if reply_button.update():
            score = 0
            score_text = system_font.render(f"Score: {score}", True, "indigo")
            game_over = False
            bone_rect.x = random.randint(0, WINDOW_WIDTH - bone_rect.width)
            bone_rect.y = random.randint(60, WINDOW_HEIGHT - bone_rect.height)
            pygame.mixer.music.play(-1)

    pygame.draw.line(screen, "indigo", (0, 60), (WINDOW_WIDTH, 60), 5)

    # check if the score is 10 or more
    if score >= 10:
        screen.blit(game_over_text, game_over_text_rect)
        game_over = True
        bone_rect.x = -100  # Move the bone off-screen
        pygame.mixer.music.stop()
        exit_button.draw()
        reply_button.draw()

    # Handle movement with arrow keys or mouse
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

    # Keep the dog within the window bounds
    if dog_rect.left < 0:
        dog_rect.left = 0
    if dog_rect.right > WINDOW_WIDTH:
        dog_rect.right = WINDOW_WIDTH
    if dog_rect.top < 60:
        dog_rect.top = 60
    if dog_rect.bottom > WINDOW_HEIGHT:
        dog_rect.bottom = WINDOW_HEIGHT

    # Check for collision with the bone
    if dog_rect.colliderect(bone_rect):
        bone_rect.x = random.randint(0, WINDOW_WIDTH - bone_rect.width)
        bone_rect.y = random.randint(60, WINDOW_HEIGHT - bone_rect.height)
        pygame.mixer.Sound("bone.mp3").play()
        score += 1
        score_text = system_font.render(f"Score: {score}", True, "indigo")

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Convert milliseconds to seconds


pygame.quit()
