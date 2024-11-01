"""Игра змейка."""

from random import choice
import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный
RED = (255, 0, 0)  # Красный
GREEN = (0, 255, 0)  # Зеленый

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """
    Это базовый класс, от которого наследуются другие игровые объекты.

    Он содержит общие атрибуты игровых объектов — например, эти атрибуты
    описывают позицию и цвет объекта; этот же класс содержит и заготовку
    метода для отрисовки объекта на игровом поле — draw.
    """

    def __init__(self, position=CENTER, body_color=None):
        """
        Конструктор класса.

        Инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Это абстрактный метод.

        Предназначен для переопределения в
        дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывает яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def randomize_position(self):
        """
        Устанавливает случайное положение яблока на игровом поле.

        Задаёт атрибуту position новое значение.
        """
        self.position = (
            choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT, GRID_SIZE)))
        return self.position

    def __init__(self, body_color=RED):
        """
        Конструктор класса.

        Который задает цвет яблока и вызывает метод
        randomize_position, чтобы установить начальную позицию яблока.
        """
        super().__init__(self.randomize_position(), body_color)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject.

    Описывает змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self, position=CENTER, body_color=GREEN):
        """Конструктор класса, инициализирующий начальное состояние змейки."""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции).

        Добавляет новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        head = self.get_head_position()
        dx, dy = self.direction
        new_pos = (
            ((head[0] + (dx * GRID_SIZE)) % SCREEN_WIDTH),
            (head[1] + (dy * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        """Возвращает первый элемент в списке positions."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            MOTION = {
                pygame.K_UP: (DOWN, UP),
                pygame.K_DOWN: (UP, DOWN),
                pygame.K_LEFT: (RIGHT, LEFT),
                pygame.K_RIGHT: (LEFT, RIGHT)
            }
            if (event.key in MOTION
                    and game_object.direction != MOTION[event.key][0]):
                game_object.next_direction = MOTION[event.key][1]


def main():
    """
    Этот код выполняется только тогда, когда запускается файл с ним.

    Если файл будет импортирован, то этот код не выполнится.
    """
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        snake.draw(surface)
        apple.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    main()
