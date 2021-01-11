import sys

import pygame
import random

from pygame.locals import *

# set constants

# # math
frames_per_sec = 30
window_width = 800
window_height = 800
x_margin = 30
y_margin = 30
FPS = 30

# # style
# # # colors
light_gray = (225, 225, 225)
dark_gray = (160, 160, 160)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 128, 0)

# # #
background_color = white
field_color = black
box_color_cov = dark_gray  # covered box color
box_color_rev = light_gray  # revealed box color
mine_color = black
text_color1 = blue
text_color2 = red
text_color3 = black
highlight_color = green
reset_bg_color = light_gray
mine_mark_cov = red

# # # font
font_type = 'Arial'
font_size = 20

# variables - set by default for expert mode (20x20)

field_count = 20  # no. of boxes / row
box_size = 33.4  # width and height of a single box - should be 74 (9x9), 41.8 (16x16) and 33.4 (20x20)
gap_size = box_size / 10  # should be 7.4 (9x9), 4.18 (16x16) and 3.34 (20x20)
total_mines = 60

mine = pygame.image.load(r'../bomb.png')


def create_blank_field():
    field = []
    for x in range(field_count):
        field.append([])
        for y in range(field_count):
            field[x].append('[ ]')
    return field


def place_mines(field):
    mine_count = 0
    mine_list = []
    while mine_count < total_mines:
        x = random.randint(0, field_count - 1)
        y = random.randint(0, field_count - 1)
        mine_list.append([x, y])
        if mine_list.count([x, y]) > 1:
            mine_list.remove([x, y])
        else:
            field[x][y] = '[X]'
            mine_count += 1


def isMine(field, x, y):
    return field[x][y] == '[X]'


def is_in_field(a, b, maxim):
    if a >= maxim or b >= maxim:
        return False
    if a < 0 or b < 0:
        return False
    return True


def neighbours_count(field, x, y):
    # creating directional vectors
    dx = (-1, -1, -1, 0, 1, 1, 1, 0)
    dy = (-1, 0, 1, 1, 1, 0, -1, -1)
    count = 0
    for i in range(0, len(dx)):
        if is_in_field(x + dx[i], y + dy[i], field_count):
            if field[x + dx[i]][y + dy[i]] == '[X]':
                count += 1
    return count


def place_numbers(field):
    count = 0
    for x in range(field_count):
        for y in range(field_count):
            if isMine(field, x, y):
                count = neighbours_count(field, x, y)
            field[x][y] = '[%s]' % count


def boolean_revealed_boxes(val):
    revealed_boxes = []
    for i in range(field_count):
        revealed_boxes.append([val] * field_count)
    return revealed_boxes


def game_setup():
    mine_field = create_blank_field()
    place_mines(mine_field)
    place_numbers(mine_field)
    zero_list_xy = []
    marked_mines = []
    revealed_boxes = boolean_revealed_boxes(False)

    return mine_field, zero_list_xy, revealed_boxes, marked_mines


def key_pressed():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def terminate():
    pygame.quit()
    sys.exit()


# getting positions
def get_left_top_xy(box_x, box_y):
    left = x_margin + box_x * (box_size + gap_size)
    top = y_margin + box_y * (box_size + gap_size)
    return left, top


def get_center_xy(box_x, box_y):
    # get center coordinates for drawing mine boxes

    center_x = x_margin + box_size / 2 + box_x * (box_size + gap_size)
    center_y = y_margin + box_size / 2 + box_y * (box_size + gap_size)
    return center_x, center_y


def draw_field():
    # draws field GUI and reset button

    for box_x in range(field_count):
        for box_y in range(field_count):
            left, top = get_left_top_xy(box_x, box_y)
            pygame.draw.rect(display_surface, box_color_rev, (left, top, box_size, box_size))

    display_surface.blit(reset_surface, reset_rect)
    display_surface.blit(show_surf, show_rect)


