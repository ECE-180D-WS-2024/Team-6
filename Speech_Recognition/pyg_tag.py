import pygame
pygame.init()

# Correctly create a screen with a tuple for the dimensions
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Tag Game")

font = pygame.font.SysFont("Arial", 40, italic=True)
clock = pygame.time.Clock()
Snds = 2000

pos = [90, 120, 90, 90]
rectPos = [330, 300, 200, 100]
tPos = [90, 600, 90, 90]

while True:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Correctly assign the pressed keys to the variable
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        pos[1] -= 5
    if pressed[pygame.K_s]:
        pos[1] += 5
    if pressed[pygame.K_a]:
        pos[0] -= 5
    if pressed[pygame.K_d]:
        pos[0] += 5

    if pressed[pygame.K_UP]:
        tPos[1] -= 3
    if pressed[pygame.K_DOWN]:
         tPos[1] += 3
    if pressed[pygame.K_LEFT]:
         tPos[0] -= 3
    if pressed[pygame.K_RIGHT]:
         tPos[0] += 3

    # Correct typos in variable names and function calls
    pygame.draw.rect(screen, "blue", pos)
    pygame.draw.rect(screen, "green", rectPos)
    pygame.draw.rect(screen, "red", tPos)

    text = font.render("Time : ", True, "blue")
    timeText = font.render(str(Snds), True, "blue")  # Directly convert Snds to string

    # Convert lists to pygame.Rect objects before checking for collisions
    pos_rect = pygame.Rect(pos)
    tPos_rect = pygame.Rect(tPos)
    rectPos_rect = pygame.Rect(rectPos)

    # Now use the colliderect method with these Rect objects
    if tPos_rect.colliderect(pos_rect):
        print("Red Caught Blue, Red Won!")
        pygame.quit()
        quit()

    
    if rectPos_rect.colliderect(pos_rect) or tPos_rect.colliderect(pos_rect):
        pygame.time.delay(4)


    if tPos[0] <= 0:
        tPos[0] = 0
    elif tPos[0] >= 1310:
        tPos[0] = 1310
    if tPos[1] <= 2:
        tPos[1] = 2
    elif tPos[1] >= 715:
        tPos[1] = 715

    if pos[0] <= 0:
        pos[0] = 0
    elif pos[0] >= 1310:
        pos[0] = 1310
    if pos[1] <= 2:
        pos[1] = 2
    elif pos[1] >= 715:
        pos[1] = 715

    

    screen.blit(text, (1280, 40))
    screen.blit(timeText, (1280, 80))
    
    if Snds == 0:
        print("The timer ran out, Blue Won")
        pygame.quit()
        quit()

    Snds -= 1
    clock.tick(1000)
    pygame.time.delay(10)
    pygame.display.update()  # Correct the typo here
