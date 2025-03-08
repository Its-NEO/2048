import pygame
import random 

size = 320
white = (255, 255, 255)
brown = (43, 23, 0)

cells = 5
total = cells*cells
WIN_CONDITION = 2**11    # 2048

pygame.init()
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.Font(size=50)
running = True
game_over = False
game_won = False

def fill():
  screen.fill("beige")
  for i in range(1, cells):
    pygame.draw.line(screen, brown, (size / cells * i, 0), (size / cells * i, size))
  for i in range(1, cells):
    pygame.draw.line(screen, brown, (0, size / cells * i), (size, size / cells * i))

fill()
state = [0 for _ in range(total)]

def start() -> None:
  global state
  state = [0 for _ in range(total)]
  while True:
    i = random.randrange(0, total)
    j = random.randrange(0, total)

    if i != j:
      state[i] = 2
      state[j] = 2
      break

def next() -> bool:
  empty = []
  for i, _ in enumerate(state):
    if state[i] == 0:
      empty.append(i)
  
  if len(empty) == 0:
    return False
  
  random_empty = random.randrange(0, len(empty))
  chosen = empty[random_empty]

  state[chosen] = 2
  return True

def check_win() -> bool:
  for value in state:
    if value >= WIN_CONDITION:
      return True
  return False

def check_moves_possible() -> bool:
  if 0 in state:
    return True
  
  for row in range(cells):
    for col in range(cells - 1):
      idx = row * cells + col
      if state[idx] == state[idx + 1]:
        return True
  
  for col in range(cells):
    for row in range(cells - 1):
      idx = row * cells + col
      if state[idx] == state[idx + cells]:
        return True
  
  return False

def get_coordinate(row: int, col: int, surface_size: list[int]):
  return ((size / cells) * col + size / (cells * 2) - surface_size[0] / 2, 
          (size / cells) * row + size / (cells * 2) - surface_size[1] / 2)

def get_xy(index: int):
  return (index // cells, index % cells)

def repaint():
  fill()
  for i in range(total):
    x, y = get_xy(i)
    if state[i] != 0:
      text_surface = font.render(str(state[i]), False, brown)
      screen.blit(text_surface, get_coordinate(x, y, text_surface.get_size()))
  
  if game_over:
    overlay = pygame.Surface((size, size))
    overlay.set_alpha(200)
    overlay.fill(brown)
    screen.blit(overlay, (0, 0))
    
    message = "You Won!" if game_won else "Game Over"
    text_surface = font.render(message, False, white)
    text_rect = text_surface.get_rect(center=(size/2, size/2))
    screen.blit(text_surface, text_rect)

def shiftL(array: list) -> bool:
  size = len(array)
  original = array.copy()
  pos = 0

  for i in range(size):
    if array[i] != 0:
      array[pos] = array[i]
      if pos != i:
        array[i] = 0
      pos += 1
  
  return original != array

def stackL(array: list) -> bool:
  size = len(array)
  original = array.copy()
  changed = False
  
  i = 0
  while i < size - 1:
    if array[i] == array[i + 1] and array[i] != 0:
      array[i] *= 2
      array[i + 1] = 0
      changed = True
      i += 2
    else:
      i += 1
  
  pos = 0
  for i in range(size):
    if array[i] != 0:
      array[pos] = array[i]
      if pos != i:
        array[i] = 0
      pos += 1
  
  return changed or original != array

def move_left() -> bool:
  moved = False
  for row in range(cells):
    array = state[row*cells : row*cells + cells]
    shifted = shiftL(array)
    stacked = stackL(array)
    state[row*cells : row*cells + cells] = array
    if shifted or stacked:
      moved = True
  return moved

def move_right() -> bool:
  moved = False
  for row in range(cells):
    array = state[row*cells : row*cells + cells]
    array.reverse()
    shifted = shiftL(array)
    stacked = stackL(array)
    array.reverse()
    state[row*cells : row*cells + cells] = array
    if shifted or stacked:
      moved = True
  return moved

def move_up() -> bool:
  moved = False
  for col in range(cells):
    array = [state[i] for i in range(col, total, cells)]
    shifted = shiftL(array)
    stacked = stackL(array)
    
    idx = 0
    for i in range(col, total, cells):
      state[i] = array[idx]
      idx += 1
        
    if shifted or stacked:
      moved = True
  return moved

def move_down() -> bool:
  moved = False
  for col in range(cells):
    array = [state[i] for i in range(col, total, cells)]
    array.reverse()
    shifted = shiftL(array)
    stacked = stackL(array)
    array.reverse()
    
    idx = 0
    for i in range(col, total, cells):
      state[i] = array[idx]
      idx += 1
        
    if shifted or stacked:
      moved = True
  return moved

start()
repaint()
pygame.display.flip()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    
    elif event.type == pygame.KEYDOWN and not game_over:
      moved = False
      
      if event.key == pygame.K_w:
        print("PRESS UP")
        moved = move_up()
      elif event.key == pygame.K_a:
        print("PRESS LEFT")
        moved = move_left()
      elif event.key == pygame.K_s:
        print("PRESS DOWN")
        moved = move_down()
      elif event.key == pygame.K_d:
        print("PRESS RIGHT")
        moved = move_right()
      elif event.key == pygame.K_r:
        start()
        game_over = False
        game_won = False
        moved = True
      
      if moved:
        if check_win():
          game_won = True
          game_over = True
          print("You won!")
        else:
          next()
          
          if not check_moves_possible():
            game_over = True
            print("Game over!")
      
      repaint()
      pygame.display.flip()
    
    elif event.type == pygame.KEYDOWN and game_over:
      if event.key == pygame.K_r:
        start()
        game_over = False
        game_won = False
        repaint()
        pygame.display.flip()

  clock.tick(60)

pygame.quit()