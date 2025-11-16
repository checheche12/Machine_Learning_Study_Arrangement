import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1600, 800
TABLE_SIZE = 4

def hash_func(x):
    return x % TABLE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hash Table Visualization (Separate Chaining)")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARKGRAY = (150, 150, 150)
BLUE = (80, 150, 255)
GREEN = (120, 220, 120)
ORANGE = (255, 180, 80)
LIGHTRED = (255, 150, 150)

FONT = pygame.font.SysFont("Malgun Gothic", 24)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 12, self.rect.y + 8))

    def is_click(self, pos):
        return self.rect.collidepoint(pos)


class WaitingItem:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y

    def update(self):
        self.x += (self.target_x - self.x) * 0.15
        self.y += (self.target_y - self.y) * 0.15

    def draw(self):
        pygame.draw.rect(screen, DARKGRAY, (self.x, self.y, 60, 40))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 20, self.y + 5))

class ChainNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class HashSlot:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

        self.type = "empty"
        self.value = None 
        self.chain_head = None  
        self.highlight = False

    def draw(self):
        base_color = BLUE if self.type != "empty" else GRAY
        if self.highlight: base_color = ORANGE

        pygame.draw.rect(screen, base_color, (self.x, self.y, 60, 50))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 60, 50), 2)

        idx_txt = FONT.render(str(self.index), True, BLACK)
        screen.blit(idx_txt, (self.x + 20, self.y + 55))

        if self.type == "single":
            val = FONT.render(str(self.value), True, BLACK)
            screen.blit(val, (self.x + 20, self.y + 12))

        elif self.type == "chain":
            cur = self.chain_head
            cy = self.y + 60

            while cur:
                pygame.draw.rect(screen, GREEN, (self.x, cy, 60, 50))
                pygame.draw.rect(screen, BLACK, (self.x, cy, 60, 50), 2)

                t = FONT.render(str(cur.value), True, BLACK)
                screen.blit(t, (self.x + 20, cy + 12))

                cur = cur.next
                cy += 60


hash_table = [HashSlot(i, 80 + i * 80, 300) for i in range(TABLE_SIZE)]
waiting_items = []

search_input = ""
message = ""

inserting = False
insert_value = None
insert_index = None
insert_highlight_time = 0

searching = False
search_value = None
search_index = None
search_cur = None
search_highlight_time = 0


def start_insert():
    global inserting, insert_value, insert_index, message

    if not waiting_items or inserting or searching:
        return

    item = waiting_items.pop(0)
    v = item.value

    insert_index = hash_func(v)
    insert_value = v
    inserting = True
    message = f"삽입 시작: hash({v}) = {insert_index}"


def process_insert():
    global inserting, message

    slot = hash_table[insert_index]
    slot.highlight = True

    if slot.type == "empty":
        slot.type = "single"
        slot.value = insert_value
        message = f"{insert_value} 삽입 완료 (single)"
        inserting = False
        return

    if slot.type == "single":
        old_value = slot.value
        slot.type = "chain"
        slot.value = None
        slot.chain_head = ChainNode(old_value)

    if slot.type == "chain":
        cur = slot.chain_head
        while cur.next:
            cur = cur.next
        cur.next = ChainNode(insert_value)
        message = f"{insert_value} 체인으로 삽입"
        inserting = False


def start_search():
    global searching, search_value, search_index, search_cur, message

    if inserting or searching:
        return

    if not search_input:
        message = "검색할 숫자를 입력하세요."
        return

    try:
        search_value = int(search_input)
    except:
        message = "정수만 입력하세요."
        return

    search_index = hash_func(search_value)
    searching = True
    search_cur = None
    message = f"검색 시작: hash({search_value}) = {search_index}"


def process_search():
    global searching, message

    slot = hash_table[search_index]
    slot.highlight = True

    if slot.type == "empty":
        message = "해당 슬롯이 비어있음 → 없음"
        searching = False
        return

    if slot.type == "single":
        if slot.value == search_value:
            message = f"Found: {search_value}"
        else:
            message = f"{search_value} 없음"
        searching = False
        return

    if slot.type == "chain":
        cur = slot.chain_head
        while cur:
            if cur.value == search_value:
                message = f"Found in chain: {search_value}"
                searching = False
                return
            cur = cur.next

        message = f"{search_value} 체인에 없음"
        searching = False

# 초기 대기 값들.
initial_values = [23, 45, 12, 7, 30, 18, 50]
x = 80
for v in initial_values:
    waiting_items.append(WaitingItem(v, x, 80))
    x += 70

btn_insert = Button(780, 60, 160, 40, "Insert Next")
btn_search = Button(780, 120, 160, 40, "Search")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if btn_insert.is_click(pos):
                start_insert()
            if btn_search.is_click(pos):
                start_search()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_search()
            elif event.key == pygame.K_BACKSPACE:
                search_input = search_input[:-1]
            else:
                if event.unicode.isdigit():
                    if len(search_input) < 5:
                        search_input += event.unicode

    for w in waiting_items:
        w.update()

    for s in hash_table:
        s.highlight = False

    if inserting:
        insert_highlight_time += 1
        if insert_highlight_time > 30:
            insert_highlight_time = 0
            process_insert()

    if searching:
        search_highlight_time += 1
        if search_highlight_time > 30:
            search_highlight_time = 0
            process_search()

    screen.fill(WHITE)

    title = FONT.render("Hash Table (Separate Chaining, key % TABLE_SIZE)", True, BLACK)
    screen.blit(title, (40, 10))

    txt = FONT.render("Waiting List:", True, BLACK)
    screen.blit(txt, (40, 40))
    for w in waiting_items:
        w.draw()

    table_lbl = FONT.render("Hash Table:", True, BLACK)
    screen.blit(table_lbl, (40, 260))

    for s in hash_table:
        s.draw()

    lbl = FONT.render("Search value:", True, BLACK)
    screen.blit(lbl, (40, 680))
    lbl2 = FONT.render("검색할 값을 그냥 숫자 타이핑으로 넣어주세요.", True, BLACK)
    screen.blit(lbl2, (40, 630))

    input_rect = pygame.Rect(200, 670, 150, 40)
    pygame.draw.rect(screen, WHITE, input_rect)
    pygame.draw.rect(screen, BLACK, input_rect, 2)
    val_txt = FONT.render(search_input, True, BLACK)
    screen.blit(val_txt, (input_rect.x + 10, input_rect.y + 6))

    # message
    msg = FONT.render(message, True, BLACK)
    screen.blit(msg, (40, 720))

    btn_insert.draw()
    btn_search.draw()

    pygame.display.flip()
    clock.tick(FPS)
