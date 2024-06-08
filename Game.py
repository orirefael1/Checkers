import pygame
from Graphics import *
from Checkers import Checkers
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from MinMax import *
from AlphaBeta import *
from DQN_Agent import *
import time


import time
 
FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
environment = Checkers()
graphics = Graphics(win, board = environment.state.board)
File_Num = 4
file = f'Data/params_{File_Num}.pth'


# player1 = Human_Agent(player=1, env = environment)
#player1 = Random_Agent(player=1, env = environment)
#player1 = MinMax(player=1, depth=1, env = environment)
# player1 = AlphaBeta(player=1, depth=8, env = environment)
#player1 = DQN_Agent(player=1, parametes_path="Data/params_4.pth", env=environment, train=False)
#player2 = Human_Agent(player=2, env = environment)
# player2 = Random_Agent(player=2, env = environment)
#player2 = MinMax(player=2, depth=3, env = environment)
#player2 = AlphaBeta(player=2, depth=5, env = environment)
#player2 = DQN_Agent(player=2, parametes_path="Data/params_10.pth", env=environment, train=False)

player1 = None
player2 = None

def main (p1, p2):
    global player1, player2
    player1 = p1
    player2 = p2

    run = True
    clock = pygame.time.Clock()
    graphics.draw(graphics.board)
    player = player1
    steps = 0
    while(run):
        clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
               run = False
               break
               
        action = player.get_Action(events=events, graphics= graphics, state= environment.state)
        if action:
            environment.move(action, environment.state)
            steps +=1
            player = switchPlayers(player)
            #print (player.player)
            #time.sleep(.5)

        graphics.draw(graphics.board)
        pygame.display.update()
        if environment.is_end_of_game(environment.state):
            run = False
    
    time.sleep(1)
    pygame.quit()
    print(steps)
    print("End of game")
    score1, score2 = environment.state.score()
    print ("player 1: score = ", score1)
    print ("player 2: score = ", score2)
    if score1 > score2:
        print("win! : player 1")
    else: 
        print("win! : player 2")
    if score1 == score2:
        print("draw!")
    


def switchPlayers(player):
    if player == player1:
       return player2
    else:
        return player1
    
def GUI ():
    global player1, player2
    # player1 = Human_Agent(player=1, env=environment)
    # player2 = Human_Agent(player=2, env=environment)
    # player1 = MinMax(player = 1,depth = 3, env=environment)
    # player2 = MinMax(player = 2,depth = 3, env=environment)
    # player1 = AlphaBeta(player = 1,depth = 3, env=environment)
    # player2 = AlphaBeta(player = 2,depth = 3, env=environment)
    # player1 = Random_Agent(player=1, env=environment)
    # player2 = Random_Agent(player=2, env=environment)

    # model = DQN(environment)
    # model = torch.load(file)
    # player1 = DQN_Agent(player=1, parametes_path=file, train=False)
    # player2 = DQN_Agent(player=2, parametes_path=file, train=False)

    colors = [['blue', 'gray', 'gray', 'gray'], ['blue', 'gray', 'gray', 'gray']]
    player1_chosen = 0
    player2_chosen = 0
    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                if 300<pos[0]<500 and 500<pos[1]<540:
                    main(player1, player2) 
                if 100<pos[0]<300 and 200<pos[1]<240:
                    player1 = Human_Agent(player=1, env=environment)
                    player1_chosen=0
                if 500<pos[0]<700 and 200<pos[1]<240:
                    player2 = Human_Agent(player=2, env=environment)
                    player2_chosen=0
                if 100<pos[0]<300 and 250<pos[1]<290:
                    player1 = Random_Agent(player=1, env=environment)
                    player1_chosen=1
                if 500<pos[0]<700 and 250<pos[1]<290:
                    player2 = Random_Agent(player=2, env=environment)
                    player2_chosen=1
                if 100<pos[0]<300 and 300<pos[1]<340:
                    player1 = MinMax(player = 1,depth = 3, env=environment)
                    player1_chosen=2
                if 500<pos[0]<700 and 300<pos[1]<340:
                    player2 = MinMax(player = 2,depth = 3, env=environment)
                    player2_chosen=2
                if 100<pos[0]<300 and 350<pos[1]<390:
                    player1 = AlphaBeta(player=1, env=environment)
                    player1_chosen=3
                if 500<pos[0]<700 and 350<pos[1]<390:
                    player2 = AlphaBeta(player=2, env=environment)
                    player2_chosen=3
                if 100<pos[0]<300 and 400<pos[1]<440:
                    player1 = DQN_Agent(player=1, parametes_path='Data/params_4.pth', train=False, env=environment)
                    player1_chosen=4
                if 500<pos[0]<700 and 400<pos[1]<440:
                    player2 = DQN_Agent(player=2, parametes_path='Data/params_20.pth', train=False, env=environment)
                    player2_chosen=4



        colors = [['black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black']]
        colors[0][player1_chosen]='BLUE'
        colors[1][player2_chosen]='RED'




        win.fill('black')
        write(win, "Checkers", pos=(300, 50), color=WHITE, background_color=None)

        write(win, 'Player 1',(150,150),color=WHITE)
        pygame.draw.rect(win, colors[0][0], (100,200,200,40))
        write(win, 'Human', (120,200),color=WHITE)
        pygame.draw.rect(win, colors[0][1], (100,250,200,40))
        write(win, 'Random', (120,250),color=WHITE)
        pygame.draw.rect(win, colors[0][2], (100,300,200,40))
        write(win, 'Min_Max', (120,300),color=WHITE)
        pygame.draw.rect(win, colors[0][3], (100,350,200,40))
        write(win, 'Alpha_Beta', (120,350),color=WHITE)
        pygame.draw.rect(win, colors[0][4], (100,400,200,40))
        write(win, 'DQN', (120,400),color=WHITE)

        write(win, 'Player 2',(550,150),color=WHITE)
        pygame.draw.rect(win, colors[1][0], (500,200,200,40))
        write(win, 'Human', (520,200),color=WHITE)
        pygame.draw.rect(win, colors[1][1], (500,250,200,40))
        write(win, 'Random', (520,250),color=WHITE)
        pygame.draw.rect(win, colors[1][2], (500,300,200,40))
        write(win, 'Min_Max', (520,300),color=WHITE)
        pygame.draw.rect(win, colors[1][3], (500,350,200,40))
        write(win, 'Alpha_Beta', (520,350),color=WHITE)
        pygame.draw.rect(win, colors[1][4], (500,400,200,40))
        write(win, 'DQN', (520,400),color=WHITE)

        
        pygame.draw.rect(win, 'gray', (300,500,200,40))
        write(win, 'Play', (350,500),color=BLACK)


        pygame.display.update()

    pygame.quit()

def write (surface, text, pos = (50, 20), color = BLACK, background_color = None):
    font = pygame.font.SysFont("arial", 36)
    text_surface = font.render(text, True, color, background_color)
    surface.blit(text_surface, pos)

if __name__ == '__main__':
    GUI()
    
