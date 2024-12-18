import pygame
import sys
import time
import pygame.font
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slime Pet")
font = pygame.font.Font(None, 36)  # 使用默认字体，大小为36

# 加载并缩放图片
slime_image = pygame.image.load('slime.png')
slime_image = pygame.transform.scale(slime_image, (150, 150))  # 调整slime的大小

food_image = pygame.image.load('food.png')
food_image = pygame.transform.scale(food_image, (50, 50))  # 缩小food图标

water_image = pygame.image.load('water.png')
water_image = pygame.transform.scale(water_image, (50, 50))  # 缩小water图标

sleep_image = pygame.image.load('sleep.png')  # 假设你已经有了这个图片
sleep_image = pygame.transform.scale(sleep_image, (50, 50))  # 缩小sleep图标

# 定义宠物类
class SlimePet:
    def __init__(self):
        self.hunger = 50
        self.thirst = 50
        self.sleepiness = 50
        self.state = 'normal'
        self.x = width // 2  # 初始x位置
        self.y = height // 2  # 初始y位置
        self.speed = 5  # 移动速度
        self.auto_move_timer = 0  # 自动移动计时器
        self.auto_move_interval = 1000  # 自动移动间隔时间（毫秒）

    def update(self):
        # 更新宠物状态
        self.hunger += 1
        self.thirst += 1
        self.sleepiness += 1

        if self.hunger > 100:
            self.state = 'hungry'
        elif self.thirst > 100:
            self.state = 'thirsty'
        elif self.sleepiness > 100:
            self.state = 'sleepy'
        else:
            self.state = 'normal'

    def feed(self):
        print("喂食")
        self.hunger -= 20

    def drink(self):
        print("喝水")
        self.thirst -= 20

    def sleep(self):
        print("睡觉")
        self.sleepiness -= 20

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > width - slime_image.get_width():
            self.x = width - slime_image.get_width()

    def move_up(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.speed
        if self.y > height - slime_image.get_height():
            self.y = height - slime_image.get_height()

    def auto_move(self):
        # 随机选择一个方向移动
        direction = random.choice(['left', 'right', 'up', 'down'])
        if direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        elif direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()

# 创建宠物实例
pet = SlimePet()

# 游戏主循环
clock = pygame.time.Clock()
last_update_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # 检查是否点击了喂食按钮
            if width // 2 - 75 <= mouse_x <= width // 2 + 75 and height - 90 <= mouse_y <= height - 30:
                pet.feed()
            # 检查是否点击了喝水按钮
            elif width // 2 + 75 <= mouse_x <= width // 2 + 150 and height - 90 <= mouse_y <= height - 30:
                pet.drink()
            # 检查是否点击了睡觉按钮
            elif width - 60 <= mouse_x <= width and height - 60 <= mouse_y <= height:
                pet.sleep()
                print("点击了睡觉按钮")  # 添加调试信息

    current_time = time.time()
    if current_time - last_update_time > 1:  # 每秒更新一次状态
        pet.update()
        last_update_time = current_time

    # 自动移动逻辑
    if pygame.time.get_ticks() - pet.auto_move_timer > pet.auto_move_interval:
        pet.auto_move()
        pet.auto_move_timer = pygame.time.get_ticks()

    # 绘制背景
    screen.fill((255, 255, 255))

    # 绘制宠物
    screen.blit(slime_image, (pet.x, pet.y))

    # 绘制按钮
    screen.blit(food_image, (width // 2 - 75, height - 90))  # 将food图标移动到同一行
    screen.blit(water_image, (width // 2 + 75, height - 90))  # 将water图标移动到同一行
    screen.blit(sleep_image, (width - 60, height - 60))  # 将sleep图标移动到右下角

    # 绘制状态信息
    hunger_text = font.render(f"Hunger: {pet.hunger}", True, (0, 0, 0))
    thirst_text = font.render(f"Thirst: {pet.thirst}", True, (0, 0, 0))
    sleep_text = font.render(f"Sleepiness: {pet.sleepiness}", True, (0, 0, 0))

    screen.blit(hunger_text, (10, 10))
    screen.blit(thirst_text, (10, 50))
    screen.blit(sleep_text, (10, 90))

    # 更新屏幕显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)