def draw_text(text, font, color, surface, x, y):
    # function to easily draw text and also return object & rect pair

    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def draw_mines_numbers(field):
    # draws mines and numbers onto GUI
    # field should have mines and numbers

    half = int(box_size * 0.5)
    quarter = int(box_size * 0.25)
    eighth = int(box_size * 0.125)

    for box_x in range(field_count):
        for box_y in range(field_count):
            left, top = get_left_top_xy(box_x, box_y)
            center_x, center_y = get_center_xy(box_x, box_y)
            if field[box_x][box_y] == '[X]':
                print('found xxx')
                display_surface.blit(mine, (left, top))
                # pygame.draw.circle(display_surface, mine_color, (left + half, top + half), quarter)
                # pygame.draw.circle(display_surface, white, (left + half, top + half), eighth)
                # pygame.draw.line(display_surface, mine_color, (left + eighth, top + half),
                #                  (left + half + quarter + eighth, top + half))
                # pygame.draw.line(display_surface, mine_color, (left + half, top + eighth),
                #                  (left + half, top + half + quarter + eighth))
                # pygame.draw.line(display_surface, mine_color, (left + quarter, top + quarter),
                #                  (left + half + quarter, top + half + quarter))
                # pygame.draw.line(display_surface, mine_color, (left + quarter, top + half + quarter),
                #                  (left + half + quarter, top + quarter))
            else:
                for i in range(1, 9):
                    if field[box_x][box_y] == '[' + str(i) + ']':
                        if i in range(1, 3):
                            text_color = text_color1
                        else:
                            text_color = text_color2
                        draw_text(str(i), basic_font, text_color, display_surface, center_x, center_y)


def reveal_adjacent_boxes(revealed_boxes, box_x, box_y):
    # modifies revealed_boxes data structure so that all adjacent boxes to (box_x, box_y) are set to True

    if box_x != 0:
        revealed_boxes[box_x - 1][box_y] = True
        if box_y != 0:
            revealed_boxes[box_x - 1][box_y - 1] = True
        if box_y != field_count - 1:
            revealed_boxes[box_x - 1][box_y + 1] = True
    if box_x != field_count - 1:
        revealed_boxes[box_x + 1][box_y] = True
        if box_y != 0:
            revealed_boxes[box_x + 1][box_y - 1] = True
        if box_y != field_count - 1:
            revealed_boxes[box_x + 1][box_y + 1] = True
    if box_y != 0:
        revealed_boxes[box_x][box_y - 1] = True
    if box_y != field_count - 1:
        revealed_boxes[box_x][box_y + 1] = True


def get_adjacent_boxes_xy(mine_field, box_x, box_y):
    # get box XY coordinates for all adjacent boxes to (box_x, box_y)

    adjacent_boxes_xy = []

    if box_x != 0:
        adjacent_boxes_xy.append([box_x - 1, box_y])
        if box_y != 0:
            adjacent_boxes_xy.append([box_x - 1, box_y - 1])
        if box_y != field_count - 1:
            adjacent_boxes_xy.append([box_x - 1, box_y + 1])
    if box_x != field_count - 1:
        adjacent_boxes_xy.append([box_x + 1, box_y])
        if box_y != 0:
            adjacent_boxes_xy.append([box_x + 1, box_y - 1])
        if box_y != field_count - 1:
            adjacent_boxes_xy.append([box_x + 1, box_y + 1])
    if box_y != 0:
        adjacent_boxes_xy.append([box_x, box_y - 1])
    if box_y != field_count - 1:
        adjacent_boxes_xy.append([box_x, box_y + 1])

    return adjacent_boxes_xy


def show_numbers(revealed_boxes, mine_field, box_x, box_y, zero_list_xy):
    # modifies revealedBox data strucure if chosen box_x & box_y is [0]
    # show all boxes using recursion

    revealed_boxes[box_x][box_y] = True
    reveal_adjacent_boxes(revealed_boxes, box_x, box_y)
    for i, j in get_adjacent_boxes_xy(mine_field, box_x, box_y):
        if mine_field[i][j] == '[0]' and [i, j] not in zero_list_xy:
            zero_list_xy.append([i, j])
            show_numbers(revealed_boxes, mine_field, i, j, zero_list_xy)


