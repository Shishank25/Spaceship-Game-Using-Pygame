import pygame
import time
import random
pygame.font.init()

wid,hei = 1000,600  


win = pygame.display.set_mode((wid,hei))


pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load('space.jpg'), (wid,hei))
flame = pygame.transform.scale(pygame.image.load('flame.png'), (60,60))



# Player Stats
player_wid = 35
player_hei = 50
player_vel = 6

# Star Stats
star_wid = 10
star_hei = 10
star_vel = 3

font = pygame.font.SysFont('comicsans', 30)


def boost(x,y):
    win.blit(flame, (x,y))
    


def draw(player, elapsed_time, stars):
    
    win.blit(BG, (0,0))

    time_text = font.render(f"Time : {round(elapsed_time)}s", 1, 'white')
    win.blit(time_text, (10,10))

    pygame.draw.rect(win, 'red', player)
    
    for star in stars:
        pygame.draw.rect(win, 'white', star)

    pygame.display.update()


def main():
   
    run = True
    w = 0

    player = pygame.Rect(200, hei - player_hei - 40, player_wid, player_hei)
    cr = 10

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        star_vel = 3

        if star_count > star_add_increment:
           
            for _ in range(3):
               
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
            ##  circle_center = (player.x + player_wid/2, player.y + player_hei + 5)
            ##  pygame.draw.circle(win, 'orange', circle_center, cr)
            pygame.display.update()


        for star in stars[:]:
          
            star.y += star_vel
            if star.y > hei:
                stars.remove(star)

            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            
            lost_text = font.render('You Dieded!', 1 ,'white')
           
            win.blit(lost_text, (wid/2 - lost_text.get_width()/2, hei/2 - lost_text.get_height()/2))
           
            pygame.display.update()
          
            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == '__main__':
    main()