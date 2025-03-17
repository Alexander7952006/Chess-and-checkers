class Checker(object):
    """Класс Checker будет являться родительским классов для других классов шашек.

    Attributes:
        color: строка для определения цвета шашки
    """

    def __init__(self, color):
        """Инициализация класса.

        Args:
            color (str): цвет шашки
        """

        self.color =  color

    def get_symbol(self):
        """Метод, который будет переопределен дочерних классах. Нужен для
        того, чтобы получить символ, которым обозначается шашка.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def get_possible_moves(self):
        """Метод, который будет переопределен дочерних классах. Нужен для
        того, получить список возможных ходов для шашки.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

class Normal(Checker):
    """Дочерний класс класса Checker для обычной шашки.

    Attributes:
        color: строка для определения цвета шашки
    """

    def get_symbol(self):
        """Метод, который нужен для того, чтобы получить символ,
         которым обозначается шашка.

        Returns:
            str: символ фигуры
        """

        return 'N' if self.color == 'white' else 'n'

    def get_possible_moves(self, board, position):
        """Метод, который нужен для
        того, получить список возможных ходов для шашки.

        Args:
            board (Board): объект класса доска
            position (tuple): позиция шашки

        Returns:
            list: список всех возможных ходов(кортежей с позициями)
        """

        moves = []
        string, col = position
        dir_str = -1 if self.color == 'white' else 1
        for dir_col in [-1, 1]:
            newpos = (string + dir_str, col + dir_col)
            if board.is_valid_position(newpos):
                if not board.get_checker(newpos):
                    moves.append((newpos, None))

        dir_x = -2 if self.color == 'white' else 2
        for dir_y in [-2, 2]:
            newpos = (string + dir_x, col + dir_y)
            between_x = 1 if dir_x < 0 else -1
            between_y = 1 if dir_y < 0 else -1
            if (not board.get_checker(newpos) and
                board.get_checker((newpos[0] + between_x, newpos[1] + between_y))):
                eatable = board.get_checker((newpos[0] + between_x,
                                     newpos[1] + between_y))
                if eatable.color != self.color:
                    moves.append((newpos, [(newpos[0] + between_x, newpos[1] + between_y)]))
                    
        cleared_moves = []
        for tup in moves:
            if tup[1] != None:
                cleared_moves.append(tup)
        if len(cleared_moves) > 0:
            return cleared_moves
        else:
            return moves
            

class Queen(Checker):
    """Дочерний класс класса Checker для дамки.

    Attributes:
        color: строка для определения цвета дамки
    """

    def get_symbol(self):
        """Метод, который нужен для того, чтобы получить символ,
         которым обозначается дамка.

        Returns:
            str: символ дамки
        """

        return 'Q' if self.color == 'white' else 'q'

    def get_possible_moves(self, board, position):
        """Метод, который нужен для
        того, получить список возможных ходов для дамки.

        Args:
            board (Board): объект класса доска
            position (tuple): позиция дамки

        Returns:
            list: список всех возможных ходов(кортежей с позициями)
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
                path = []
                arg = 0
                new_pos = (string + dir, col + dir_y)
                if board.is_valid_position(new_pos):
                    if not board.get_checker(new_pos):
                        for el in range(start, end, step):
                            if el > 0:
                                el_y = el if dir_y > 0 else -el
                            else:
                                el_y = -el if dir_y > 0 else el
                            path.append((board.get_checker((string + el, col + el_y)),
                                        (string + el, col + el_y)))
                    else:
                        arg += 1
                else:
                    arg += 1

                if arg == 0:
                    eated = []
                    for indx, el in enumerate(path):
                        if type(el[0]) == Queen or type(el[0]) == Normal:
                            if el[0].color == self.color:
                                arg += 1

                        if indx > 0:
                            if path[indx][0] != None and path[indx - 1][0] != None:
                                arg += 1
                        
                        if el[0] != None:
                            eated.append(el[1])

                    if arg == 0:
                        moves.append((new_pos, eated))

        cleared_moves = []
        for tup in moves:
            if tup[1] != None:
                cleared_moves.append(tup)
        if len(cleared_moves) > 0:
            return cleared_moves
        else:
            return moves


class Board(object):
    """Класс шахматной доски.

    Attributes:
        field (lst): представление поля в котором вложены списки с рядами доски
    """

    def __init__(self):
        """Инициализация доски"""
        self.field = [[None for _ in range(8)] for _ in range(8)]
        self.setup_checkers()

    def setup_checkers(self):
        """Метод для расстановки фигур на поле"""
        for string in [0, 1, 2]:
            for col in range(1, 8, 2):
                self.field[string][col - string % 2] = Normal('black')
        for string in [5, 6, 7]:
            for col in range(1, 8, 2):
                self.field[string][col - string % 2] = Normal('white')

    def display(self):
        """Метод для вывода поля в консоль"""
        print(' ')
        print("   a b c d e f g h\n")
        for indx, row in enumerate(self.field):
            print(8 - indx, end = '  ')
            for checker in row:
                print(checker.get_symbol() if checker else '.', end = ' ')

            print(' ' + str(8 - indx))
        print("\n   a b c d e f g h\n")

    def get_checker(self, position):
        """Метод для получения шашки по заданным координатам.

        Args:
            position (tuple): координаты клетки

        Returns:
            Объект типа одной из шашек либо None
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

    def turning_queen(self):
        """Метод для замены шашаки на дамку при достижении другого конца поля."""

        for indx, row in enumerate(self.field):
            for indx2, checker in enumerate(row):
                if indx == 0 and checker == Normal('white'):
                    self.field[indx][indx2] = Queen('white')
                if indx == 7 and checker == Normal('black'):
                    self.field[indx][indx2] = Queen('black')

