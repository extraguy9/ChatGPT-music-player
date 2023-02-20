import pygame
import os
import tkinter as tk
from tkinter import filedialog

title_x = 10

# Set up the root window for the dialog
root = tk.Tk()
root.withdraw()

# Open a file dialog to get the folder path
mp3_folder = filedialog.askdirectory(title="Select MP3 folder")

# Initialize Pygame mixer
pygame.mixer.init()

# Set up the display
pygame.init()
screen = pygame.display.set_mode((400, 150))
pygame.display.set_caption("MP3 Player")

# Set up fonts and colors
font = pygame.font.SysFont("Arial", 20)
color = pygame.Color("white")
textcolor = pygame.Color("black")

# Get a list of all the MP3 files in the folder
mp3_files = [os.path.join(mp3_folder, f) for f in os.listdir(mp3_folder) if f.endswith(".mp3")]

# Load the first MP3 file in the list
current_mp3_index = 0
pygame.mixer.music.load(mp3_files[current_mp3_index])

#pausing 
paused_pos = 0
is_paused = False

# Create functions to change the current MP3 file
def next_mp3():
    global current_mp3_index
    current_mp3_index = (current_mp3_index + 1) % len(mp3_files)
    pygame.mixer.music.load(mp3_files[current_mp3_index])
    pygame.display.set_caption(os.path.splitext(os.path.basename(mp3_files[current_mp3_index]))[0])

def prev_mp3():
    global current_mp3_index
    current_mp3_index = (current_mp3_index - 1) % len(mp3_files)
    pygame.mixer.music.load(mp3_files[current_mp3_index])
    pygame.display.set_caption(os.path.splitext(os.path.basename(mp3_files[current_mp3_index]))[0])

# Create a function to play the current MP3 file
def play_music():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play()
    is_paused = False

# Create a function to pause the current MP3 file
def pause_music():
    global is_paused, paused_pos
    is_paused = True
    paused_pos = pygame.mixer.music.get_pos()
    pygame.mixer.music.pause()

# Create a function to skip the current MP3 file
def skip_music():
    global is_paused, paused_pos
    is_paused = False
    paused_pos = 0
    pygame.mixer.music.stop()

# set the background image
bg_texture = pygame.image.load("background.PNG")

# Create a function to display the current MP3 title scrolling in a box above the buttons
def display_title():
    title = font.render(os.path.basename(mp3_files[current_mp3_index]), True, textcolor)
    title_width = title.get_width()
    title_height = title.get_height()
    title_x = (screen.get_width() - title_width) / 2
    pygame.draw.rect(screen, color, (title_x - 10, 20, title_width + 20, title_height + 10))
    screen.blit(title, (title_x, 25))

# Set up the buttons
play_button = pygame.Rect(12, 102, 52, 32)
pause_button = pygame.Rect(72, 102, 52, 32)
skip_button = pygame.Rect(132, 102, 52, 32)
prev_button = pygame.Rect(200, 100, 50, 30)
next_button = pygame.Rect(260, 100, 50, 30)

bg_color = pygame.Color("black")

pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Run the main loop
running = True
while running:
    title_x -= .01
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if a button was clicked
            if play_button.collidepoint(event.pos):
                play_music()
            elif pause_button.collidepoint(event.pos):
                pause_music()
            elif skip_button.collidepoint(event.pos):
                skip_music()
            elif prev_button.collidepoint(event.pos):
                prev_mp3()
                play_music()
            elif next_button.collidepoint(event.pos):
                next_mp3()
                play_music()
        elif event.type == pygame.USEREVENT:
            # The end event was triggered, so play the next MP3 in the list
            next_mp3()
            play_music()    
    screen.blit(bg_texture, (0, 0))

    # Draw the buttons
    pygame.draw.rect(screen, color, play_button)
    pygame.draw.rect(screen, color, pause_button)
    pygame.draw.rect(screen, color, skip_button)
    pygame.draw.rect(screen, color, prev_button)
    pygame.draw.rect(screen, color, next_button)

        # Create a surface to display the mp3 title
    title_surf = font.render(os.path.basename(mp3_files[current_mp3_index]), True, textcolor)

    title_box = pygame.Surface((380, 30), pygame.SRCALPHA)
    title_box.fill((255, 255, 255, 128))

    # Blit the title onto the transparent box, adjusting the x-coordinate based on the title_x variable
    title_box.blit(title_surf, (title_x, 5))

    # If the text has scrolled out of the box, reset the position to the right side of the box
    if title_x < -title_surf.get_width():
        title_x = 380

    # Draw the title box onto the screen
    screen.blit(title_box, (10, 10))

    # Draw the button labels

    play_label = font.render("Play", True, textcolor)
    screen.blit(play_label, (play_button.x + 10, play_button.y + 5))
    pause_label = font.render("Pause", True, textcolor)
    screen.blit(pause_label, (pause_button.x + 5, pause_button.y + 5))
    skip_label = font.render("Skip", True, textcolor)
    screen.blit(skip_label, (skip_button.x + 10, skip_button.y + 5))
    prev_label = font.render("<<<", True, textcolor)
    screen.blit(prev_label, (prev_button.x + 10, prev_button.y + 5))
    next_label = font.render(">>>", True, textcolor)
    screen.blit(next_label, (next_button.x + 10, next_button.y + 5))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
