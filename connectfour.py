import numpy as np
import math
import random
import pygame
import sys

#####################  VARIABLES  #######################


wht_bg =(255,255,255)

blue_piece = (0,0,255)
green_piece = (255,255,0)

grid_fg = (0,255,255)

rows = 6
columns = 7

win_len = 4
box_size = 50
win_width = columns * box_size
win_height = (rows+1) * box_size
win_size = (win_width, win_height)

disk_rad = int(box_size/2 - 5)

player = 0
minimax_ai = 1

empty = 0
player_disk = 1
minimax_disk = 2

############################  END VARIABLES  ##########################


def create_game_board():
    '''
    ##description::
    Creates the command line version of the board filled with zeroes using numpy

    ##return::
    Returns the game board as an array of zeroes
    '''
    game_board = np.zeros((rows, columns))
    return game_board


def pygame_board_create(game_board):
    '''
    ##description::
    Draws the pygame board to the gui screen window.

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    '''
    for j in range(columns):
        for i in range(rows):
            pygame.draw.rect(pygame_win, grid_fg, (j*box_size, i*box_size+box_size, box_size, box_size))
            pygame.draw.circle(pygame_win, wht_bg, (int(j*box_size+box_size/2), int(i*box_size+box_size+box_size/2)), disk_rad)
            
    for j in range(columns):
        for i in range(rows):		
            if game_board[i][j] == player_disk:
                pygame.draw.circle(pygame_win, blue_piece, (int(j*box_size+box_size/2), win_height-int(i*box_size+box_size/2)), disk_rad)
            elif game_board[i][j] == minimax_disk: 
                pygame.draw.circle(pygame_win, green_piece, (int(j*box_size+box_size/2), win_height-int(i*box_size+box_size/2)), disk_rad)
            
    pygame.display.update()


def display_board(game_board):
    '''
    ##description::
    This will print the numpy board of zeroes to the command window.

    #args::
    game_board : create_game_board() ## a board of zeroes created
    '''
    print(np.flip(game_board, 0))


def place_disk(game_board, row, col, disk):
    '''
    ##description::
    Places a disk at the location row, col on the game_board. 
    The disk that is placed is for either the player or the minimax AI based on the value of disk.

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    row : int (0, 6) the row on the game_board.
    col : int (0, 7) the column on the game_board.
    disk: int (0 or 1) ## player_disk or minimax_disk
    '''

    game_board[row][col] = disk


def valid_move(game_board, col):
    '''
    ##description::
    Returns True if there is no piece (i.e. a 0) at the location in the top row of the passed column.

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    col : int (0, 7) the column on the game_board.

    ##return::
    Returns a True value if the column is not full (i.e. a 0).
    Returns a False value if the column is full (i.e. a 1, or 2).
    '''
    return game_board[rows-1][col] == 0


def available_row(game_board, col):
    '''
    ##description::
    Determines the next available row for the specified column on the game_board.

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    col : int (0, 7) the column on the game_board.

    ##return::
    Returns an int (0, 6) for the highest available row in the column.

    '''
    for i in range(rows):
        if game_board[i][col] == 0:
            return i


def wind_eval(wind, disk):
    tally = 0
    disk_posses = player
    if disk == player:
        disk_posses = minimax_ai

    if wind.count(disk) == 4:
        tally += 100
    elif wind.count(disk) == 3 and wind.count(empty) == 1:
        tally += 5
    elif wind.count(disk) == 2 and wind.count(empty) == 2:
        tally += 2

    if wind.count(disk_posses) == 3 and wind.count(empty) == 1:
        tally -= 4

    return tally


def get_win(game_board, disk):
    #horizontal
    for j in range(columns-3):
        for i in range(rows):
            if game_board[i][j] == disk and game_board[i][j+1] == disk and game_board[i][j+2] == disk and game_board[i][j+3] == disk:
                return True
                   
    #negative diagonal
    for j in range(columns-3):
        for i in range(3, rows):
            if game_board[i][j] == disk and game_board[i-1][j+1] == disk and game_board[i-2][j+2] == disk and game_board[i-3][j+3] == disk:
                return True
    
    #vertical
    for j in range(columns):
        for i in range(rows-3):
            if game_board[i][j] == disk and game_board[i+1][j] == disk and game_board[i+2][j] == disk and game_board[i+3][j] == disk:
                return True

    #positive diagonal
    for j in range(columns-3):
        for i in range(rows-3):
            if game_board[i][j] == disk and game_board[i+1][j+1] == disk and game_board[i+2][j+2] == disk and game_board[i+3][j+3] == disk:
                return True


