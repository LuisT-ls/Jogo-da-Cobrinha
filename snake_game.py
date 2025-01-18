import pygame
import random
import time
import json
import os
from enum import Enum

# Inicializar o Pygame
pygame.init()
pygame.mixer.init()  # Inicializar o mixer para sons

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Estados do jogo
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Snake Game")
clock = pygame.time.Clock()


# Carregar ou criar arquivo de high score
def load_high_score():
    try:
        with open("high_score.json", "r") as f:
            return json.load(f)["high_score"]
    except:
        return 0


def save_high_score(score):
    with open("high_score.json", "w") as f:
        json.dump({"high_score": score}, f)


# Classe para power-ups
class PowerUp:
    def __init__(self):
        self.reset()

    def reset(self):
        self.type = random.choice(["speed", "slow", "double_points"])
        self.pos = [
            random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE,
        ]
        self.active = False
        self.duration = 5  # duração em segundos
        self.start_time = 0

    def spawn(self):
        self.active = True
        self.reset()

    def apply_effect(self, game):
        self.start_time = time.time()
        if self.type == "speed":
            game.speed += 5
        elif self.type == "slow":
            game.speed = max(5, game.speed - 3)
        # double_points não precisa de efeito imediato

    def check_duration(self, game):
        if time.time() - self.start_time > self.duration:
            if self.type == "speed":
                game.speed = max(10, game.speed - 5)
            elif self.type == "slow":
                game.speed = min(15, game.speed + 3)
            return True
        return False


