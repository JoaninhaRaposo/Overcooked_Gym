# import pygame module in this program
from teammates.Astro import ACTION_MEANINGS_MDP 
import itertools
import pickle
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


log = []
LVL=1
LOG_NRS = range(300,329, 2) # PICK CONDITION: nrs impares - condição 1 | nrs pares - condição 2
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

for i in LOG_NRS:
    # Concatenate all logfiles from chosen condition
    log_file = f"logfiles/logfile_{i}_lvl{LVL}.pickle"
    with open(log_file, "rb") as f:
        log = pickle.load(f)

    for logframe in log:
        s_env.append(logframe.state_env[:4])
        s_mdp.append(logframe.state_mdp)

#x,y - coordenadas dos humanos no mapa (para ficar igual ao mapa: (y,-x))
x = [-array[0] for array in s_env]
y = [array[1] for array in s_env]

#Counter - (state): #times visited 
count_human = count_occurrences(s_env)

l= list(count_human.items())
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
#print(count_occurrences(s_mdp).items())
#print("STATE ENV: ", count_occurrences(s_env))
#print("STATE MDP: ", count_occurrences(s_mdp))

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
mdp_transitions = np.zeros((len(s_mdp), len(s_mdp)))

for i in range(1,len(s_mdp)):
  if s_mdp[i-1][1] != s_mdp[i][1]: #No mdp onde o humano se encontra mudou
     mdp_transitions[i-1][i] += 1 #Aumentar contador de nó i-1 para i

print(mdp_transitions)  #Esta a 0. TODO: Continuar, fazer debug perceber o que esta mal. Confirmar feedback da duvida