def show_mines(revealed_boxes, mine_field, box_x, box_y):
    # modifies revealedBox data strucure if chosen box_x & box_y is [X]

    for i in range(field_count):
        for j in range(field_count):
            if mine_field[i][j] == '[X]':
                revealed_boxes[i][j] = True


def drawCovers(revealed_boxes, marked_mines):
    # uses revealedBox FIELDWIDTH x FIELDHEIGHT data structure to determine whether to draw box covering mine/number
    # draw red cover instead of gray cover over marked mines

    for box_x in range(field_count):
        for box_y in range(field_count):
            if not revealed_boxes[box_x][box_y]:
                left, top = get_left_top_xy(box_x, box_y)
                if [box_x, box_y] in marked_mines:
                    pygame.draw.rect(display_surface, mine_mark_cov, (left, top, box_size, box_size))
                else:
                    pygame.draw.rect(display_surface, box_color_cov, (left, top, box_size, box_size))


def draw_button(text, color, bgcolor, center_x, center_y):
    # similar to drawText but text has bg color and returns obj & rect

    but_surf = basic_font.render(text, True, color, bgcolor)
    but_rect = but_surf.get_rect()
    but_rect.centerx = center_x
    but_rect.centery = center_y

    return but_surf, but_rect


def get_box_at_pixel(x, y):
    # gets coordinates of box at mouse coordinates

    for box_x in range(field_count):
        for box_y in range(field_count):
            left, top = get_left_top_xy(box_x, box_y)
            box_rect = pygame.Rect(left, top, box_size, box_size)
            if box_rect.collidepoint(x, y):
                return box_x, box_y
    return None, None


def highlightBox(box_x, box_y):
    # highlight box when mouse hovers over it

    left, top = get_left_top_xy(box_x, box_y)
    pygame.draw.rect(display_surface, highlight_color, (left, top, box_size, box_size), 4)


def highlightButton(but_rect):
    # highlight button when mouse hovers over it

    line_width = 4
    pygame.draw.rect(display_surface, highlight_color, (
        but_rect.left - line_width, but_rect.top - line_width, but_rect.width + 2 * line_width,
        but_rect.height + 2 * line_width),
                     line_width)


def gameWon(revealed_boxes, mine_field):
    # check if player has revealed all boxes

    not_mine_count = 0

    for box_x in range(field_count):
        for box_y in range(field_count):
            if revealed_boxes[box_x][box_y]:
                if mine_field[box_x][box_y] != '[X]':
                    not_mine_count += 1

    if not_mine_count >= (field_count * field_count) - total_mines:
        return True
    else:
        return False


def game_over_animation(mine_field, revealed_boxes, marked_mines, result):
    # makes background flash red (loss) or blue (win)

    orig_surf = display_surface.copy()
    flash_surf = pygame.Surface(display_surface.get_size())
    flash_surf = flash_surf.convert_alpha()
    animation_speed = 20

    if result == 'WIN':
        r, g, b = blue
    else:
        r, g, b = red

    for i in range(5):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animation_speed * step):  # animation loop
                key_pressed()
                flash_surf.fill((r, g, b, alpha))
                display_surface.blit(orig_surf, (0, 0))
                display_surface.blit(flash_surf, (0, 0))
                pygame.draw.rect(display_surface, field_color, (
                    x_margin - 5, y_margin - 5, (box_size + gap_size) * field_count + 5,
                    (box_size + gap_size) * field_count + 5))
                draw_field()
                draw_mines_numbers(mine_field)

                # tipFont = pygame.font.SysFont(font_type, 16)  ## not using BASICFONT - too big
                # drawText('Tip: Highlight a box and press space (rather than click the mouse)', tipFont, text_color3,
                #          display_surface, window_width / 2, window_height - 60)
                # drawText('to mark areas that you think contain mines.', tipFont, text_color3, display_surface,
                #          window_width / 2, window_height - 40)

                RESET_SURF, RESET_RECT = draw_button('RESET', text_color3, reset_bg_color, window_width / 2,
                                                     window_height - 120)
                SHOW_SURF, SHOW_RECT = draw_button('SHOW ALL', text_color3, reset_bg_color, window_width / 2,
                                                   window_height - 95)
                drawCovers(revealed_boxes, marked_mines)
                pygame.display.update()
                fps_clock.tick(FPS)


