import re
import copy


class Piece(object):
    """Класс Piece будет являться родительским классов для других классов фигур.

    Attributes:
        color: строка для определения цвета фигуры
    """

    def __init__(self, color):
        """Инициализация класса

        Args:
            color (str): цвет фигуры
        """

        self.color = color

    def get_symbol(self):
        """Метод, который будет переопределены дочерних классах. Нужен для
        того, чтобы получить символ, которым обозначается фигура.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def get_possible_moves(self):
        """Метод, который будет переопределены дочерних классах. Нужен для
        того, получить список возможных ходов для фигуры.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()


class Pawn(Piece):
    """Дочерний класс класса Piece для пешки.

    Attributes:
        color: строка для определения цвета фигуры
    """

    def get_symbol(self):
        """Метод, который нужен для
        того, чтобы получить символ, которым обозначается фигура.

        Returns:
            str: символ фигуры
        """

        return 'P' if self.color == 'white' else 'p'

    def get_possible_moves(self, board, position):
        """Метод, который нужен для
        того, получить список возможных ходов для фигуры.

        Args:
            board (Board): объекс класса доска
            position (tuple): позиция фигуры

        Returns:
            list: список всех возможных ходов(кортежей с позициями)
        """

        moves = []
        string, col = position
        direction = -1 if self.color == 'white' else 1

        if self.color == 'white' and string == 6:
            dir = -2
            if board.is_valid_position((string + dir, col)) and not board.get_piece((string + dir, col)):
                moves.append((string + dir, col))

        if self.color == 'black' and string == 1:
            dir = 2
            if board.is_valid_position((string + dir, col)) and not board.get_piece((string + dir, col)):
                moves.append((string + dir, col))

        if board.is_valid_position((string + direction, col)) and not board.get_piece((string + direction, col)):
            moves.append((string + direction, col))

        for eat in [-1, 1]:
            new_pos = (string + direction, col + eat)
            if board.is_valid_position(new_pos):
                piece = board.get_piece(new_pos)
                if piece and piece.color != self.color:
                    moves.append(new_pos)
        return moves


class Rook(Piece):
    """Дочерний класс класса Piece для ладьи.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'R' if self.color == 'white' else 'r'

    def get_possible_moves(self, board, position):
        """Метод для получения всех возможных ходов фигуры.

        Args:
            board (Board): объект класса доска
            position (tuple): позиция фигуры

        Returns:
            list: список всех возможных ходов
        """

        moves = []
        string, col = position

        for direction in [el for el in range(-8, 9) if el != 0]:
            for dir_x in [direction, 0]:
                for dir_y in [direction, 0]:
                    if dir_x != dir_y:
                        new_pos = (string + dir_x, col + dir_y)
                        if board.is_valid_position(new_pos):
                            arg = 0
                            if direction > 0:
                                start = 1
                                end = direction
                            else:
                                start = direction + 1
                                end = 0
                            for el in range(start, end):
                                el_x = 0 if dir_x == 0 else el
                                el_y = 0 if dir_y == 0 else el
                                if board.get_piece((string + el_x, col + el_y)):
                                    arg += 1
                                    break

                            if arg == 0:
                                if board.get_piece(new_pos):
                                    if board.get_piece(new_pos).color != self.color:
                                        moves.append(new_pos)
                                else:
                                    moves.append(new_pos)
        return moves


class Bishop(Piece):
    """Дочерний класс класса Piece для слона.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'B' if self.color == 'white' else 'b'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position

        for dir in [el for el in range(-8, 9) if el != 0]:
            if dir > 0:
                start = 1
                end = dir
                step = 1
            else:
                start = -1
                end = dir
                step = -1
            for dir_y in [-dir, dir]:
                new_pos = (string + dir, col + dir_y)
                if board.is_valid_position(new_pos):
                    arg = 0
                    for el in range(start, end, step):
                        if el > 0:
                            el_y = el if dir_y > 0 else -el
                        else:
                            el_y = -el if dir_y > 0 else el
                        if board.get_piece((string + el, col + el_y)):
                            arg += 1
                            break
                    if arg == 0:
                        if board.get_piece(new_pos):
                            if board.get_piece(new_pos).color != self.color:
                                moves.append(new_pos)
                        else:
                            moves.append(new_pos)
        return moves