class Game(object):
    """Класс игры.
    
    Attributes:
        board (Board): шахматная доска
        player (str): цвет игрока который сейчас хходит
        move_count (int): счетчик кол-ва ходов
    """
    def __init__(self):
        """Инициализация игры"""
        self.board = Board()
        self.player = 'white'
        self.move_count = 0

    def play(self):
        """Метод для игры"""
        while True:
            self.board.display()
            print(f"Ход № {self.move_count + 1}\n")
            print(f"ХОД {'БЕЛЫХ' if self.player == 'white' else 'ЧЕРНЫХ'}\n")
            start = self.get_input('Введите координаты поля откуда хотите ходить: ')
            end = self.get_input('Введите координаты поля куда хотите ходить: ')
            self.board.turning_queen()
            if self.make_move(start, end):
                self.move_count += 1
                self.player = 'black' if self.player == 'white' else 'white'
            else:
                print('НЕДОПУСТИМЫЙ ХОД. ПОПРОБУЙТЕ СНОВА!\n')
            self.win()

    def get_input(self, prompt):
        """Метод для получения от пользователя координат на поле.

        Args:
            prompt (str): координаты в строчной виде

        Returns:
            tuple: координаты клетки кортежем
        """

        while True:
            position = input(prompt).lower()
            col = ord(position[0]) - ord('a')
            row = 8 - int(position[1])
            return (row, col)

    def make_move(self, start, end):
        """Метод для хода.

        Args:
            start (tuple): координаты откуда сходить
            end (tuple): координаты куда сходить

        Returns:
            bool: истина если все веро введено в противном случае ложь
        """

        checker = self.board.get_checker(start)
        pure_moves = []
        for tup in checker.get_possible_moves(self.board, start):
            pure_moves.append(tup[0])
        if not checker or checker.color != self.player:
            return False
        if end not in pure_moves:
            return False
        for tup in checker.get_possible_moves(self.board, start):
            if tup[0] == end:
                if tup[1] is not None:
                    for el in tup[1]:
                        self.board.field[el[0]][el[1]] = None
        self.board.field[end[0]][end[1]] = checker
        self.board.field[start[0]][start[1]] = None
        return True

    def win(self):
        """Метод для определения победы."""

        black_count = 0
        white_count = 0
        for row in self.board.field:
            for el in row:
                if type(el) == Normal or type(el) == Queen:
                    if el.color == 'black':
                        black_count += 1
                    else:
                        white_count += 1
        if white_count == 0:
            print('ПОБЕДИЛИ БЕЛЫЕ!')
        if black_count == 0:
            print('ПОБЕДИЛИ ЧЕРНЫЕ!')


if __name__ == '__main__':
    game = Game()
    game.play()
