from Checkers import Checkers

from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Random_Agent import Random_Agent
import torch
from Tester import Tester



epochs = 2000000
start_epoch = 0
C = 25
learning_rate = 0.0001
batch_size = 64
env = Checkers()
MIN_Buffer = 4000

File_Num = 200
######### path player1 ########
path_load1= None
path_Save1=f'Data/params1_{File_Num}.pth'
path_best1 = f'Data/best_params1_{File_Num}.pth'
buffer_path1 = f'Data/buffer1_{File_Num}.pth'
results_path1=f'Data/results1_{File_Num}.pth'
random_results_path1 = f'Data/random_results1_{File_Num}.pth'   
path_best_random1 = f'Data/best_random_params1_{File_Num}.pth'

######### path player2 ########
path_load2= None
path_Save2=f'Data/params2_{File_Num}.pth'
path_best2 = f'Data/best_params2_{File_Num}.pth'
buffer_path2 = f'Data/buffer2_{File_Num}.pth'
results_path2=f'Data/results2_{File_Num}.pth'
random_results_path2 = f'Data/random_results2_{File_Num}.pth'   
path_best_random2 = f'Data/best_random_params2_{File_Num}.pth'


def main ():
    
    player1 = DQN_Agent(player=1, env=env,parametes_path=path_load1)
    player1_hat = DQN_Agent(player=1, env=env, train=False)
    Q1 = player1.DQN
    Q1_hat = Q1.copy() 
    Q1_hat.eval()
    player1_hat.DQN = Q1_hat

    player2 = DQN_Agent(player=2, env=env,parametes_path=path_load2)
    player2_hat = DQN_Agent(player=2, env=env, train=False)
    Q2 = player2.DQN
    Q2_hat = Q2.copy() 
    Q2_hat.eval()
    player2_hat.DQN = Q2_hat
        
    buffer1 = ReplayBuffer(path=None) # None
    buffer2 = ReplayBuffer(path=None) # None
    
    results_file = [] #torch.load(results_path)
    results = [] #results_file['results'] # []
    avgLosses1, avgLosses2 = [], [] #results_file['avglosses']     #[]
    avgLoss1, avgLoss2 = 0,0 #avgLosses[-1] #0
    loss1, loss2 = 0, 0
    loss_count1, loss_count2 = 0, 0
    tester1 = Tester(player1=player1, player2=Random_Agent(player=-1, env=env), env=env)
    tester2 = Tester(player1=Random_Agent(player=-1, env=env), player2=player2, env=env)
    random_results1, random_results2  = [], [] #torch.load(random_results_path)   # []
    best_random1, best_random2 = 0, 0 #max(random_results)
    max_steps = 200
    res = 0
    best_res = -200 
    
    # init optimizer
    optim1 = torch.optim.Adam(Q1.parameters(), lr=learning_rate)
    optim2 = torch.optim.Adam(Q2.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000*30, gamma=0.90)
    scheduler1 = torch.optim.lr_scheduler.MultiStepLR(optim1,[50*1000, 50*5000, 50*10000, 50*20000], gamma=0.5)
    scheduler2 = torch.optim.lr_scheduler.MultiStepLR(optim2,[50*1000, 50*5000, 50*10000, 50*20000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state_1 = env.get_init_state()
        state_2 = None
        step = 0
        while not env.is_end_of_game(state_1) or step > 200:
            # Sample Environement
            step += 1
            action_1 = player1.get_Action(state_1, epoch=epoch)
            after_state_1 = env.get_next_state(state=state_1, action=action_1)
            reward_1, end_of_game_1 = env.reward(after_state_1, action=action_1)
            if end_of_game_1 or step > max_steps:
                res += 1
                buffer1.push(state_1, action_1, reward_1, after_state_1, True) # when done after_state is not important. loss useses (1-done)
                buffer2.push(state_2, action_2, -reward_2, after_state_1, True)
                break
            if state_2 is not None:
                buffer2.push(state_2, action_2, -reward_2, after_state_1, end_of_game_2)
            state_2 = after_state_1
            action_2 = player2.get_Action(state=state_2)
            after_state_2 = env.get_next_state(state=state_2, action=action_2)
            reward_2, end_of_game_2 = env.reward(state=after_state_2, action=action_2)
            reward_2 = reward_2 + reward_1
            if end_of_game_2 or step > max_steps:
                res += -1
                buffer1.push(state_1, action_1, reward_2, after_state_2, True)
                buffer2.push(state_2, action_2, -reward_2, after_state_2, True)
                break
            buffer1.push(state_1, action_1, reward_2, after_state_2, end_of_game_2)
            
                
            state_1 = after_state_2

            if len(buffer1) < 1000: #MIN_Buffer:
                continue
            
            ############################ Train White NN ############################
            states, actions, rewards, next_states, dones = buffer1.sample(batch_size)
            Q_values = Q1(states[0], actions)
            next_actions = player1_hat.get_Actions(next_states, dones) 
            with torch.no_grad():
                Q_hat_Values = Q1_hat(next_states[0], next_actions) 

            loss1 = Q1.loss(Q_values, rewards, Q_hat_Values, dones)
            loss1.backward()
            optim1.step()
            optim1.zero_grad()
            scheduler1.step()

            ############################ Train Black NN ############################
            states, actions, rewards, next_states, dones = buffer2.sample(batch_size)
            Q_values = Q2(states[0], actions)
            next_actions = player2_hat.get_Actions(next_states, dones) 
            with torch.no_grad():
                Q_hat_Values = Q2_hat(next_states[0], next_actions) 

            loss2 = Q2.loss(Q_values, rewards, Q_hat_Values, dones)
            loss2.backward()
            optim2.step()
            optim2.zero_grad()          
            scheduler2.step()

            if loss_count1 <= 1000:
                avgLoss1 = (avgLoss1 * loss_count1 + loss1.item()) / (loss_count1 + 1)
                loss_count1 += 1
            else:
                avgLoss1 += (loss1.item()-avgLoss1)* 0.00001 
            if loss_count2 <= 1000:
                avgLoss2 = (avgLoss2 * loss_count2 + loss2.item()) / (loss_count2 + 1)
                loss_count2 += 1
            else:
                avgLoss2 += (loss2.item()-avgLoss2)* 0.00001 
            
        if epoch % C == 0:
            Q1_hat.load_state_dict(Q1.state_dict())
            Q2_hat.load_state_dict(Q2.state_dict())



        ######### End Training ###############

        if (epoch+1) % 100 == 0:
            print(f'\nres= {res}')
            avgLosses1.append(avgLoss1)
            results.append(res)
            if best_res < res:      
                best_res = res
            res = 0

        if (epoch+1) % 100 == 0:
            test1 = tester1(100)
            test2 = tester2(100)
            test_score1 = test1[0]-test1[1]
            test_score2 = test2[1]-test2[0]
            if best_random1 < test_score1:
                best_random1 = test_score1
                player1.save_param(path_best_random1)
            if best_random2 < test_score2:
                best_random2 = test_score2
                player1.save_param(path_best_random2)
            print(test2, test2)
            random_results1.append(test_score1)
            random_results2.append(test_score2)

        if (epoch+1) % 500 == 0:
            torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses1}, results_path1)           
            torch.save(buffer1, buffer_path1)
            torch.save(buffer2, buffer_path2)
            player1.save_param(path_Save1)
            player2.save_param(path_Save2)
            torch.save(random_results1, random_results_path1)
            torch.save(random_results2, random_results_path1)
        
        print (f'epoch={epoch} steps={step} loss={loss1:.5f} avgloss={avgLoss1:.5f}', end=" ")
        print (f'learning rate={scheduler1.get_last_lr()[0]} path={path_Save1} res= {res} best_res = {best_res}')


    
    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses1}, results_path1)
    player1.save_param(path_Save1)
    player2.save_param(path_Save2)
    torch.save(buffer1, buffer_path1)
    torch.save(buffer2, buffer_path2)
    torch.save(random_results1, random_results_path1)
    torch.save(random_results2, random_results_path2)

if __name__ == '__main__':
    main()

