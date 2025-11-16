import pygame
import sys

pygame.init()

# 화면 크기
WIDTH, HEIGHT = 1024, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BST Search Visualization")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (80, 150, 255)
GREEN = (120, 220, 120)
ORANGE = (255, 180, 80)
GRAY = (200, 200, 200)
DARKGRAY = (150, 150, 150)

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
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

    def draw(self):
        pygame.draw.rect(screen, DARKGRAY, (self.x, self.y, 50, 30))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x + 15, self.y - 2))


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

        self.x = WIDTH // 2
        self.y = 200
        self.target_x = self.x
        self.target_y = self.y

        self.highlight = False

    def update(self):
        self.x += (self.target_x - self.x) * 0.15
        self.y += (self.target_y - self.y) * 0.15

    def draw(self):
        color = ORANGE if self.highlight else BLUE
        pygame.draw.rect(screen, color, (self.x - 25, self.y - 15, 50, 30))
        txt = FONT.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x - 10, self.y - 17))

root = None
waiting_items = []
search_input = ""
search_message = ""


searching = False
search_path = []
search_found = False
search_index = 0
search_frame_counter = 0
SEARCH_INTERVAL = 35


def arrange_waiting():
    for i, item in enumerate(waiting_items):
        item.target_x = 80 + i * 70
        item.target_y = 80


def bst_insert(root, value):
    if root is None:
        return TreeNode(value)

    cur = root
    while True:
        if value < cur.value:
            if cur.left is None:
                cur.left = TreeNode(value)
                break
            else:
                cur = cur.left
        else:
            if cur.right is None:
                cur.right = TreeNode(value)
                break
            else:
                cur = cur.right
    return root


def collect_nodes_inorder(node, depth, nodes_list):
    if node is None:
        return
    collect_nodes_inorder(node.left, depth + 1, nodes_list)
    nodes_list.append((node, depth))
    collect_nodes_inorder(node.right, depth + 1, nodes_list)


def layout_tree(root):
    if root is None:
        return

    nodes = []
    collect_nodes_inorder(root, 0, nodes)

    margin_x = 120
    spacing_x = 80
    base_y = 200
    level_h = 80

    for idx, (node, depth) in enumerate(nodes):
        node.target_x = margin_x + idx * spacing_x
        node.target_y = base_y + depth * level_h


def draw_edges(node):
    if node is None:
        return
    for child in [node.left, node.right]:
        if child is not None:
            pygame.draw.line(
                screen,
                BLACK,
                (node.x, node.y + 15),
                (child.x, child.y - 15),
                2,
            )
    draw_edges(node.left)
    draw_edges(node.right)


def clear_highlight(node):
    if node is None:
        return
    node.highlight = False
    clear_highlight(node.left)
    clear_highlight(node.right)


def build_search_path(root, target):
    path = []
    cur = root
    while cur is not None:
        path.append(cur)
        if target == cur.value:
            return path, True
        elif target < cur.value:
            cur = cur.left
        else:
            cur = cur.right
    return path, False


def action_insert_next():
    global root
    if not waiting_items:
        return

    item = waiting_items.pop(0)
    arrange_waiting()

    v = item.value
    root_is_none = (root is None)
    root = bst_insert(root, v)
    layout_tree(root)

    def find_node(n, val):
        if n is None:
            return None
        if n.value == val:
            return n
        left = find_node(n.left, val)
        if left:
            return left
        return find_node(n.right, val)

    new_node = find_node(root, v)
    if new_node:
        if root_is_none:
            new_node.x = new_node.target_x
            new_node.y = new_node.target_y
        else:
            new_node.x = new_node.target_x
            new_node.y = new_node.target_y - 60


def action_start_search():
    global searching, search_path, search_found, search_index, search_frame_counter, search_message

    if root is None:
        search_message = "트리가 비어 있습니다."
        return
    if not search_input:
        search_message = "검색할 숫자를 입력해 주세요."
        return

    try:
        target = int(search_input)
    except ValueError:
        search_message = "정수만 입력 가능합니다."
        return

    clear_highlight(root)

    path, found = build_search_path(root, target)
    search_path = path
    search_found = found
    search_index = 0
    search_frame_counter = SEARCH_INTERVAL
    searching = True
    search_message = f"Searching: {target}"

# 이 값을 변경하면, 여러 상황을 시도 할 수 있음
initial_values = [7, 3, 10, 1, 5, 8, 12, 33]
x = 80
for v in initial_values:
    waiting_items.append(WaitingItem(v, x, 80))
    x += 70
arrange_waiting()

btn_insert = Button(750, 60, 140, 40, "Insert")
btn_search = Button(750, 120, 140, 40, "Search")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if btn_insert.is_click(pos):
                action_insert_next()
            if btn_search.is_click(pos):
                action_start_search()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                action_start_search()
            elif event.key == pygame.K_BACKSPACE:
                search_input = search_input[:-1]
            else:
                if event.unicode.isdigit():
                    if len(search_input) < 5:
                        search_input += event.unicode

    for w in waiting_items:
        w.update()

    def update_nodes(n):
        if n is None:
            return
        n.update()
        update_nodes(n.left)
        update_nodes(n.right)

    update_nodes(root)

    if searching and search_path:
        search_frame_counter += 1
        if search_frame_counter >= SEARCH_INTERVAL:
            search_frame_counter = 0

            clear_highlight(root)

            if search_index < len(search_path):
                node = search_path[search_index]
                node.highlight = True
                search_index += 1
            else:
                searching = False
                last_val = search_path[-1].value
                if search_found:
                    search_message = f"Found: {last_val}"
                else:
                    search_message = f"Not found: {search_input}"

    screen.fill(WHITE)

    txt = FONT.render("Waiting List:", True, BLACK)
    screen.blit(txt, (40, 50))
    for w in waiting_items:
        w.draw()

    txt_tree = FONT.render("Binary Search Tree (왼쪽 < 노드 < 오른쪽)", True, BLACK)
    screen.blit(txt_tree, (40, 150))

    txt_in = FONT.render("Search value, 그냥 숫자를 타이핑 하면 값이 들어가고", True, BLACK)
    screen.blit(txt_in, (40, 700))
    txt_in2 = FONT.render("Delete 키를 누르면 삭제 됩니다.", True, BLACK)
    screen.blit(txt_in2, (40, 730))
    txt_in3 = FONT.render("Search 를 누르면 값을 찾습니다.", True, BLACK)
    screen.blit(txt_in3, (40, 760))

    input_rect = pygame.Rect(800, 690, 150, 40)
    pygame.draw.rect(screen, WHITE, input_rect)
    pygame.draw.rect(screen, BLACK, input_rect, 2)
    txt_val = FONT.render(search_input if search_input else "", True, BLACK)
    screen.blit(txt_val, (input_rect.x + 10, input_rect.y + 6))

    if search_message:
        txt_msg = FONT.render(search_message, True, BLACK)
        screen.blit(txt_msg, (40, 620))

    draw_edges(root)

    def draw_nodes(n):
        if n is None:
            return
        n.draw()
        draw_nodes(n.left)
        draw_nodes(n.right)

    draw_nodes(root)


    btn_insert.draw()
    btn_search.draw()

    pygame.display.flip()
    clock.tick(FPS)
