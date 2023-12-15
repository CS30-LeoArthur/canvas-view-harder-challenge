import pygame

# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = SCREEN_HEIGHT - 50
WORLD_WIDTH = 1800
platform_list = []
    
def rectCollide(rect1, rect2):
    return rect1.x < rect2.x + rect2.width and rect1.y < rect2.y + rect2.height and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

def check_collision(object1, object2):
    for i in range(len(object1)):
        if rectCollide(object1[i], object2):
            return i
    return -1

class Player():
    def __init__(self, x, y, width, height, change_x, change_y, view, jump_count):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.change_x = change_x
        self.change_y = change_y
        self.view = view
        self.jump_count = jump_count
    
    def jump(self):
        if self.jump_count > 0:
            self.change_y = -7
            self.jump_count = 0

    def go_left(self):
        self.change_x = -3
    
    def go_right(self):
        self.change_x = 3

    def hzstop(self):
        self.change_x = 0
    
    def vt_default(self):
        self.change_y = 0.1

    def check_vertical_platform_collsion(self):
        platform_index = check_collision(platform_list, self)
        if platform_index != -1:
            self.jump_count += 1
            if self.change_y > 0:
                self.vt_default()
                self.y = platform_list[platform_index].y - self.height
            elif self.change_y < 0:
                self.vt_default()
                self.y = platform_list[platform_index].y + platform_list[platform_index].height
    
    def check_horizontal_platform_collision(self):
        platform_index = check_collision(platform_list, self)
        if platform_index != -1:
            if self.change_x > 0:
                self.x = platform_list[platform_index].x - self.width
            elif self.change_x < 0:
                self.x = platform_list[platform_index].x + platform_list[platform_index].width
    
    def world_edge_collision(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WORLD_WIDTH:
            self.x = WORLD_WIDTH - self.width

    def view_vertical_edge_collision(self):
        if self.view[0] < 0:
            self.view[0] = 0
        elif self.view[0] > WORLD_WIDTH - SCREEN_WIDTH:
            self.view[0] = WORLD_WIDTH - SCREEN_WIDTH
    
    def view_horizontal_edge_collision(self):
        if self.view[1] > GROUND_HEIGHT - 500:
            self.view[1] = GROUND_HEIGHT - 500
        

    def update(self):
        self.change_y = min(5, self.change_y + 0.2)
        self.y += self.change_y 
        self.check_vertical_platform_collsion()

        self.x += self.change_x
        self.check_horizontal_platform_collision()

        self.world_edge_collision()

        view_x = self.x - 400
        view_y = self.y - 300
        self.view = [view_x, view_y]

        self.view_horizontal_edge_collision()
        self.view_vertical_edge_collision()
    
    def draw_player(self, screen):
        pygame.draw.rect(screen, RED, [self.x - self.view[0], self.y - self.view[1], self.width, self.height])

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw_platform(self, screen, player):
        pygame.draw.rect(screen, GREY, [self.x - player.view[0], self.y - player.view[1], self.width, self.height])

def make_platforms():
    platform_list.append(Platform(0, GROUND_HEIGHT, WORLD_WIDTH, 200))
    platform_list.append(Platform(150, GROUND_HEIGHT - 100, 150, 20))
    platform_list.append(Platform(400, GROUND_HEIGHT - 200, 150, 20))
    platform_list.append(Platform(650, GROUND_HEIGHT - 300, 150, 20))
    platform_list.append(Platform(900, GROUND_HEIGHT - 200, 150, 20))
    platform_list.append(Platform(1150, GROUND_HEIGHT - 100, 150, 20))
    platform_list.append(Platform(1400, GROUND_HEIGHT - 200, 150, 20))
    platform_list.append(Platform(900, GROUND_HEIGHT - 400, 150, 20))
    platform_list.append(Platform(1150, GROUND_HEIGHT - 500, 150, 20))
    platform_list.append(Platform(1400, GROUND_HEIGHT - 600, 150, 20))
    platform_list.append(Platform(400, GROUND_HEIGHT - 400, 150, 20))
    platform_list.append(Platform(150, GROUND_HEIGHT - 500, 150, 20))
    platform_list.append(Platform(400, GROUND_HEIGHT - 600, 150, 20))
    platform_list.append(Platform(650, GROUND_HEIGHT - 700, 150, 20))
    platform_list.append(Platform(900, GROUND_HEIGHT - 600, 150, 20))
    platform_list.append(Platform(1150, GROUND_HEIGHT - 500, 150, 20))


def main():
    # Initialize pygame
    pygame.init()
    # Set screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    # Variables
    frame_count = 0
    
    player = Player(SCREEN_WIDTH / 2, GROUND_HEIGHT + 20, 20, 20, 0, 0, 0, 1)

    make_platforms()
    # create loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_w:
                    player.jump()    
            # Stop player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0 or event.key == pygame.K_d and player.change_x > 0:
                    player.hzstop()
        # Logic

        player.update()
        
        # Drawing
        screen.fill(WHITE)
        for i in range(len(platform_list)):
            platform_list[i].draw_platform(screen, player)
        player.draw_player(screen)

        pygame.display.flip()
        # frame rate
        frame_count += 1
        clock.tick(60)

    pygame.quit

if __name__ == "__main__":
    main()