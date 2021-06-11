import pygame, sys, random

def move_ground():
    window.blit(ground,(ground_x_pos,530))
    window.blit(ground,(ground_x_pos+336,530))
    window.blit(ground,(ground_x_pos+336*2,530))

def create_pipe():
    pipe_height = random.choice(random_pipe_pos)
    bottom_pipe =  pipe_surface.get_rect(midtop = (510,pipe_height))
    top_pipe =  pipe_surface.get_rect(midbottom = (510,pipe_height-200))
    return bottom_pipe, top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 530:
            window.blit(pipe_surface,pipe)
        else:
            fliped_pipe_surf = pygame.transform.flip(pipe_surface,False,True)
            window.blit(fliped_pipe_surf,pipe)

def check_collision():
    for pipe in pipes_list:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            pygame.time.delay(1000)
            hit_sound.stop()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 530:
        if bird_rect.bottom >= 530:
            fall_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,True)
    return new_bird

def bird_animation():
    new_bird_surf = bird_frames[bird_index]
    new_bird_rect = new_bird_surf.get_rect(center = (100,bird_rect.centery))
    return new_bird_surf,new_bird_rect

def display_score(game_state):
    global highscore, score, total
    if game_state == "Active":
        #score+=0.01
        score_surf = game_font.render(f"Score:{int(score)}",1,(235,235,255))
        score_rect = score_surf.get_rect(midleft = (20,50))
        window.blit(score_surf,score_rect)
    if game_state == "not-Active":
        
        score_surf = game_font.render(f"Score:{int(score)}",1,(255,255,255))
        score_rect = score_surf.get_rect(center = (250,50))
        window.blit(score_surf,score_rect)
        
        
        if int(score) >= int(highscore):
            with open('assets/highscore.txt','w') as f:
                f.write(str(int(score)))
  
        score_surf = game_font.render(f"HighScore:{int(highscore)}",1,(255,255,255))   
        score_rect = score_surf.get_rect(center= (250,500))
        window.blit(score_surf,score_rect)
        
def pipe_score_check():
    global score, can_score 
	
	
    for pipe in pipes_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 0.2
                point_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

#pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)
pygame.init()
window = pygame.display.set_mode((500,640))
icon = pygame.image.load('assets/images/favicon.ico').convert_alpha()
pygame.display.set_icon(icon)
window.fill((0,0,0))
pygame.display.set_caption("Flappy Bird")
game_font = pygame.font.Font('assets/twofont.ttf',40)
clock = pygame.time.Clock()

# Game Variables
game_over = False
ground_x_pos = 0
gravity = 0
bird_movement = 0
game_active = True
highscore = 'highscore will here in while loop'
score = 0
can_score=True

# Loading required assets
bg_image = pygame.image.load("assets/images/bg-img.png").convert_alpha()
ground = pygame.image.load("assets/images/ground.png").convert_alpha()
message = pygame.transform.scale2x(pygame.image.load("assets/images/gameover.png").convert_alpha())
message_rect = message.get_rect(center = (250,220))
bird_upflap = pygame.image.load("assets/images/yellowbird-upflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/images/yellowbird-midflap.png").convert_alpha()
bird_downflap = pygame.image.load("assets/images/yellowbird-downflap.png").convert_alpha()
bird_frames = [bird_upflap,bird_midflap,bird_downflap]
bird_index = 0
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center = (100,200))

# sounds
flap_sound = pygame.mixer.Sound('assets/sound/sfx_wing.wav')
point_sound = pygame.mixer.Sound('assets/sound/sfx_point.wav')
hit_sound = pygame.mixer.Sound('assets/sound/sfx_hit.wav')
fall_sound = pygame.mixer.Sound('assets/sound/sfx_die.wav')
# bird_surf = pygame.image.load("assets/images/yellowbird-midflap.png").convert_alpha()
# bird_surf = pygame.transform.scale2x(bird_surf) [with this we can double any image]
# bird_rect = bird_surf.get_rect(center = (100,200))

pipe_surface = pygame.image.load("assets/images/pipe-green.png").convert_alpha()
pipes_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

random_pipe_pos = [300,350,400,450]
while not game_over: # Gameloop
    with open('assets/highscore.txt','r') as f:
        highscore = f.read()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                flap_sound.play()
                gravity = 0.25
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_RETURN and game_active == False:
                game_active = True
                pipes_list.clear()
                bird_rect.center = (100,200)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipes_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surf,bird_rect = bird_animation()
        
    window.blit(bg_image,(0,-270))
    if game_active:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surf)
        window.blit(rotated_bird,bird_rect)
        game_active = check_collision()
       
        # pipe
        pipes_list = move_pipes(pipes_list)
        draw_pipes(pipes_list)
        
        pipe_score_check()
        display_score("Active")
    else:
        window.blit(message,message_rect)
        display_score("not-Active")
            
    # ground
    ground_x_pos-=1
    if ground_x_pos <= -336:
        ground_x_pos = 0
    move_ground() 
    pygame.display.update()
    clock.tick(120)

pygame.quit()
sys.exit()
