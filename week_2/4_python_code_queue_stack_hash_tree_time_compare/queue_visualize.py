import pygame
import sys

pygame.init()

# 여기서 너비와 높이를 조절 가능
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Queue Visualization")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (80,150,255)
GREEN = (120,220,120)
RED = (250,120,120)
GRAY = (200,200,200)
DARKGRAY = (150,150,150)

FONT = pygame.font.SysFont(None, 30)

waiting_items = []
queue_items = []
dequeue_result = []

moving_to_queue = None
moving_to_dequeue = None
QUEUE_Y = 250
WAIT_Y = 80
RESULT_Y = 500


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 15, self.rect.y + 10))

    def is_click(self, pos):
        return self.rect.collidepoint(pos)


class WaitingItem:
    def __init__(self, value, x):
        self.value = value
        self.x = x
        self.y = WAIT_Y
        self.target_x = x

    def update(self):
        if abs(self.x - self.target_x) > 1:
            self.x += (self.target_x - self.x) * 0.075

    def draw(self):
        pygame.draw.rect(screen, DARKGRAY, (self.x, self.y, 60, 40))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 20, self.y + 8))


class QueueItem:
    def __init__(self, value, x):
        self.value = value
        self.x = x
        self.y = QUEUE_Y
        self.target_x = x

    def update(self):
        if abs(self.x - self.target_x) > 1:
            self.x += (self.target_x - self.x) * 0.075

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 60, 40))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 20, self.y + 8))


def arrange_waiting():
    for i, item in enumerate(waiting_items):
        item.target_x = 50 + i * 80


def arrange_queue():
    for i, item in enumerate(queue_items):
        item.target_x = 200 + i * 80


def enqueue():
    global moving_to_queue

    if not waiting_items:
        return
    moving_to_queue = waiting_items[0]
    entry_x = 200 + len(queue_items) * 80
    moving_to_queue.target_x = entry_x
    moving_to_queue.y = QUEUE_Y

    for i in range(1, len(waiting_items)):
        waiting_items[i].target_x -= 80


def dequeue():
    global moving_to_dequeue

    if not queue_items:
        return

    item = queue_items[0]
    item.target_x = -200
    moving_to_dequeue = item

# 여러가지 결과를 보고 싶으면, 해당 리스트만 바꿔주면 됨.
initial_values = [1, 2, 3, 4, 5]
start_x = 50

for v in initial_values:
    waiting_items.append(WaitingItem(v, start_x))
    start_x += 80

btn_enqueue = Button(200, 380, 150, 50, "Enqueue")
btn_dequeue = Button(380, 380, 150, 50, "Dequeue")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if btn_enqueue.is_click(pos):
                enqueue()
            if btn_dequeue.is_click(pos):
                dequeue()

    for item in waiting_items:
        item.update()

    for item in queue_items:
        item.update()

    if moving_to_queue:
        moving_to_queue.update()
        if abs(moving_to_queue.x - moving_to_queue.target_x) < 1:
            waiting_items.pop(0)
            arrange_waiting()

            queue_items.append(
                QueueItem(moving_to_queue.value, moving_to_queue.x)
            )
            arrange_queue()

            moving_to_queue = None

    if moving_to_dequeue:
        moving_to_dequeue.update()
        if moving_to_dequeue.x < -150:
            dequeue_result.append(moving_to_dequeue.value)
            queue_items.pop(0)
            arrange_queue()
            moving_to_dequeue = None

    screen.fill(WHITE)

    txt = FONT.render("Waiting List:", True, BLACK)
    screen.blit(txt, (50, 40))
    for item in waiting_items:
        item.draw()

    txt2 = FONT.render("Queue:", True, BLACK)
    screen.blit(txt2, (50, QUEUE_Y - 50))
    for item in queue_items:
        item.draw()

    txt3 = FONT.render("Dequeue Result:", True, BLACK)
    screen.blit(txt3, (50, 460))
    x = 50
    for v in dequeue_result:
        pygame.draw.rect(screen, GREEN, (x, RESULT_Y, 60, 40))
        screen.blit(FONT.render(str(v), True, BLACK), (x + 20, RESULT_Y + 8))
        x += 80

    btn_enqueue.draw()
    btn_dequeue.draw()

    pygame.display.flip()
    clock.tick(FPS)