class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.high_score = load_high_score()
        self.power_up = PowerUp()  # Movido para antes de reset_game
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [[100, 50]]
        self.snake_dir = "RIGHT"
        self.change_to = self.snake_dir
        self.food_pos = self.generate_food_position()
        self.score = 0
        self.speed = 10
        self.power_up.reset()

    def generate_food_position(self):
        while True:
            pos = [
                random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE,
            ]
            if pos not in self.snake_pos:
                return pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING

                if self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.PLAYING

                elif self.state == GameState.PLAYING:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake_dir != "DOWN":
                        self.change_to = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake_dir != "UP":
                        self.change_to = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake_dir != "RIGHT":
                        self.change_to = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake_dir != "LEFT":
                        self.change_to = "RIGHT"

                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

        return True

    def update(self):
        if self.state != GameState.PLAYING:
            return True

        # Atualizar direção
        self.snake_dir = self.change_to

        # Calcular nova posição da cabeça
        head_x, head_y = self.snake_pos[0]
        if self.snake_dir == "UP":
            head_y -= BLOCK_SIZE
        elif self.snake_dir == "DOWN":
            head_y += BLOCK_SIZE
        elif self.snake_dir == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.snake_dir == "RIGHT":
            head_x += BLOCK_SIZE

        # Verificar colisões com as bordas
        if head_x < 0:
            head_x = WIDTH - BLOCK_SIZE
        elif head_x >= WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = HEIGHT - BLOCK_SIZE
        elif head_y >= HEIGHT:
            head_y = 0

        # Inserir nova posição da cabeça
        self.snake_pos.insert(0, [head_x, head_y])

        # Verificar colisão com comida
        if self.snake_pos[0] == self.food_pos:
            points = (
                2
                if self.power_up.type == "double_points" and self.power_up.active
                else 1
            )
            self.score += points
            self.food_pos = self.generate_food_position()

            # 20% de chance de spawnar power-up
            if random.random() < 0.2:
                self.power_up.spawn()
        else:
            self.snake_pos.pop()

        # Verificar colisão com power-up
        if self.power_up.active and self.snake_pos[0] == self.power_up.pos:
            self.power_up.apply_effect(self)
            self.power_up.active = False

        # Verificar duração do power-up
        if self.power_up.start_time > 0:
            if self.power_up.check_duration(self):
                self.power_up.start_time = 0

        # Verificar colisão com o próprio corpo
        for block in self.snake_pos[1:]:
            if self.snake_pos[0] == block:
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_high_score(self.high_score)
                self.state = GameState.GAME_OVER
                return True

        return True

    def draw(self):
        screen.fill(BLACK)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self.draw_game()
            if self.state == GameState.PAUSED:
                self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        font = pygame.font.SysFont("arial", 64)
        title = font.render("Super Snake Game", True, GREEN)
        screen.blit(title, [WIDTH // 2 - title.get_width() // 2, HEIGHT // 4])

        font = pygame.font.SysFont("arial", 32)
        start = font.render("Pressione ENTER para começar", True, WHITE)
        screen.blit(start, [WIDTH // 2 - start.get_width() // 2, HEIGHT // 2])

        high_score = font.render(f"High Score: {self.high_score}", True, YELLOW)
        screen.blit(
            high_score, [WIDTH // 2 - high_score.get_width() // 2, HEIGHT * 3 // 4]
        )

    def draw_game(self):
        # Desenhar cobra
        for i, pos in enumerate(self.snake_pos):
            color = GREEN if i == 0 else (0, 200, 0)  # Cabeça mais clara
            pygame.draw.rect(
                screen, color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
            )

            # Desenhar olhos na cabeça
            if i == 0:
                eye_size = 4
                if self.snake_dir in ["LEFT", "RIGHT"]:
                    pygame.draw.circle(
                        screen, WHITE, (pos[0] + BLOCK_SIZE // 2, pos[1] + 5), eye_size
                    )
                    pygame.draw.circle(
                        screen,
                        WHITE,
                        (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE - 5),
                        eye_size,
                    )
                else:
                    pygame.draw.circle(
                        screen, WHITE, (pos[0] + 5, pos[1] + BLOCK_SIZE // 2), eye_size
                    )
                    pygame.draw.circle(
                        screen,
                        WHITE,
                        (pos[0] + BLOCK_SIZE - 5, pos[1] + BLOCK_SIZE // 2),
                        eye_size,
                    )

        # Desenhar comida
        pygame.draw.rect(
            screen,
            RED,
            pygame.Rect(self.food_pos[0], self.food_pos[1], BLOCK_SIZE, BLOCK_SIZE),
        )

        # Desenhar power-up se ativo
        if self.power_up.active:
            color = (
                BLUE
                if self.power_up.type == "speed"
                else YELLOW if self.power_up.type == "slow" else RED
            )
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    self.power_up.pos[0], self.power_up.pos[1], BLOCK_SIZE, BLOCK_SIZE
                ),
            )

        # Exibir pontuação
        font = pygame.font.SysFont("arial", 20)
        score_text = font.render(
            f"Score: {self.score} | High Score: {self.high_score} | Speed: {self.speed}",
            True,
            WHITE,
        )
        screen.blit(score_text, [10, 10])

        # Exibir power-up ativo
        if self.power_up.start_time > 0:
            time_left = max(
                0, self.power_up.duration - (time.time() - self.power_up.start_time)
            )
            power_text = font.render(
                f"Power-up: {self.power_up.type.upper()} - {time_left:.1f}s",
                True,
                WHITE,
            )
            screen.blit(power_text, [10, 40])

    def draw_pause_screen(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0, 0))

        font = pygame.font.SysFont("arial", 64)
        pause_text = font.render("PAUSADO", True, WHITE)
        screen.blit(pause_text, [WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2])

    def draw_game_over(self):
        font = pygame.font.SysFont("arial", 64)
        game_over = font.render("Game Over", True, RED)
        screen.blit(game_over, [WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3])

        font = pygame.font.SysFont("arial", 32)
        score = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score, [WIDTH // 2 - score.get_width() // 2, HEIGHT // 2])

        font = pygame.font.SysFont("arial", 24)
        restart = font.render(
            "Pressione ENTER para jogar novamente ou ESC para o menu", True, WHITE
        )
        screen.blit(restart, [WIDTH // 2 - restart.get_width() // 2, HEIGHT * 2 // 3])


def main():
    game = Game()
    running = True

    while running:
        running = game.handle_input()
        if running:
            running = game.update()
            game.draw()
            clock.tick(game.speed)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
