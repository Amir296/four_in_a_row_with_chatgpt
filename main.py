import logging

import pygame
import random


def check_win(player, board):
    # Check for horizontal win
    for row in range(6):
        for col in range(4):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                print('option1')
                return True
    # Check for vertical win
    for row in range(3):
        for col in range(7):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                print('option2')
                return True
    # Check for diagonal win (left to right)
    for row in range(3):
        for col in range(4):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                print('option3')
                return True
    # Check for diagonal win (right to left)
    for row in range(3):
        for col in range(3, 7):
            if board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
                print('option4')
                return True
    return False


def check_draw(board):
    for row in range(6):
        for col in range(7):
            if board[row][col] == 0:
                return False


def is_terminal_state(board):
    # check for a win in rows
    for row in range(6):
        for col in range(4):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != 0:
                return board[row][col]

    # check for a win in columns
    for row in range(3):
        for col in range(7):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != 0:
                return board[row][col]

    # check for a win in diagonal
    for row in range(3):
        for col in range(4):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != 0:
                return board[row][col]

    for row in range(3):
        for col in range(4):
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col] != 0:
                return board[row][col + 3]

    # check for draw
    for row in range(6):
        for col in range(7):
            if board[row][col] == 0:
                return None

    return 0

def evaluate_board(board):
    # Check for a win by the maximizing player
    if check_for_win(board, 1):
        return float('inf')

    # Check for a win by the minimizing player
    if check_for_win(board, 2):
        return -float('inf')

    # Check for a draw
    if check_for_draw(board):
        return 0

    # Evaluate the board based on a heuristic
    return evaluate_heuristic(board)

def check_for_win(board, player):
    # Check rows
    for i in range(6):
        for j in range(4):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True

    # Check columns
    for i in range(3):
        for j in range(7):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True

    # Check diagonals
    for i in range(3):
        for j in range(4):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                return True
            if board[i][j+3] == player and board[i+1][j+2] == player and board[i+2][j+1] == player and board[i+3][j] == player:
                return True
    return False

def check_for_draw(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                return False
    return True

def evaluate_heuristic(board):
    # Implement a heuristic to evaluate the board
    # For example, you can count the number of possible winning positions for each player and return the difference
    player1_pos = 0
    player2_pos = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                player1_pos += check_neighbour(board,i,j,1)
                player2_pos += check_neighbour(board,i,j,2)
    return player1_pos - player2_pos

def check_neighbour(board,i,j,player):
    count = 0
    if i>0 and board[i-1][j] == player:
        count +=1
    if i<5 and board[i+1][j] == player:
        count +=1
    if j>0 and board[i][j-1] == player:
        count +=1
    if j<6 and board[i][j+1] == player:
        count +=1
    return count

def get_possible_moves(board):
    possible_moves = []
    for j in range(7):
        for i in range(6):
            if board[i][j] == 0:
                possible_moves.append((i, j))
                break
    return possible_moves

def game_over_f(board):
    # check for a win
    if check_for_win(board, 1) or check_for_win(board, 2):
        return True

    # check for a draw
    if check_for_draw(board):
        return True

    return False

def minimax(board, depth, isMaximizing):
    if depth == 0 or game_over_f(board):
        return evaluate_board(board), None
    bestMove = None
    bestValue = -float('inf') if isMaximizing else float('inf')
    for move in get_possible_moves(board):
        board[move[0]][move[1]] = 1 if isMaximizing else 2
        value, move1 = minimax(board, depth - 1, not isMaximizing)
        if (isMaximizing and value > bestValue) or (not isMaximizing and value < bestValue):
            bestValue = value
            bestMove = move[1]
        board[move[0]][move[1]] = 0
    return bestValue, bestMove

def agent_play(board):
    available_columns = [col for col in range(7) if board[0][col] == 0]
    if available_columns:
        #col = random.choice(available_columns)
        bestValue, col = minimax(board=board, depth=5, isMaximizing=False)
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                board[row][col] = 2
                break
        return True
    return False


# Initialize pygame and create window
pygame.init()
width = 700
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)

# Define colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


# Create a 2D list to represent the game board
board = [[0 for x in range(7)] for y in range(6)]

# Initialize game variables
player = 1
game_over = False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if player == 2:
            # Agent's turn
            agent_play(board)
            player = 1

        # Handle mouse clicks on the game board
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the column that was clicked
            pos = pygame.mouse.get_pos()
            col = pos[0] // 100

            # Place the piece in the bottom-most empty cell of the column
            for row in range(5, -1, -1):
                if board[row][col] == 0:
                    board[row][col] = player
                    break

            # Check for a win or draw
            if check_win(player, board):
                print("Player", player, "wins!")
                game_over = True
            elif check_draw(board):
                print("It's a draw!")
                game_over = True

            # Switch to the other player
            if player == 1:
                player = 2


    # Draw the game board
    for row in range(6):
        for col in range(7):
            pygame.draw.rect(screen, BLUE, (col * 100, row * 100, 100, 100))
            pygame.draw.circle(screen, BLACK, (col * 100 + 50, row * 100 + 50), 45)

            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * 100 + 50, row * 100 + 50), 45)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * 100 + 50, row * 100 + 50), 45)

    # Update the screen
    pygame.display.flip()

# Close the window and quit pygame
pygame.image.save(screen, "screenshot.png")
pygame.quit()



