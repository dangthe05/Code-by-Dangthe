import pygame
import time
pygame.init()


ROWS, COLS = 8, 8
SQUARE_SIZE = 100
PIECE_SIZE = 50
WIDTH, HEIGHT = 800, 800

# Màu sắc
GAINSBORO = (220, 200, 220)  # Màu sáng
GRAY = (128, 128, 128)  # Màu tối

def load_piece_images():
    images = {}
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    for color in colors:
        for piece in pieces:
            image = pygame.image.load(f"images/{color}_{piece}.png")
            images[f"{color}_{piece}"] = pygame.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))
    return images

piece_images = load_piece_images()

# Khởi tạo bảng cờ
board = [[None for _ in range(8)] for _ in range(8)]

# Danh sách quân cờ
def initialize_board():
    # Quân đen
    board[0] = ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook']
    board[1] = ['black_pawn'] * 8

    # Quân trắng
    board[6] = ['white_pawn'] * 8
    board[7] = ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook']

initialize_board()

pygame.display.set_caption("Chess with friend")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_board():
    screen.fill(GAINSBORO)  # Lấp đầy màn hình với màu nền

    for row in range(8):
        for col in range(8):
            # Tô màu ô chọn
            if selected_pos == (row, col):
                pygame.draw.rect(screen, (255, 255, 102), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                if (row + col) % 2 == 1:  # Kiểm tra ô chẵn lẻ
                    pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, GAINSBORO, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Vẽ quân cờ
            piece = board[row][col]
            if piece:
                x = col * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                y = row * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                screen.blit(piece_images[piece], (x, y))  # Vẽ quân cờ lên ô

    pygame.display.flip()  # Cập nhật màn hình


selected_piece = None
selected_pos = None
current_player = 'white'  # Trắng bắt đầu


def get_square(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

check_left_rook = 0
check_right_rook = 0
check_move_king = 0
previous_move = None


def is_valid_move(selected_piece, target_row, target_col):
    # Biến cục bộ để kiểm tra các trường hợp nước đi đặc biệt
    global check_move_king, check_left_rook, check_right_rook, previous_move

    
    piece_type = selected_piece.split('_')[1]
    piece_color = selected_piece.split('_')[0]
    start_row, start_col = selected_pos

    # Quân tốt
    if piece_type == 'pawn':
        if piece_color == 'white':
            if start_col == target_col and start_row - 1 == target_row and board[target_row][target_col] is None:
                if target_row == 0 :
                    board[target_row][target_col] = promotion_pawn_menu(piece_color)
                    board[start_row][start_col] = None
                    print(f"{selected_piece}") 
                else:
                    board[target_row][target_col] = selected_piece
                    return True

            if start_col == target_col and start_row == 6 and start_row - 2 == target_row and board[start_row - 1][start_col] is None and board[target_row][target_col] is None:
                previous_move = (start_row, start_col, target_row, target_col)
                return True

            if abs(target_col - start_col) == 1 and target_row == start_row - 1 and board[target_row][target_col] and board[target_row][target_col].split('_')[0] != piece_color:
                if target_row == 0 :
                    board[target_row][target_col] = promotion_pawn_menu(piece_color)
                    board[start_row][start_col] = None
                    print(f"{selected_piece}")
                else:    
                    board[target_row][target_col] = selected_piece
                    return True

            # Điều kiện bắt tốt qua đường
            if previous_move and previous_move[2] == start_row and abs(previous_move[3] - start_col) == 1:
                if previous_move[0] == start_row - 2 and target_row == start_row - 1 and target_col == previous_move[3]:
                    board[previous_move[2]][previous_move[3]] = None  # Xóa quân tốt bị bắt qua đường
                    board[target_row][target_col] = selected_piece
                    return True

        elif piece_color == 'black':
            if start_col == target_col and start_row + 1 == target_row and board[target_row][target_col] is None:
                if target_row == 7 :
                    board[target_row][target_col] = promotion_pawn_menu(piece_color)
                    board[start_row][start_col] = None
                    print(f"{selected_piece}")
                else:
                    board[target_row][target_col] = selected_piece
                    return True

            if start_col == target_col and start_row == 1 and start_row + 2 == target_row and board[start_row + 1][start_col] is None and board[target_row][target_col] is None:
                previous_move = (start_row, start_col, target_row, target_col)
                return True

            if abs(target_col - start_col) == 1 and target_row == start_row + 1 and board[target_row][target_col] and board[target_row][target_col].split('_')[0] != piece_color:
                if target_row == 7 :
                    board[target_row][target_col] = promotion_pawn_menu(piece_color)
                    print(f"{selected_piece}")
                    board[start_row][start_col] = None
                else:    
                    board[target_row][target_col] = selected_piece
                    return True

            # Điều kiện bắt tốt qua đường
            if previous_move and previous_move[2] == start_row and abs(previous_move[3] - start_col) == 1:
                if previous_move[0] == start_row + 2 and target_row == start_row + 1 and target_col == previous_move[3]:
                    board[previous_move[2]][previous_move[3]] = None  # Xóa quân tốt bị bắt qua đường
                    board[target_row][target_col] = selected_piece
                    return True


    # Quân mã
    elif piece_type == 'knight':
        if board[target_row][target_col] is None or (board[target_row][target_col].split('_')[0] != piece_color):
            if (abs(target_col - start_col) == 1 and abs(target_row - start_row) == 2) or (abs(target_row - start_row) == 1 and abs(target_col - start_col) == 2):
                return True

    # Quân tượng
    elif piece_type == 'bishop':
        if board[target_row][target_col] is None or (board[target_row][target_col].split('_')[0] != piece_color):
            if abs(start_col - target_col) == abs(start_row - target_row):
                row_step = 1 if start_row < target_row else -1
                col_step = 1 if start_col < target_col else -1
                r, c = start_row + row_step, start_col + col_step
                while r != target_row and c != target_col:
                    if board[r][c] is not None:
                        return False
                    r += row_step
                    c += col_step
                return True

    # Quân hậu
    elif piece_type == 'queen':
        if board[target_row][target_col] is None or (board[target_row][target_col].split('_')[0] != piece_color):
            if abs(start_col - target_col) == abs(start_row - target_row):
                # Di chuyển chéo
                row_step = 1 if start_row < target_row else -1
                col_step = 1 if start_col < target_col else -1
                r, c = start_row + row_step, start_col + col_step
                while r != target_row and c != target_col:
                    if board[r][c] is not None:
                        return False
                    r += row_step
                    c += col_step
                return True
            elif target_row == start_row:
                # Di chuyển ngang
                step = 1 if target_col > start_col else -1
                for c in range(start_col + step, target_col, step):
                    if board[start_row][c] is not None:
                        return False
                return True
            elif target_col == start_col:
                # Di chuyển dọc
                step = 1 if target_row > start_row else -1
                for r in range(start_row + step, target_row, step):
                    if board[r][start_col] is not None:
                        return False
                return True

    # Quân xe
    elif piece_type == 'rook':
        if board[target_row][target_col] is None or (board[target_row][target_col].split('_')[0] != piece_color):
            if target_row == start_row:
                step = 1 if target_col > start_col else -1
                for c in range(start_col + step, target_col, step):
                    if board[start_row][c] is not None:
                        return False
                
                if board[start_row][0] != f"{piece_color}_rook":  # Kiểm tra quân xe bên trái
                    check_left_rook = check_left_rook + 1
                if board[start_row][7] != f"{piece_color}_rook":  # Kiểm tra quân xe bên phải
                    check_right_rook = check_right_rook + 1

                return True

            elif target_col == start_col:
                step = 1 if target_row > start_row else -1
                for r in range(start_row + step, target_row, step):
                    if board[r][start_col] is not None:
                        return False

                if board[start_row][0] != f"{piece_color}_rook":  # Kiểm tra quân xe bên trái
                    check_left_rook = check_left_rook + 1
                if board[start_row][7] != f"{piece_color}_rook":  # Kiểm tra quân xe bên phải
                    check_right_rook = check_right_rook + 1

                return True

    # Quân vua
    elif piece_type == 'king':
        if board[target_row][target_col] is None or (board[target_row][target_col].split('_')[0] != piece_color):
            if abs(start_row - target_row) <= 1 and abs(start_col - target_col) <= 1:
                check_move_king = check_move_king + 1 
                return True
            
            # Nhập thành
        if check_move_king == 0:
            if start_col == 4 and target_col == 6 and start_row == target_row :
                if check_right_rook == 0:
                    if target_col == 6 and board[start_row][7] == f'{piece_color}_rook' and board[start_row][5] is None:
                        board[start_row][4] = None
                        board[start_row][6] = f'{piece_color}_king'
                        board[start_row][7] = None
                        board[start_row][5] = f'{piece_color}_rook'
                    return True
        if check_move_king == 0:
            if start_col == 4 and target_col == 2 and  start_row == target_row :
                if check_left_rook == 0:
                    if target_col == 2 and board[start_row][0] == f'{piece_color}_rook' and board[start_row][1] is None and board[start_row][2] is None and board[start_row][3] is None:
                        board[start_row][4] = None
                        board[start_row][2] = f'{piece_color}_king'
                        board[start_row][0] = None
                        board[start_row][3] = f'{piece_color}_rook'
                        return True

    return False

def promotion_pawn_menu(color):
    menu_width, menu_height = 420, 200
    pygame.display.set_caption("Phong cấp tốt")
    screen = pygame.display.set_mode((menu_width, menu_height))
    BACKGROUND_COLOR = (255, 255, 200)
    promote_options = ['queen', 'rook', 'bishop', 'knight']
    
    positions = [(60, 100), (160, 100), (260, 100), (360, 100)]
    
    piece_images = {
        'queen': pygame.image.load(f'images/{color}_queen.png'),
        'rook': pygame.image.load(f'images/{color}_rook.png'),
        'bishop': pygame.image.load(f'images/{color}_bishop.png'),
        'knight': pygame.image.load(f'images/{color}_knight.png')
    }
    
    RUNNING = True
    selected_piece = None
    
    while RUNNING:
        screen.fill(BACKGROUND_COLOR)

        for i, option in enumerate(promote_options):
            image = piece_images[option]
            image = pygame.transform.scale(image, (50, 50))
            screen.blit(image, (positions[i][0] - 30, positions[i][1] - 30))
            
            font = pygame.font.Font(None, 36)
            text = font.render(option.capitalize(), True, (0, 0, 0))
            screen.blit(text, (positions[i][0] - 40, positions[i][1] + 35))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                for i, pos in enumerate(positions):
                    if (pos[0] - 30 <= x_pos <= pos[0] + 30) and (pos[1] - 30 <= y_pos <= pos[1] + 30):
                        selected_piece = f"{color}_{promote_options[i]}"
                        RUNNING = False
                        break 

    pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess with friend")
    return selected_piece

def is_king_alive(board):
    white_king = False
    black_king = False
    
    for row in board:
        for piece in row:
            if piece == "white_king":
                white_king = True
            elif piece == "black_king":
                black_king = True
    
    return white_king, black_king

def main():
    global selected_piece, selected_pos, current_player
    running = True
    END = False
    while running:
        #Xử lý các sự kiện khi người dùng bấm chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                row, col = get_square((x_pos, y_pos))

                #Nếu chưa chọn quân cờ nào        
                if selected_piece is None:
                    piece = board[row][col]
                    # Thực hiện việc chọn quân cờ với màu sắc bằng current_player
                    if piece and piece.split('_')[0] == current_player:
                        selected_piece = piece
                        selected_pos = (row, col)
                # Nếu đã chọn quân cờ
                else:
                    #Xử lý các logic đã được cài đặt ở hàm is_valid_move nếu vị trí mục tiêu có quân cờ đối phương
                    if is_valid_move(selected_piece, row, col):
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = None
                        white_king_alive, black_king_alive = is_king_alive(board)
                        if not white_king_alive:
                             print("Đen thắng")
                             END = True
                        elif not black_king_alive:
                            print("Trắng thắng")
                            END = True
                            
                        # Đổi lượt chơi
                        else:
                            current_player = 'black' if current_player == 'white' else 'white'
                    if board[row][col] != selected_piece:
                        white_king_alive, black_king_alive = is_king_alive(board)
                        if not white_king_alive:
                             print("Đen thắng")
                             END = True
                        elif not black_king_alive:
                            print("Trắng thắng")
                            END = True
                        else:
                            current_player = 'black' if current_player == 'white' else 'white'

                    selected_piece = None
                    selected_pos = None



        draw_board()
        if END == True:
            for i in range( 4 , 0, -1):
                time.sleep(1)
                print(f"Đóng chương trình sau {i-1}")
            print("kết thúc")
            time.sleep(1)
            break
    pygame.quit()


if __name__ == "__main__":
    main()