def main():
    global fps_clock, display_surface, basic_font, reset_surface, reset_rect, show_surf, show_rect
    pygame.init()
    pygame.display.set_caption('Minesweeper Python Project')
    fps_clock = pygame.time.Clock()
    display_surface = pygame.display.set_mode((window_width, window_height))
    basic_font = pygame.font.SysFont(font_type, font_size)

    reset_surface, reset_rect = draw_button('RESET', text_color3, reset_bg_color, x_margin + 25, 20)
    show_surf, show_rect = draw_button('SHOW ALL', text_color3, reset_bg_color, x_margin + 110, 20)

    # set up mouse events
    cursor_x = 0
    cursor_y = 0

    # data structures

    mine_field, zero_list_xy, revealed_boxes, marked_mines = game_setup()

    display_surface.fill(background_color)

    while True:
        key_pressed()

        mouse_right_clicked = False
        mouse_left_clicked = False

        # also need buttons for: RESET, SURRENDER (show all), 9x9, 16x16, 20x20

        # draw field
        display_surface.fill(background_color)
        pygame.draw.rect(display_surface,
                         field_color,
                         (x_margin, y_margin, 700, 700)
                         )
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                cursor_x, cursor_y = event.pos
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
                cursor_x, cursor_y = event.pos
                mouse_left_clicked = True
                print("Left click at: ", event.pos)
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:  # right click
                cursor_x, cursor_y = event.pos
                mouse_right_clicked = True
                print("Right click at: ", event.pos)
                
        drawCovers(revealed_boxes, marked_mines)

        # mine marker tip
        tipFont = pygame.font.SysFont(font_type, 16)  # not using BASICFONT - too big
        # drawText('Tip: Highlight a box and press space (rather than click the mouse)', tipFont, text_color3, 
        # display_surface, window_width / 2, window_height - 60) drawText('to mark areas that you think contain 
        # mines.', tipFont, text_color3, display_surface, window_width / 2, window_height - 40) 

        # determine boxes at clicked areas
        box_x, box_y = get_box_at_pixel(cursor_x, cursor_y)

        # mouse not over a box in field
        if (box_x, box_y) == (None, None):

            # check if reset box is clicked
            if reset_rect.collidepoint(cursor_x, cursor_y):
                highlightButton(reset_rect)
                if mouse_right_clicked:
                    mine_field, zero_list_xy, revealed_boxes, marked_mines = game_setup()

            # check if show box is clicked
            if show_rect.collidepoint(cursor_x, cursor_y):
                highlightButton(show_rect)
                if mouse_right_clicked:
                    revealed_boxes = boolean_revealed_boxes(True)

        # mouse currently over box in field
        else:

            # highlight unrevealed box
            if not revealed_boxes[box_x][box_y]:
                highlightBox(box_x, box_y)

                # mark mines
                if mouse_left_clicked:
                    marked_mines.append([box_x, box_y])

                # reveal clicked boxes
                if mouse_right_clicked:
                    revealed_boxes[box_x][box_y] = True

                    # when 0 is revealed, show relevant boxes
                    if mine_field[box_x][box_y] == '[0]':
                        show_numbers(revealed_boxes, mine_field, box_x, box_y, zero_list_xy)

                    # when mine is revealed, show mines
                    if mine_field[box_x][box_y] == '[X]':
                        show_mines(revealed_boxes, mine_field, box_x, box_y)
                        game_over_animation(mine_field, revealed_boxes, marked_mines, 'LOSS')
                        mine_field, zero_list_xy, revealed_boxes, marked_mines = game_setup()

        # check if player has won
        if gameWon(revealed_boxes, mine_field):
            game_over_animation(mine_field, revealed_boxes, marked_mines, 'WIN')
            mine_field, zero_list_xy, revealed_boxes, marked_mines = game_setup()

        # redraw screen, wait clock tick
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
