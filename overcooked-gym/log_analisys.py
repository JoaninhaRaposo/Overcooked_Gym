# import pygame module in this program

from teammates.Astro import ACTION_MEANINGS_MDP 
import itertools
import pickle
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


log = []
LVL=2
#LOG_NRS = range(300,329, 2) # PICK CONDITION: nrs impares - condição 1 | nrs pares - condição 2
LOG_NRS = range(301,330, 2) #cond 1
ACTION_SPACE = tuple(range(len(ACTION_MEANINGS_MDP[LVL-1])))
JOINT_ACTION_SPACE = list(itertools.product(ACTION_SPACE, repeat=2))
#print("READING FROM: ", log_file)

class LogFrame:
  def __init__(self, timestep:int , state_env, state_mdp:list, action_env:tuple, action_mdp:tuple, onion_time:float, game_time:float):
    self.timestep = timestep
    self.state_env = state_env
    self.state_mdp = state_mdp
    self.action_env = action_env
    self.action_mdp = action_mdp
    self.onion_time = onion_time
    self.game_time = game_time

def count_occurrences(arrays):
    return Counter([tuple(array) for array in arrays])

s_env = []
s_mdp = []
s_full_env = []
ball_time = []
game_time = []
total_scores = []
print("Log nrs:")
for i in LOG_NRS:
    print("{}".format(i))
    # Concatenate all logfiles from chosen condition
    log_file = f"logfiles/logfile_{i}_lvl{LVL}.pickle"
    with open(log_file, "rb") as f:
        log = pickle.load(f)

    for logframe in log:
        s_env.append(logframe.state_env[:4])
        s_mdp.append(logframe.state_mdp)
        s_full_env.append(logframe.state_env)
    
    ball_time.append(logframe.onion_time)
    game_time.append(logframe.game_time)
#x,y - coordenadas dos humanos no mapa (para ficar igual ao mapa: (y,-x))
x = [-array[0] for array in s_env]
y = [array[1] for array in s_env]

#Counter - (state): #times visited 
count_human = count_occurrences(s_env)

l= list(count_human.items())
#print("Prints da Ana")
#print: x   y   #times visited || para colocar em https://chart-studio.plotly.com
for item in l:
   toPrint = str(-item[0][0]) + "\t" + str(item[0][1]) + "\t" + str(item[1])
#   print(toPrint)

'''
plt.scatter(y, x,count_human.item((x,y)))
plt.xlim(0,14)
plt.ylim(-14,0)
plt.title('HUMAN POS ENV')
#plt.grid()
plt.show()
'''
"""print(count_occurrences(s_mdp).items())
print("STATE ENV: ", count_occurrences(s_env))
print("STATE MDP: ", count_occurrences(s_mdp))"""

#Transições estados de MDP; ( Retirar quantas vezes são registadas transições dos humanos entre node X e node Y do MDP.)
#1. s_mdp = todos os state mdp numa só lista
#2. verificar estado x e x+1 - houve transição?

#trans_0_1 = 0 #Transição do no 0 para no 1    
#trans_0_5 = 0 #transicao do no 0 para o no 5
#trans_1_2 = 0 
#trans_1_3 = 0 
#trans_2_3 = 0
#trans_3_4 = 0
#trans_3_5 = 0
#trans_5_6 = 0
#trans_6_7 = 0    
#Fazer matriz 2x2 (in -> out)
#mdp_transitions = np.zeros((8, 8)) Level 1
mdp_transitions = np.zeros((9,9)) # Level 2
save_mdp_transition = []
#states_mdp_ball = np.zeros(8) level 1
states_mdp_ball = np.zeros(9)
states_env_ball = {}
plot_env_ball = {}

count_timesteps = 0
for i in range(1,len(s_mdp)):
    if s_mdp[i-1][1] != 10 and s_mdp[i][1] != 10:
        if s_mdp[i-1][1] != s_mdp[i][1]: #No mdp onde o humano se encontra mudou
            mdp_transitions[s_mdp[i-1][1]][s_mdp[i][1]] += 1 #Aumentar contador de nó i-1 para i
            str_aux = str(s_mdp[i-1][1]) + "->" + str( s_mdp[i][1])  
            save_mdp_transition.append(str_aux)