class King(Piece):
    """Дочерний класс класса Piece для короля.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'K' if self.color == 'white' else 'k'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position

        for dir_str in [-1, 0, 1]:
            for dir_col in [-1, 0, 1]:
                if not (dir_col == 0 and dir_str == 0):
                    new_pos = (string + dir_str, col + dir_col)
                    if board.is_valid_position(new_pos):
                        if board.get_piece(new_pos):
                            if board.get_piece(new_pos).color != self.color:
                                moves.append(new_pos)
                        else:
                            moves.append(new_pos)
        return moves


class Knight(Piece):
    """Дочерний класс класса Piece для коня.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'N' if self.color == 'white' else 'n'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position
        for dir_str in [-2, -1, 1, 2]:
            for dir_col in [-2, -1, 1, 2]:
                if abs(dir_str) != abs(dir_col):
                    new_pos = (string + dir_str, col + dir_col)
                    if board.is_valid_position(new_pos):
                        if board.get_piece(new_pos):
                            if board.get_piece(new_pos).color != self.color:
                                moves.append(new_pos)
                        else:
                            moves.append(new_pos)
        return moves


class Queen(Piece):
    """Дочерний класс класса Piece для ферзя.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'Q' if self.color == 'white' else 'q'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position

        for direction in [el for el in range(-8, 9) if el != 0]:
            for dir_x in [direction, 0]:
                for dir_y in [direction, 0]:
                    if dir_x != dir_y:
                        new_pos = (string + dir_x, col + dir_y)
                        if board.is_valid_position(new_pos):
                            arg = 0
                            if direction > 0:
                                start = 1
                                end = direction
                            else:
                                start = direction + 1
                                end = 0
                            for el in range(start, end):
                                el_x = 0 if dir_x == 0 else el
                                el_y = 0 if dir_y == 0 else el
                                if board.get_piece((string + el_x, col + el_y)):
                                    arg += 1
                                    break

                            if arg == 0:
                                if board.get_piece(new_pos):
                                    if board.get_piece(new_pos).color != self.color:
                                        moves.append(new_pos)
                                else:
                                    moves.append(new_pos)

        for dir in [el for el in range(-8, 9) if el != 0]:
            if dir > 0:
                start = 1
                end = dir
                step = 1
            else:
                start = -1
                end = dir
                step = -1
            for dir_y in [-dir, dir]:
                new_pos = (string + dir, col + dir_y)
                if board.is_valid_position(new_pos):
                    arg = 0
                    for el in range(start, end, step):
                        if el > 0:
                            el_y = el if dir_y > 0 else -el
                        else:
                            el_y = -el if dir_y > 0 else el
                        if board.get_piece((string + el, col + el_y)):
                            arg += 1
                            break
                    if arg == 0:
                        if board.get_piece(new_pos):
                            if board.get_piece(new_pos).color != self.color:
                                moves.append(new_pos)
                        else:
                            moves.append(new_pos)
        return moves


class Soldier(Piece):
    """Дочерний класс класса Piece для солдата.
     Эта фигура ходит на 2 клетки аперед и может перескакивать другие фигуры.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'S' if self.color == 'white' else 's'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position
        direction = -2 if self.color == 'white' else 2
        new_pos = (string + direction, col)
        if board.is_valid_position(new_pos):
            if board.get_piece(new_pos):
                if board.get_piece(new_pos).color != self.color:
                    moves.append(new_pos)
            else:
                moves.append(new_pos)
        return moves


