import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Stack Visualization")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (80,150,255)
GREEN = (120,220,120)
GRAY = (200,200,200)
DARKGRAY = (150,150,150)

FONT = pygame.font.SysFont(None, 30)

waiting_items = []
stack_items = []
pop_result = []

moving_to_stack = None
moving_to_pop = None

WAIT_Y = 80
STACK_CENTER_X = 450
STACK_TOP_Y = 320 
RESULT_Y = 500


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 20, self.rect.y + 10))

    def is_click(self, pos):
        return self.rect.collidepoint(pos)


class WaitingItem:
    def __init__(self, value, x):
        self.value = value
        self.x = x
        self.y = WAIT_Y
        self.target_x = x
        self.target_y = WAIT_Y

    def update(self):
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

    def draw(self):
        pygame.draw.rect(screen, DARKGRAY, (self.x, self.y, 60, 40))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 20, self.y + 8))


class StackItem:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y

    def update(self):
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 60, 40))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 20, self.y + 8))


def arrange_waiting():
    for i, item in enumerate(waiting_items):
        item.target_x = 50 + i * 80
        item.target_y = WAIT_Y


def arrange_stack():
    for i, item in enumerate(stack_items):
        item.target_x = STACK_CENTER_X
        item.target_y = STACK_TOP_Y - i * 60


def push():
    global moving_to_stack

    if not waiting_items:
        return

    moving_to_stack = waiting_items[0]
    moving_to_stack.target_x = STACK_CENTER_X
    moving_to_stack.target_y = STACK_TOP_Y - len(stack_items) * 60

    for i in range(1, len(waiting_items)):
        waiting_items[i].target_x -= 80

def pop_stack():
    global moving_to_pop

    if not stack_items:
        return

    moving_to_pop = stack_items[-1]
    target_x = 50 + len(pop_result) * 80
    target_y = RESULT_Y
    moving_to_pop.target_x = target_x
    moving_to_pop.target_y = target_y


initial_values = [3, 5, 8, 2, 9]
start_x = 50

for v in initial_values:
    waiting_items.append(WaitingItem(v, start_x))
    start_x += 80

btn_push = Button(300, 380, 150, 50, "Push")
btn_pop = Button(500, 380, 150, 50, "Pop")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if btn_push.is_click(pos):
                push()
            if btn_pop.is_click(pos):
                pop_stack()

    for item in waiting_items:
        item.update()

    for item in stack_items:
        item.update()

    if moving_to_stack:
        moving_to_stack.update()
        if (abs(moving_to_stack.x - moving_to_stack.target_x) < 1 and
            abs(moving_to_stack.y - moving_to_stack.target_y) < 1):
            waiting_items.pop(0)
            arrange_waiting()

            stack_items.append(
                StackItem(moving_to_stack.value, moving_to_stack.x, moving_to_stack.y)
            )
            arrange_stack()

            moving_to_stack = None

    if moving_to_pop:
        moving_to_pop.update()
        if (abs(moving_to_pop.x - moving_to_pop.target_x) < 1 and
            abs(moving_to_pop.y - moving_to_pop.target_y) < 1):
            pop_result.append(moving_to_pop.value)
            stack_items.pop()
            arrange_stack()
            moving_to_pop = None

    screen.fill(WHITE)

    txt = FONT.render("Waiting List:", True, BLACK)
    screen.blit(txt, (50, 40))
    for item in waiting_items:
        item.draw()

    txt2 = FONT.render("Stack (Top -> Bottom)", True, BLACK)
    screen.blit(txt2, (STACK_CENTER_X - 200, STACK_TOP_Y - 20))  
    for item in stack_items:
        item.draw()

    txt3 = FONT.render("Pop Result:", True, BLACK)
    screen.blit(txt3, (50, 460))

    x = 50
    for v in pop_result:
        pygame.draw.rect(screen, GREEN, (x, RESULT_Y, 60, 40))
        screen.blit(FONT.render(str(v), True, BLACK), (x + 20, RESULT_Y + 8))
        x += 80

    btn_push.draw()
    btn_pop.draw()

    pygame.display.flip()
    clock.tick(FPS)