for i in range(len(s_mdp)):
    if s_mdp[i][1] != 10:
        if 1 in s_mdp[i][2:]: #Verificar em quantos time steps o humano fica com a bola para cada no mdp
            states_mdp_ball[s_mdp[i][1]] += 1
            #print(states_mdp_ball)
            count_timesteps += 1

counter = 0
for i in range(len(s_full_env)):
    if s_full_env[i][6] == 1:
        counter += 1
        if tuple(s_full_env[i][0:2]) not in states_env_ball.keys():
            states_env_ball[(tuple(s_full_env[i][0:2]))] = 1
        else:
            states_env_ball[(tuple(s_full_env[i][0:2]))] += 1

        
print("Len do states_mdp: {}, len do states env: {}".format(len(s_mdp), len(s_full_env)))
print("mdp counter, env counter: {} {}".format(count_timesteps,counter))        
print("MDP transitions")

print(mdp_transitions)
print("Human transitions:")
for i in range(len(mdp_transitions)):
   for j in range(len(mdp_transitions)):
      if mdp_transitions[i][j] != 0: 
         print("[{}->{}]".format(i, j))

print("Values for each transition")
for i in range(len(mdp_transitions)):
   for j in range(len(mdp_transitions)):
      if mdp_transitions[i][j] != 0: 
         print(mdp_transitions[i][j])


#plt.hist(save_mdp_transition, bins=21)
#plt.show()


#Tempos com bolas na mão em cada estado:
#   Verificar em quantos timesteps o humano se encontra com a bola na mão, para cada mdp node/posição no environment. 
#1.colocar todos os state_mdp de todos os logfiles numa só lista (ver log_analisys.py);
#2. Filtrar estados sem bola na mão: Ignorar estados onde state_mdp[2:] != 1 OU ignorar estados onde state_env[6]!=1; 
#3. Para os restantes, registar node/(x,y) no state_env onde humano se encontra com a bola na mão


print("Timesteps with ball in each MDP state:")
print(states_mdp_ball)
print("All MDP States")
for i in range(len(states_mdp_ball)):
      if states_mdp_ball[i] != 0: 
         #print("{}: {} timesteps".format(i, states_mdp_ball[i]))
         print(i)
print("All counts:")
for i in range(len(states_mdp_ball)):
      if states_mdp_ball[i] != 0: 
         #print("{}: {} timesteps".format(i, states_mdp_ball[i]))
         print(states_mdp_ball[i])



print("Time with ball in each Env state:")
print(states_env_ball)

"""for state in states_env_ball.keys():
      if state != 0: 
         print("human timesteps with ball at env state {}: {} timesteps".format(state, states_env_ball[state]))
"""
print("Time with ball in each Env state: without text")
print("Just states:")
lista = []

for state in states_env_ball.keys():
      aux = []
      if state != 0: 
        #print("{}".format(state))
        aux.append(state[0])
        aux.append(state[1])
        aux.append(states_env_ball[state])
        tuplo = tuple(aux)
        lista.append(tuplo)

print(lista)


lista_ordenada = sorted(lista, key = lambda x: (x[0], x[1]))
print(lista_ordenada)
for x in lista_ordenada:
    if x!=0:
        print(x[0:2])

for x in lista_ordenada:
    if x!=0:
        print(x[2])

"""for state in states_env_ball.keys():
      if state != 0: 
         print("{}".format(states_env_ball[state]))"""

#TODO: Pode tb ser interessante analisar quem teve mais tempo com a bola, e quem teve melhores ou piores pontuaçoes
#Ponto 3: Histogramas de posição mas para estados só com humanos com bolas na mão: Plot de histograma com # vezes com bola na mão por (x,y).

print("Ball time")
for time in ball_time:
    print(time)
print("Game time")
for time in game_time:
    print(time)

print("Score")
for i in range(len(game_time)):
    score = 100 - game_time[i] - round(ball_time[i])
    print(score)