class Horse(Piece):
    """Дочерний класс класса Piece для всадника.
     Эта фигура ходит как конь только 2 на 2.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'H' if self.color == 'white' else 'h'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position
        for dir_str in [-2, 2]:
            for dir_col in [-2, 2]:
                new_pos = (string + dir_str, col + dir_col)
                if board.is_valid_position(new_pos):
                    if board.get_piece(new_pos):
                        if board.get_piece(new_pos).color != self.color:
                            moves.append(new_pos)
                    else:
                        moves.append(new_pos)
        return moves


class Changer(Piece):
    """Дочерний класс класса Piece для changer.
     Эта фигура ходит как ладья но не есть вражескую фигуру, а меняется с ней местами.

    Attributes:
        color (str): цвет фигуры
    """

    def get_symbol(self):
        """Метод для получения символа фигуры.

        Returns:
            str: символ фигуры
        """

        return 'C' if self.color == 'white' else 'c'

    def get_possible_moves(self, board, position):
        """Метод для получения списка всех возможных ходов.

        Args:
            board (Board): шахматная доска
            position (tuple): координаты фигуры которой ходите

        Returns:
            list: список возможных ходов
        """

        moves = []
        string, col = position

        for direction in [el for el in range(-8, 9) if el != 0]:
            for dir_x in [direction, 0]:
                for dir_y in [direction, 0]:
                    if dir_x != dir_y:
                        new_pos = (string + dir_x, col + dir_y)
                        if board.is_valid_position(new_pos):
                            arg = 0
                            if direction > 0:
                                start = 1
                                end = direction
                            else:
                                start = direction + 1
                                end = 0
                            for el in range(start, end):
                                el_x = 0 if dir_x == 0 else el
                                el_y = 0 if dir_y == 0 else el
                                if board.get_piece((string + el_x, col + el_y)):
                                    arg += 1
                                    break

                            if arg == 0:
                                if board.get_piece(new_pos):
                                    if board.get_piece(new_pos).color != self.color:
                                        moves.append(new_pos)
                                else:
                                    moves.append(new_pos)
        return moves


class Board(object):
    """Класс шахматной доски.

    Attributes:
        field (lst): представление поля в котором вложены списки с рядами доски
    """

    def __init__(self):
        """Инициализация шахматной доски."""

        self.field = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        """Метод для расстановки фигур на поле."""

        for indx in range(8):
            self.field[1][indx] = Pawn('black')
            self.field[6][indx] = Pawn('white')

        self.field[0][0] = Rook('black')
        self.field[0][7] = Rook('black')
        self.field[7][0] = Rook('white')
        self.field[7][7] = Rook('white')

        self.field[7][2] = Bishop('white')
        self.field[7][5] = Bishop('white')
        self.field[0][2] = Bishop('black')
        self.field[0][5] = Bishop('black')

        self.field[7][4] = King('white')
        self.field[0][4] = King('black')

        self.field[7][1] = Knight('white')
        self.field[7][6] = Knight('white')
        self.field[0][1] = Knight('black')
        self.field[0][6] = Knight('black')

        self.field[7][3] = Queen('white')
        self.field[0][3] = Queen('black')

        self.field[5][1] = Soldier('white')
        self.field[2][1] = Soldier('black')

        self.field[5][3] = Horse('white')
        self.field[2][3] = Horse('black')

        self.field[5][5] = Changer('white')
        self.field[2][5] = Changer('black')

    def display(self):
        """Метод для вывода поля в консоль."""

        print(' ')
        print("   a b c d e f g h\n")
        for indx, row in enumerate(self.field):
            print(8 - indx, end = '  ')
            for piece in row:
                print(piece.get_symbol() if piece else '.', end = ' ')

            print(' ' + str(8 - indx))
        print("\n   a b c d e f g h\n")


    def get_piece(self, position):
        """Метод для получения фигуры по заданным координатам.

        Args:
            position (tuple): координаты клетки

        Returns:
            Объект типа одной из фигур либо None
        """

        string, col = position
        return self.field[string][col] if self.is_valid_position(position) else None

    @staticmethod
    def is_valid_position(position):
        """Метод для проверки корректности введенных координат(не выходят ли они за пределы поля).

        Args:
            position (tuple): координаты позиции

        Returns:
            bool: истина если координаты валидны и ложь в противном случае
        """

        string, col = position
        return 0 <= string < 8 and 0 <= col < 8


class Game(object):
    """Класс игры.
    
    Attributes:
        board (Board): шахматная доска
        player (str): цвет игрока который сейчас хходит
        move_count (int): счетчик кол-ва ходов
        history (list): список в котором хранятся копии объектов поля
        на каждом из ходов. Необходимо для отката на n ходов
    """
    def __init__(self):
        """Метод для инициализации игры."""

        self.board = Board()
        self.player = 'white'
        self.move_count = 0
        self.history = [copy.deepcopy(self.board)]

    def play(self):
        """Метод для игры"""

        while True:
            self.board.display()
            print(f"Ход № {self.move_count + 1}\n")
            print(f"ХОД {'БЕЛЫХ' if self.player == 'white' else 'ЧЕРНЫХ'}\n")
            start = self.get_input('Введите координаты фигуры, которой хотите ходить: ')
            self.help_func(start)
            try:
                if re.fullmatch(r"откат на [0-9]+", start):
                    num = int(re.search(r"[0-9]+", start).group())
                    self.move_count -= num
                    if num % 2:
                        if self.player == 'black':
                            self.player = 'white'
                        else:
                            self.player = 'black'
                    self.history = self.history[: - num]
                    self.board = self.history[-1]

            except TypeError:
                end = self.get_input('Введите координаты, куда хотите ходить. Например, a1: ')

                if self.make_move(start, end):
                    self.move_count += 1
                    self.player = 'black' if self.player == 'white' else 'white'
                else:
                    print('НЕДОПУСТИМЫЙ ХОД, ПОПРОБУЙТЕ СНОВА\n')

    def get_input(self, prompt):
        """Метод для получения от пользователя координат на поле.

        Args:
            prompt (str): координаты в строчной виде

        Returns:
            tuple or str: координаты клетки кортежем либо строчная команда для
            отката
        """

        while True:
            try:
                position = input(prompt).lower()
                col = ord(position[0]) - ord('a')
                row = 8 - int(position[1])
                return (row, col)
            except:
                try:
                    if re.fullmatch(r"откат на [0-9]+", position):
                        num = int(re.search(r"[0-9]+", position).group())
                        if num <= self.move_count:
                            return position
                        else:
                            print('Нельзя откатить на такое кол-во ходов')
                    else:
                        print('Некорректно введени координаты, попробуйте снова. Пример правильного ввода: a1\n')
                except:
                    print('Неправильно прописана функция отката')

    def make_move(self, start, end):
        """Метод для хода.

        Args:
            start (tuple): координаты откуда сходить
            end (tuple): координаты куда сходить

        Returns:
            bool: истина если все веро введено в противном случае ложь
        """

        piece = self.board.get_piece(start)
        if not piece or piece.color != self.player:
            return False
        if end not in piece.get_possible_moves(self.board, start):
            return False
        if type(piece) == Changer:
            self.board.field[start[0]][start[1]] = self.board.get_piece(end)
            self.board.field[end[0]][end[1]] = piece
            self.history.append(copy.deepcopy(self.board))
            return True
        else:
            self.board.field[end[0]][end[1]] = piece
            self.board.field[start[0]][start[1]] = None
            self.history.append(copy.deepcopy(self.board))
            return True

    def help_func(self, start):
        """Метод для подсказки куда можно сходить и какие фигуры можно съесть.

        Args:
            start (tuple): координаты откуда сходить
        """

        try:
            if self.board.get_piece(start):
                current_piece = self.board.get_piece(start)
                print(' ')
                print("   a b c d e f g h\n")
                for indx, row in enumerate(self.board.field):
                    print(8 - indx, end = '  ')
                    for indx2, piece in enumerate(row):
                        if (indx, indx2) in current_piece.get_possible_moves(self.board, start):
                            print(f"\033[91m{piece.get_symbol() if piece else '.'}\033[0m", end = ' ')
                        else:
                            print(piece.get_symbol() if piece else '.', end = ' ')

                    print(' ' + str(8 - indx))
                print("\n   a b c d e f g h\n")
        except:
            return


if __name__ == '__main__':
    game = Game()
    game.play()
