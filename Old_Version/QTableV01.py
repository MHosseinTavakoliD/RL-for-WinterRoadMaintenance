import random

import numpy as np
import pandas as pd
import Snow_Covrg_calc_3 as SC
import xlwt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
epochs = 1500000
n_states = 4
n_episodes = 13
State0 = {1:{'SnowFall': [5.5e-06, 1.08e-05, 1.62e-05, 2.16e-05, 2.16e-05, 2.7e-06, 0, 5.4e-05, 1.08e-05, 2.7e-06, 3.24e-05, 4.05e-05, 5.4e-05, 0],'T_air': [-3, -1, 0, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1], 'T_ps': [-5, -2, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 0, 0],'Vwind': [10, 10, 15, 10, 10, 15, 10, 0, 0, 15, 10, 15, 0, 5], 'Humidity': [100, 20, 40, 40, 80, 40, 40, 40, 20, 80, 60, 20, 20, 60],'Weather_cond': [3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1], 'Reward_list': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Action_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'ACC_REWARD' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Materials':[], 'status':[] }
        ,2: {'SnowFall': [0, 2.7e-06, 0, 2.7e-06, 1.08e-05, 0, 5.4e-05, 0, 2.7e-06, 0, 0, 0, 5.4e-05], 'T_air': [-17, -18, -18, -19, -19, -19, -19, -19, -18, -18, -17, -15, -14], 'T_ps': [-19, -18, -19, -19, -19, -19, -19, -17, -17, -16, -13, -12, -11], 'Vwind': [10, 20, 15, 15, 0, 5, 20, 10, 20, 5, 20, 20, 0], 'Humidity': [80, 60, 60, 100, 80, 40, 80, 80, 60, 40, 60, 60, 60], 'Weather_cond': [1, 3, 2, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3], 'Reward_list': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Action_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'ACC_REWARD' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Materials':[], 'status':[]}
        ,3: {'SnowFall': [1.08e-05, 1.08e-05, 0, 0, 0, 0, 0, 3.24e-05, 2.7e-06, 2.7e-06, 0, 8.1e-06, 5.5e-06], 'T_air': [-8, -10, -11, -12, -14, -15, -16, -17, -17, -18, -19, -19, -19], 'T_ps': [-10, -11, -12, -15, -16, -17, -18, -18, -19, -20, -20, -19, -19], 'Vwind': [15, 10, 10, 10, 10, 5, 0, 15, 10, 5, 5, 20, 5], 'Humidity': [20, 20, 80, 60, 60, 60, 80, 60, 80, 60, 40, 20, 40], 'Weather_cond': [3, 3, 1, 1, 2, 1, 1, 3, 3, 3, 2, 3, 3], 'Reward_list': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Action_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,'ACC_REWARD' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Materials':[], 'status':[]}
        ,4: {'SnowFall': [0, 2.7e-06, 0, 0, 0, 2.7e-06, 1.08e-05, 5.5e-06, 0, 3.24e-05, 8.1e-06, 0, 0], 'T_air': [0, 0, -1, -2, -3, -4, -6, -7, -8, -10, -11, -12, -14], 'T_ps': [-2, -2, -3, -4, -5, -8, -9, -9, -12, -13, -14, -16, -18], 'Vwind': [0, 5, 10, 15, 10, 5, 15, 10, 10, 5, 15, 20, 10], 'Humidity': [60, 80, 40, 80, 80, 40, 100, 100, 100, 80, 80, 60, 80], 'Weather_cond': [3, 3, 1, 3, 2, 3, 3, 3, 3, 3, 3, 1, 2], 'Reward_list': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Action_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'ACC_REWARD' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Materials':[], 'status':[]}
          }

Table = pd.DataFrame(State0)
# print (Table)

Check_table = pd.DataFrame(State0)
for state in range (1, n_states+1):
    pre_Acc_reward = -1000000
    for i in range (0, epochs):
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Epoch", i , "out of", epochs,  "  For state number: ", state )
        Reward_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Action_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ACC_REWARD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        salt_limit = 2
        plow_limit = 4
        Acc_reward = 0
        STEP_LIMIT = 14
        step_n = 0
        Materials = []
        Stat = []
        Material = [0, 0, 0]
        info1 = {}
        for episode in range (0, n_episodes):
            snowfall = State0[state]['SnowFall'][episode]
            t_air = State0[state]['T_air'][episode]
            t_ps = State0[state]['T_ps'][episode]
            vwind = State0[state]['Vwind'][episode]
            humidity = State0[state]['Humidity'][episode]
            weather_cond = State0[state]['Weather_cond'][episode]

            # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
            min_T_ps_list = min(State0[state]['T_ps'])
            reward = 0
            rewards = 0

            # Apply action

            try:
                Material = info1['material']
                # print ("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            except:
                Material = [0, 0, 0]
            initail_snow_for_step = Material[0]
            initail_water_for_step = Material[1]
            initail_salt_for_step = Material[2]

            action_list = [0,1,2]
            action = random.choice(action_list)
            # action_list = [2,2,2,2,0,2,2,1,1,0,1,2,2]
            # action = action_list[episode]

            # print("%%%%%Action:", action)

            if action == 0:  # Salt

                # Select the salt amount to use based on the minimum surface temp:
                min_T_ps = min_T_ps_list  # min(States['T_ps'])
                # Assuming using pre-wetted salts
                # Measuring salt amount based on the Ruled-Base model
                Salt_amount = -32.027 * min_T_ps + 79.24
                if Salt_amount < 0: Salt_amount = 0
                if Salt_amount > 400: Salt_amount = 400  # here salt unit is lb/mile/lane

                # From Previous steps:
                initail_salt_for_step = Salt_amount + initail_salt_for_step
                if salt_limit <= 0:
                    reward = -2000  # -150 + 100 * salt_limit
                    salt_limit -= 1

                if salt_limit > 0:
                    reward = -65  # -1*initail_salt_for_step *0.233
                    salt_limit -= 1
            # print("salt_limit", salt_limit)
            if action == 1:  # plow/
                # initail_snow_for_step = Material[0] * 0.5
                if plow_limit <= 0:
                    reward = -2000  # -150 + 100 *plow_limit
                    plow_limit -= 1

                if plow_limit > 0:
                    reward = -10
                    plow_limit -= 1
            # print("plow_limit", plow_limit)
            if action == 2:  # Do nothing
                reward = 0



            State = [snowfall, t_air, t_ps, vwind, humidity, weather_cond]
            # print ("initail_salt_for_step", initail_salt_for_step)
            Material[0], Material[1], Material[2], stat = SC.SnowMass(Snowfall=snowfall,
                                                                      rainfall=0, Tps=t_air, Tair=t_air,
                                                                      Weather_cond=weather_cond, Vwind=vwind,
                                                                      Humidity=humidity, Snow_init=initail_snow_for_step
                                                                      , Water_init=initail_water_for_step,
                                                                      salt_init=initail_salt_for_step)
            # print ("Material[2]", Material[2])
            if Material[2] > 20:
                Material[0] = 0

            if action == 1:  # plow 90% of snow removal
                Material[0] = Material[0] * 0.1

            # print("Material:  kg/m2/hr ", Material)
            info1 = {'material': Material}
            # Figure out the reward
            # Based on the snow on the road
            #######################################################################################################################################
            Snow_punish = Material[0]*-100 # try 60.... for example: for 0.5 kg/m2 snow it will receive -2.5 reward
            #######################################################################################################################################

            step_score = (step_n +1)* 10

            # print ("reward: ", reward)
            rewards = reward + Snow_punish + step_score

            Acc_reward += rewards

            # Set placeholder for info
            info = {'score': Acc_reward}

            if step_n > 0 and step_n < 13:
                done = False
            if step_n == 13:
                done = True
            # # if Acc_reward < -500:
            # #     done = True
            # if Material[0] > 5:
            #     done = True

            # State = np.reshape(State, (1,6))
            # print()
            print('Step:{} action:{} Acc_reward:{} step reward:{}'.format(step_n, action,Acc_reward, rewards))

            step_n += 1
            Action_list[episode] = action
            Reward_list[episode] = "{:.0f}".format(rewards)
            ACC_REWARD[episode] = "{:.0f}".format(Acc_reward)

            Materials.append(Material.copy())
            Stat.append(stat)
            # print("Material", Material)
            # print("Materials", Materials)


            # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if Acc_reward > pre_Acc_reward:
            # print("ALLLLL")
            pre_Acc_reward = Acc_reward
            Table[state]['Reward_list']= Reward_list
            Table[state]['Action_list'] = Action_list
            Table[state]['ACC_REWARD'] = ACC_REWARD
            Table[state]['Materials'] = Materials
            Table[state]['status'] = Stat




print (Table)
for state in range (1, n_states+1):
    print ("State number: ", state)
    print(Table[state]['Materials'][0][0], Table[state]['Materials'][1][0], Table[state]['Materials'][2][0], Table[state]['Materials'][3][0], Table[state]['Materials'][4][0], Table[state]['Materials'][5][0], Table[state]['Materials'][6][0], Table[state]['Materials'][7][0], Table[state]['Materials'][8][0], Table[state]['Materials'][9][0], Table[state]['Materials'][10][0], Table[state]['Materials'][11][0], Table[state]['Materials'][12][0])
    print(Table[state]['Materials'][0][1], Table[state]['Materials'][1][1], Table[state]['Materials'][2][1], Table[state]['Materials'][3][1], Table[state]['Materials'][4][1], Table[state]['Materials'][5][1], Table[state]['Materials'][6][1], Table[state]['Materials'][7][1], Table[state]['Materials'][8][1], Table[state]['Materials'][9][1], Table[state]['Materials'][10][1], Table[state]['Materials'][11][1], Table[state]['Materials'][12][1])
    print(Table[state]['Materials'][0][2], Table[state]['Materials'][1][2], Table[state]['Materials'][2][2], Table[state]['Materials'][3][2], Table[state]['Materials'][4][2], Table[state]['Materials'][5][2], Table[state]['Materials'][6][2], Table[state]['Materials'][7][2], Table[state]['Materials'][8][2], Table[state]['Materials'][9][2], Table[state]['Materials'][10][2], Table[state]['Materials'][11][2], Table[state]['Materials'][12][2])
    print ("#########")
Table.to_excel('result.xls', index=False)