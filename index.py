import pygame
import random
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("AIMLABS")

def start_game(level):
    root.withdraw()  
    score = game(level)
    messagebox.showinfo("Game Over", f"Your score: {score}%")

def game(level):
    pygame.init()
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    WIDTH,HEIGHT = 1000,800
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("AIMLAB")


    background_image = pygame.image.load('bg2.jpg').convert()
    background_image = pygame.transform.scale(background_image,(WIDTH,HEIGHT))

    agent_image = pygame.image.load('target.png').convert_alpha()
    agent_image = pygame.transform.scale(agent_image,(100,100))

    class Target(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = agent_image
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))

    score = 0
    total_clicks = 0

    clock = pygame.time.Clock()

    all_targets = pygame.sprite.Group()
    target_timer = 0

    if level == "beginner":
        target_interval = 1000
    elif level == "intermediate":
        target_interval = 800

    game_duration = 40000

    start_time = pygame.time.get_ticks()

    running=True
    while running:
        screen.blit(background_image,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                total_clicks += 1
                pos = pygame.mouse.get_pos()
                for target in all_targets:
                    if target.rect.collidepoint(pos):
                        score += 1
                        target.kill()

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= game_duration:
            running = False

        if current_time - target_timer > target_interval:
            all_targets.empty()
            all_targets.add(Target())
            target_timer = current_time

        all_targets.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        text = font.render(f"Total Clicks: {total_clicks}", True, WHITE)
        screen.blit(text, (10, 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return round(score/total_clicks*100,2)

label = tk.Label(root,text = "Select Level: ")
label.pack()

var = tk.StringVar(root)
beginner_button = tk.Radiobutton(root, text="Beginner", variable=var, value="beginner")
beginner_button.pack()

intermediate_button = tk.Radiobutton(root, text="Intermediate", variable=var, value="intermediate")
intermediate_button.pack()

start_button = tk.Button(root, text="Start", command=lambda: start_game(var.get()))
start_button.pack()




root.mainloop()