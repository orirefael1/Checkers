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


# player1 = Human_Agent(player=1, env = environment)
#player1 = Random_Agent(player=1, env = environment)
#player1 = MinMax(player=1, depth=1, env = environment)
#player1 = AlphaBeta(player=1, depth=1, env = environment)
player1 = DQN_Agent(player=1, parametes_path="Data/params_4.pth", env=environment, train=False)
#player2 = Human_Agent(player=2, env = environment)
player2 = Random_Agent(player=2, env = environment)
#player2 = MinMax(player=2, depth=3, env = environment)
#player2 = AlphaBeta(player=2, depth=5, env = environment)
#player2 = DQN_Agent(player=2, parametes_path="Data/params_10.pth", env=environment, train=False)

#player2.load_params("Data/params_15.pth")

def main ():
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

if __name__ == '__main__':
    main()
    
