import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Load background image
BACKGROUND_IMAGE = pygame.image.load("hangmanbg.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
LETTER_FONT = pygame.font.SysFont('arial', 30)
WORD_FONT = pygame.font.SysFont('arial', 50)
TITLE_FONT = pygame.font.SysFont('arial', 50)

# Game variables
BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50
BUTTON_GAP = 10
letters = []
startx = (WIDTH - (BUTTON_WIDTH + BUTTON_GAP) * 13) // 2
starty = 350
A = 65  # ASCII for 'A'

# Create buttons
for i in range(26):
    x = startx + (BUTTON_WIDTH + BUTTON_GAP) * (i % 13)
    y = starty + (i // 13) * (BUTTON_HEIGHT + BUTTON_GAP)
    letters.append([x, y, chr(A + i), True])  # letters are initially visible

# Word categories
categories = {
    "Linked List": ["NODE", "POINTER", "DATA", "SINGLY", "INSERT", "DELETE"],
    "Binary Tree": ["ROOT", "CHILD", "NODE", "INORDER", "POSTORDER", "PREORDER"]
}

chosen_category = "Linked List"  # Default category
guessed = []

# Game state
hangman_status = 0
current_player = 1  # 1 for Player 1, 2 for Player 2
word = random.choice(categories[chosen_category])  # Set initial word
player1_score = 0
player2_score = 0


def draw_hangman(stage):
    """Draw the hangman depending on the current stage."""
    base_x = 50
    pole_x = base_x + 75

    # Base stand
    pygame.draw.line(screen, BLACK, (base_x, 400), (base_x + 150, 400), 5)  # Base
    pygame.draw.line(screen, BLACK, (pole_x, 400), (pole_x, 100), 5)  # Vertical pole
    pygame.draw.line(screen, BLACK, (pole_x, 100), (pole_x + 100, 100), 5)  # Top pole
    pygame.draw.line(screen, BLACK, (pole_x + 100, 100), (pole_x + 100, 150), 5)  # Rope

    if stage > 0:
        pygame.draw.circle(screen, BLACK, (pole_x + 100, 175), 25, 5)  # Head
    if stage > 1:
        pygame.draw.line(screen, BLACK, (pole_x + 100, 200), (pole_x + 100, 300), 5)  # Body
    if stage > 2:
        pygame.draw.line(screen, BLACK, (pole_x + 100, 220), (pole_x + 75, 250), 5)  # Left Arm
    if stage > 3:
        pygame.draw.line(screen, BLACK, (pole_x + 100, 220), (pole_x + 125, 250), 5)  # Right Arm
    if stage > 4:
        pygame.draw.line(screen, BLACK, (pole_x + 100, 300), (pole_x + 75, 350), 5)  # Left Leg
    if stage > 5:
        pygame.draw.line(screen, BLACK, (pole_x + 100, 300), (pole_x + 125, 350), 5)  # Right Leg


def draw():
    """Draw the game elements on the screen."""
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Draw title
    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))

    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.rect(screen, GRAY, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(screen, BLACK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
            text = LETTER_FONT.render(ltr, True, BLACK)
            screen.blit(text, (x + BUTTON_WIDTH / 2 - text.get_width() / 2, y + BUTTON_HEIGHT / 2 - text.get_height() / 2))

    # Draw hangman
    draw_hangman(hangman_status)

    # Draw current player
    player_text = WORD_FONT.render(f"Player {current_player}'s Turn", True, BLACK)
    screen.blit(player_text, (WIDTH / 2 - player_text.get_width() / 2, 100))

    # Draw player scores
    player1_text = WORD_FONT.render(f"Player 1: {player1_score}", True, BLACK)
    screen.blit(player1_text, (50, 50))
    player2_text = WORD_FONT.render(f"Player 2: {player2_score}", True, BLACK)
    screen.blit(player2_text, (WIDTH - 200, 50))

    pygame.display.update()


def display_message(message):
    """Display a message in the center of the screen."""
    pygame.time.delay(1000)
    screen.fill((255, 182, 193))  # Light pink background
    text_color = (0, 182, 0) if message == "You WON!" else (255, 0, 0)  # Green for WIN, Red for LOSS
    text = WORD_FONT.render(message, True, text_color)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def switch_player():
    """Switch between players after each turn."""
    global current_player, word, guessed, hangman_status

    for letter in letters:
        letter[3] = True  # Make letters visible again

    current_player = 1 if current_player == 2 else 2
    word = random.choice(categories[chosen_category])  # Randomly choose a new word
    guessed = []
    hangman_status = 0


def category_menu():
    """Display the category selection menu."""
    global chosen_category
    menu_run = True
    while menu_run:
        screen.fill((173, 216, 230))  # Light blue background
        title_text = TITLE_FONT.render("Select Category", True, BLACK)
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 4))

        # Draw category buttons
        linked_list_rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 - 50, 300, 50)
        binary_tree_rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 + 50, 300, 50)

        pygame.draw.rect(screen, GRAY, linked_list_rect)
        pygame.draw.rect(screen, BLACK, linked_list_rect, 3)
        linked_list_text = LETTER_FONT.render("Linked List", True, BLACK)
        screen.blit(linked_list_text, (linked_list_rect.x + linked_list_rect.width / 2 - linked_list_text.get_width() / 2,
                                       linked_list_rect.y + linked_list_rect.height / 2 - linked_list_text.get_height() / 2))

        pygame.draw.rect(screen, GRAY, binary_tree_rect)
        pygame.draw.rect(screen, BLACK, binary_tree_rect, 3)
        binary_tree_text = LETTER_FONT.render("Binary Tree", True, BLACK)
        screen.blit(binary_tree_text, (binary_tree_rect.x + binary_tree_rect.width / 2 - binary_tree_text.get_width() / 2,
                                       binary_tree_rect.y + binary_tree_rect.height / 2 - binary_tree_text.get_height() / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if linked_list_rect.collidepoint(m_x, m_y):
                    chosen_category = "Linked List"
                    menu_run = False
                elif binary_tree_rect.collidepoint(m_x, m_y):
                    chosen_category = "Binary Tree"
                    menu_run = False


# Main loop
def main():
    global hangman_status, guessed, word, player1_score, player2_score

    run = True
    while run:
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        if x < m_x < x + BUTTON_WIDTH and y < m_y < y + BUTTON_HEIGHT:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            if current_player == 1:
                player1_score += 1
            else:
                player2_score += 1
            display_message(f"Player {current_player} WON!")
            switch_player()

        if hangman_status == 6:
            if current_player == 1:
                player2_score += 1
            else:
                player1_score += 1
            display_message(f"Player {current_player} LOST! The word was {word}")
            switch_player()


while True:
    category_menu()
    main()
