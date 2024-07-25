import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

wid,hei = 1000,600  

pygame.mixer.music.load('bgmusic.mp3')
pygame.mixer.music.play(-1)

guns = pygame.mixer.Sound('gun_shot.mp3')
gunl = pygame.mixer.Sound('gun_load.mp3')
explode = pygame.mixer.Sound('ship_death.mp3')
star_hit = pygame.mixer.Sound('star_hit.mp3')

guns.set_volume(0.1)
gunl.set_volume(0.5)
explode.set_volume(0.5)
star_hit.set_volume(0.5)


win = pygame.display.set_mode((wid,hei))


pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load('space.jpg'), (wid,hei))

flame = pygame.transform.scale(pygame.image.load('flame.png'), (60,60))



# Player Stats
player_wid = 35
player_hei = 50
player_vel = 6

# Star Stats
star_wid = 20
star_hei = 20
star_vel = 3

bul_vel = 6
bul_wid = 5

font = pygame.font.SysFont('comicsans', 30)
PLAYER_IMG = pygame.transform.scale(pygame.image.load("ship.png"), (player_wid, player_hei))
star_img = pygame.transform.scale(pygame.image.load('asteroid.png'), (star_wid, star_hei))

PLAYER_MASK = pygame.mask.from_surface(PLAYER_IMG)
star_mask = pygame.mask.from_surface(star_img)


def boost(x,y):
    
    win.blit(flame, (x,y))
    


def draw(player, elapsed_time, stars, bullets):
    
    win.blit(BG, (0,0))
    

    time_text = font.render(f"Time : {round(elapsed_time)}s", 1, 'white')

    win.blit(time_text, (10,10))

    win.blit(PLAYER_IMG, (player.x, player.y))
    
    for star in stars:
    
        win.blit(star_img, (star.x, star.y))
    
    for bull in bullets:
    
        pygame.draw.rect(win,'yellow', bull)

    pygame.display.update()


def start():
    
    while True:
        
        for event in pygame.event.get():
      
            if event.type == pygame.QUIT:
       
                pygame.quit()
            
                sys.exit()


        begin_text = font.render('Press Space to Play', 1 ,'yellow') 
      
        win.blit(begin_text, (wid/2 - begin_text.get_width()/2, hei/2 - begin_text.get_height()/2))
        
        
        keys = pygame.key.get_pressed()
     
        if keys[pygame.K_SPACE]:          
        
            pygame.display.flip()
            break

        pygame.display.update()

def dieded():

    lost_text = font.render('You\'re Die!', 1 ,'white')
           
    win.blit(lost_text, (wid/2 - lost_text.get_width()/2, hei/2 - lost_text.get_height()/2))
           
    pygame.display.update()
    pygame.mixer.music.stop
    pygame.time.delay(2000)


def restart():

    restart_text = font.render('Press J to restart', 1,'blue')
    win.fill('black')
    win.blit(restart_text, (wid/2 - restart_text.get_width()/2, hei/2 - restart_text.get_height()/2))

    pygame.display.flip()

    uhhh = True

    while uhhh:

        for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                
                    run=False
                    break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_j]:

            gunl.play()
            main()



def main():
   
    run = True
    win.fill('black')
    start()

    player = pygame.Rect(200, hei - player_hei - 40, player_wid, player_hei)
    cr = 10

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    bullets = []
    
    hit = False
    shot = False

    nstar = 3

    while run:
        
        star_count += clock.tick(60)
      
        elapsed_time = time.time() - start_time
    
        star_vel = 3

        if elapsed_time > 30:
            nstar = 4

        if star_count > star_add_increment:
           
            for _ in range(nstar):
               
                star_x = random.randint(0, wid - star_wid)
               
                star = pygame.Rect(star_x, -star_hei, star_wid, star_hei)
               
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
         
            star_count = 0


        for event in pygame.event.get():
         
            if event.type == pygame.QUIT:
              
                run=False
                break

        keys = pygame.key.get_pressed()
      
        if keys[pygame.K_a] and player.x - player_vel >= 0:
            
            player.x -= player_vel 
            
        elif keys[pygame.K_d] and player.x + player_vel + player_wid <= wid:
          
            player.x += player_vel

        elif keys[pygame.K_w]:
            
            star_vel += 2
           
            win.blit(flame, (player.x - player_wid/2 , player.y + player_hei/1.5))

            pygame.display.update()

        elif keys[pygame.K_s]:
          
            bull = pygame.Rect(player.x + player_wid/2, player.y - 5, bul_wid, star_hei)
          
            if len(bullets) == 0:
              
                bullets.append(bull)
                guns.play()

        for bull in bullets:

            bull.y -= bul_vel
            
            if bull.y < 0:
               
                bullets.remove(bull)
            


        for star in stars[:]:
            

            offset = (star.x - player.x, star.y - player.y)
            star.y += star_vel
           
            if star.y > hei:
              
                stars.remove(star)
            
            if len(bullets) != 0:
                
                if star.colliderect(bull):
                   
                    stars.remove(star)
                    star_hit.play()
                    bullets.remove(bull)

            elif PLAYER_MASK.overlap(star_mask, offset):
               
                explode.play()
                stars.remove(star)
                hit = True
                break

        if hit:
            
            dieded()
            restart()
            break           


        draw(player, elapsed_time, stars, bullets)

    pygame.quit()


if __name__ == '__main__':
    
    main()