def pos_value(game_board, disk):
    '''
    ##description::
    Tally the value of each position scoring the value for vertical, horizontal, and both diagonal 
    slopes away from a specific location on the board. 

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    disk: int (0 or 1) ## player_disk or minimax_disk

    ##return::
    A tally of the value of a position
    '''
    tally = 0

	#tally mid
    middle_arr = [int(x) for x in list(game_board[:, columns//2])]
    middle_cnt = middle_arr.count(disk)
    tally += middle_cnt * 3

	#tally horizontal
    for i in range(rows):
        row_arr = [int(x) for x in list(game_board[i,:])]
        for j in range(columns-3):
            wind = row_arr[j:j+win_len]
            tally += wind_eval(wind, disk)

    #tally negative diagonal
    for i in range(rows-3):
        for j in range(columns-3):
            wind = [game_board[i+3-x][j+x] for x in range(win_len)]
            tally += wind_eval(wind, disk)

	#tally vertical
    for i in range(columns):
        col_arr = [int(x) for x in list(game_board[:,i])]
        for j in range(rows-3):
            wind = col_arr[j:j+win_len]
            tally += wind_eval(wind, disk)

	#tally positive diagonal
    for i in range(rows-3):
        for j in range(columns-3):
            wind = [game_board[i+x][j+x] for x in range(win_len)]
            tally += wind_eval(wind, disk)

    return tally


def get_is_term(game_board):
    return get_win(game_board, player_disk) or get_win(game_board, minimax_disk) or len(get_is_valid(game_board)) == 0


def get_is_valid(game_board):
    valid_loc = []
    for col in range(columns):
        if valid_move(game_board, col):
            valid_loc.append(col)
    return valid_loc

'''def minimax_calculation (game_board, minimax_depth, a, b, player_max):
    '#''
    Determines the greatest valued move for the AI to play. Utilizes varying levels of depth 
    and alpha-beta pruning to determine how deep the minimax AI should look before selecting a move.

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    minimax_depth : int 0+ ## the number of branches from the original node (odd = min, even = max)
    a : alpha value for alpha-beta pruning
    b : beta value for alpha-beta pruning
    player_max : boolean value ## signifies if the calculation is at a max or min (max = True, min = False) 
    
    ##return::

    '#''
    
    valid_loc = get_is_valid(game_board)
    term_node = get_is_term(game_board)

    if minimax_depth == 0 or term_node:
        if term_node:
            if get_win(game_board, minimax_disk):
                #If the specific move will allow for the minimax_ai to win then make this move
                return (None, 100000000000000)

            elif get_win(game_board, player_disk):
                #If the specific move will allow for the player to win then make this move
                return (None, -10000000000000)
            else:
                #Return 0 for minimax_depth case 0 if no immediate move effect
                return (None, 0)
        else: 
            #If the minimax_depth is 0 this will be the return clause
            return (None, pos_value(game_board, minimax_disk))
    
    if player_max:
        #Valuing the 'maximization' of the player
        pos_val = -math.inf
        which_column = random.choice(valid_loc)
        for col in valid_loc:
            row = available_row(game_board, col)
            game_board_copy = game_board.copy()
            place_disk(game_board_copy, row, col, minimax_disk)
            #recursively calls the minimax calculation changing the depth to 1 less and the player_max to False
            
            new_tally = minimax_calculation(game_board_copy, minimax_depth-1, a, b, False)[1]

            if new_tally > pos_val:
                pos_val = new_tally
                which_column = col
            a = max(a, pos_val)
            if a >= b:
                break
        return which_column, pos_val

    else: 
        #Valuing the 'minimization' of the player
        pos_val = math.inf
        which_column = random.choice(valid_loc)
        for col in valid_loc:
            row = available_row(game_board, col)
            game_board_copy = game_board.copy()
            place_disk(game_board_copy, row, col, player_disk)
            #recursively calls the minimax calculation changing the depth to 1 less and the player_max to True

            new_tally = minimax_calculation(game_board_copy, minimax_depth-1, a, b, True)[1]

            if new_tally < pos_val:
                pos_val = new_tally
                which_column = col
            b = min(b, pos_val)
            if a >= b:
                break
            return which_column, pos_val'''

def minimax_calculation(game_board, minimax_depth, a, b, player_max):
	valid_loc = get_is_valid(game_board)
	term_node = get_is_term(game_board)
	if minimax_depth == 0 or term_node:
		if term_node:
			if get_win(game_board, minimax_disk):
				return (None, 100000000000000)
			elif get_win(game_board, player_disk):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, pos_value(game_board, minimax_disk))
	if player_max:
		value = -math.inf
		which_column = random.choice(valid_loc)
		for col in valid_loc:
			row = available_row(game_board, col)
			b_copy = game_board.copy()
			place_disk(b_copy, row, col, minimax_disk)
			new_score = minimax_calculation(b_copy, minimax_depth-1, a, b, False)[1]
			if new_score > value:
				value = new_score
				which_column = col
			a = max(a, value)
			if a >= b:
				break
		return which_column, value

	else: # Minimizing player
		value = math.inf
		which_column = random.choice(valid_loc)
		for col in valid_loc:
			row = available_row(game_board, col)
			b_copy = game_board.copy()
			place_disk(b_copy, row, col, player_disk)
			new_score = minimax_calculation(b_copy, minimax_depth-1, a, b, True)[1]
			if new_score < value:
				value = new_score
				which_column = col
			b = min(b, value)
			if a >= b:
				break
		return which_column, value



'''def determine_ideal_move(game_board, disk):
    ###
    Determines the ideal column for the disk to be dropped into. 

    ##args::
    game_board : create_game_board() ## a board of zeroes created
    disk : int (0 or 1) ## player_disk or minimax_disk
    ###
    valid_loc = get_is_valid(game_board)
    ideal_tally = -10000
    ideal_column = random.choice(valid_loc)

    for col in valid_loc:
        row = available_row(game_board, col)
        #creates a temporary copy of the game board
        game_board_copy = game_board.copy()
        place_disk(game_board_copy, row, col, disk)
        tally = pos_value(game_board_copy, disk)

        if tally > ideal_tally:
            ideal_tally = tally
            ideal_column = col

    print(ideal_column)
    return ideal_column'''


if __name__ == "__main__":

    game_board = create_game_board()
    display_board(game_board)
    is_game_finished = False
    whos_move = random.randint(player, minimax_ai)

    pygame.init()
    pygame_win = pygame.display.set_mode(win_size)
    pygame_font = pygame.font.SysFont("calibri", 30)

    pygame_board_create(game_board)

    #updates the pygame visual gui display with the current board
    pygame.display.update()

    #### MAIN LOOP OF THE GAME ####
    while not is_game_finished:
        #continues the while loop until the game is determined to be complete

        for e in pygame.event.get():
            #iterates through the list of events received from pygame event handler

            if e.type == pygame.QUIT:
                #closes the system window using sys.exit() if the event is QUIT
                sys.exit()

            if e.type == pygame.MOUSEMOTION:
                #tracks the mouse movement and hovers the piece above the grid in the similar x cordinate
                pygame.draw.rect(pygame_win, grid_fg, (0,0, win_width, box_size))
                x_position = e.pos[0]
                if whos_move == player:
                    pygame.draw.circle(pygame_win, blue_piece, (x_position, int(box_size/2)), disk_rad)
                    
            pygame.display.update()

            if e.type == pygame.MOUSEBUTTONDOWN:
			
                pygame.draw.rect(pygame_win, grid_fg, (0,0, win_width, box_size))
			    #print(event.pos)
			    # Ask for Player 1 Input
                if whos_move == player:
                    x_position = e.pos[0]
                    col = int(math.floor(x_position/box_size))
                    
                    if valid_move(game_board, col):
                        row = available_row(game_board, col)
                        place_disk(game_board, row, col, player_disk)
                        
                        if get_win(game_board, player_disk):
                            winner_text = pygame_font.render("Player 1 wins!!", 1, blue_piece)
                            # blit will display the text overlapping the rest of the window
                            pygame_win.blit(winner_text, (20,5))
                            
                            is_game_finished = True
                            
                        whos_move += 1
                        whos_move = whos_move % 2
                        
                        display_board(game_board)
                        pygame_board_create(game_board)

        if whos_move == minimax_ai and not is_game_finished:
            # If it is the minimax_ai turn and the game has not been deemed to be over
            col, minimax_value = minimax_calculation(game_board, 5, -math.inf, math.inf, True)
            print(col, minimax_value)

            if valid_move(game_board, col):
                row = available_row(game_board, col)
                place_disk(game_board, row, col, minimax_disk)

                if get_win(game_board, minimax_disk):
                    winner_text = pygame_font.render("Player 2 wins!!", 1, green_piece)
                    pygame_win.blit(winner_text, (20,5))
                    is_game_finished = True

                display_board(game_board)
                pygame_board_create(game_board)

                whos_move += 1
                whos_move = whos_move % 2


        if is_game_finished:
            pygame.time.wait(3000)