import numpy as np


def SnowMass(Snowfall, rainfall, Tps, Tair, Weather_cond, Vwind, Humidity, Snow_init, Water_init, salt_init):
    # print (Snowfall, rainfall, Tps, Tair, Weather_cond, Vwind, Humidity, Snow_init, Water_init, salt_init)
    # print("#########################################################")
    # print('Snow_init:{}      Water_init:{}      Salt_init:{}'.format( Snow_init, Water_init, salt_init))
    T_f = -0.025 * salt_init - 0.5
    # print("TF",T_f)

    if Tps > T_f:
        Z = "Melting"
        # print("###############################Melting")  # Melting
    else:
        Z = "Freezing"
        # print("Freezing")

    # 1: Consider that Snowfall is m/s
    # f(t) = 0.5, Snow density 100 kg/m3, Snowfall => Hsnow/1 hour => m/s
    f_t = 0.9
    g_t = 1 - f_t
    Twis = (Tps + Tair) / 2

    V_ice = Snow_init * 10**(-3)#/500
    # print (V_ice)
    ## Heat transfer%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    q_csp = (Tps - Twis) * 1 / (V_ice / (2*2.22) + 50e-3 / (2 * 0.8) + 0.6e-3* np.exp(4) ) #* np.exp(5.3 * 0.1) # For ice ==2.22 for snow btw 0.02 to 0.8
    # print ("q_csp", q_csp)
    q_sn = (10.4 * Vwind**0.7 + 2.2)*(Twis - Tair) + f_t * \
           ( 100 * Snowfall * 2.108 + 1000 * rainfall * 4.184) * Tair + \
           0 + (4.184)* Twis * (1000 * 0.5 * V_ice * 0.015)
    # print ("q_sn", q_sn)
    # Radiation:
    if Weather_cond == 1: # "sunny":
        q_rld = 400
        q_rsd = 250
        q_rsu = 75
    if Weather_cond == 2: #"cloudy":
        q_rld = 300
        q_rsd = 150
        q_rsu = 45
    if Weather_cond == 3: #"overcast" or Weather_cond == "night":
        q_rld = 200
        q_rsd = 0
        q_rsu = 0
    # print("q_rld", q_rld, "q_rsd", q_rsd,"q_rsu", q_rsu)
    q_rn = 20#f_t * q_rld + (0.97 * 5.67e-8 * (Twis + 273.15) ** 4) + f_t * q_rsd - q_rsu
    # print ("q_rn",  q_rn)
    ########################################################################################
    P_A = f_t * 100 * Snowfall
    Mass_H2O_on_the_road_t0 = Water_init + P_A*3600 + Snow_init
    # print ("Mass_H2O_on_the_road", Mass_H2O_on_the_road_t0)
    if Mass_H2O_on_the_road_t0 > 0:
        P_B = abs(0.001*q_csp/334)
        P_C = abs(0.001 * q_sn / 334)
        P_D = abs(0.001 * q_rn / 334)
    if Mass_H2O_on_the_road_t0 <=0:
        P_B = 0
        P_C = 0
        P_D = 0
    # print ("P_D", P_D*3600)
    # print("P_C", P_C*3600)
    P_E = g_t * 100 * Snowfall * 0.05
    # Humidity freezing
    P_F = 0
    # if Humidity >= 40:
    #     Humidity_freezing_point = 0.1429*Humidity - 15.89
    #     # print ("Humidity_freezing_point", Humidity_freezing_point)
    #     if Tair <= Humidity_freezing_point and Tair >= -10:
    #         P_F = 2.2e-6 #0.008/3600
    #         # print ("Tair <= Humidity_freezing_point")
    # Water transfer
    P_Water = f_t * 1000 * rainfall - g_t *0
    Snow_end= 0
    Water_end = 0
    Salt_end = 0

    Snow_prod = Snow_init + (P_A + P_F - P_E) * 3600
    Snow_water_conversion = (P_B)*3600
    Water_prod = Water_init + P_Water
    # print ("Snow_water_conversion", Snow_water_conversion)

    # Snow_calc
    if Z == "Melting":
        # print ("Melting")
        if Snow_water_conversion >= Snow_prod:
            Snow_water_conversion = Snow_prod
        Water_prod = Water_prod + Snow_water_conversion

        Water_dispersed = 0.02* (P_C + P_D )*3600
        # print ("Water_dispersed", Water_dispersed)
        if Water_dispersed >= Water_prod:
            Water_dispersed = Water_prod

        Water_end =  Water_prod - Water_dispersed

        Snow_dispersed = 0
        Snow_prod = Snow_prod - Snow_water_conversion
        if Snow_prod > 0:
            Snow_dispersed = 0.35 * (P_C + P_D) * 3600
            if Snow_dispersed > Snow_prod:
                Snow_dispersed = Snow_prod
        Snow_end = Snow_prod - Snow_dispersed
        # print ( "Snow_prod:   ", Snow_prod, "   Snow_end:", Snow_end, "    Water_from_snow:", Water_from_snow ,
        #         "  Water_prod:", Water_prod, "   Water_dispersed:",Water_dispersed ,"Water_end:",
        #         Water_end, "salt_end:", Salt_end/0.00007621
        #         )
        # print ("Snow_init:", Snow_init, "Snow_prod:", Snow_prod, "Snow_end:", Snow_end,"  Water_init:", Water_init,"  Water_prod:", Water_prod,"Water_end:",
        #         Water_end, "Salt_init: " , salt_init, "salt_end: ", Snow_end)
    if Z == "Freezing":
        # print ("Freezing")
        if Snow_water_conversion >= Water_prod:
            Snow_water_conversion = Water_prod
        Snow_prod = Snow_prod + Snow_water_conversion
        Snow_dispersed = 0.2*(P_C + P_D ) * 3600
        # print("Snow_dispersed", Snow_dispersed)
        if Snow_dispersed >= Snow_prod:
            Snow_dispersed = Snow_prod

        Snow_end = Snow_prod - Snow_dispersed
        Water_end = Water_prod - Snow_water_conversion
    Salt_end = 0.55 * salt_init#*0.00007621#salt_init * 0.00007621 - 0.1 * salt_init * 0.00007621  # lb/mile/lane ==> 0.00007621 kg/m2, and vehicle dispersion
    if Salt_end < 0: Salt_end = 0
        # print(" - Freezing")
        # print("Snow_init:", Snow_init, "    Snow_prod:", Snow_prod, "  Snow_end:", Snow_end, "   Snow_from_water:", Snow_from_water,
        #       "   Snow_dispersed:", Snow_dispersed, "Water_end:", Water_end,  "salt_end:", Salt_end/0.00007621)
        # print("Snow_init:", Snow_init, "Snow_prod:", Snow_prod, "Snow_end:", Snow_end, "  Water_init:", Water_init,
        #       "Water_end:", Water_end, "Salt_init: " , salt_init, "salt_end: ", Salt_end)

    # M_water = -1* M_snow_per_sec *3600
    # print("P_A: ", P_A*3600 , "   P_B:  ", P_B*3600 , "  P_C: " , P_C*3600 , "  P_D: ", P_D*3600 ,
    #       "   P_E: ", P_E*3600 , "  P_F: ", P_F*3600)
    return (Snow_end, Water_end, Salt_end, Z)

###### Test the model ########
# Water_init = 0
# Snowfall = 6e-6
# rainfall = 0
# Tps = -5
# Tair = -2
# Weather_cond = 1
# Vwind = 0
# Snow_init = 0.0e-2
# # salting = False
# salt_init = 300.0
# Salt_time_intervals = 8
# Humidity = 90
#
#
# print ("_________________________________________________________")
# print ( SnowMass(Snowfall, rainfall, Tps, Tair, Weather_cond, Vwind, Humidity, Snow_init, salt_init, Water_init))
# print ("Ice/Snow on the road", Ice, "kg/m2/hr")
# print ("Water on the road", water, "kg/m2/hr")
# print ("Water dispersed from the road", time0_mass - water- Ice, "kg/m2/hr")
'''
print ("###### Test the model ######## Fujimoto 2013.01.21 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
Water_init = [0,0,0,0,0,0]
Snowfall = 0
rainfall = 0
Tps = [-3, -3.7, -4.8, -5.5, -6.5, -7.8, -8]
Tair = [-5, -6, -6.5, -8, -9, -9, -9]
Weather_cond = 3
Vwind = [3,4,3,3,4,3, 3]
Snow_init = [0.5, 0,0,0,0,0, 0]
# salting = False
salt_init = [0,260,0,0,0,0, 0]
# Salt_time_intervals = 8
Humidity = [80, 85, 90, 82, 82, 87, 84]


for i in range (0,6):
    Snow_end, Water_end, Salt_end, Z = SnowMass(Snowfall, rainfall, Tps[i], Tair[i], Weather_cond, Vwind[i], Humidity[i], Snow_init[i],Water_init[i],salt_init[i])
    if Snow_end > 0 :
        Snow_init[i+1] = Snow_end
    if Water_end > 0 :
        Water_init[i+1] = Water_end
    if Salt_end > 0 :
        salt_init[i+1] = Salt_end

    # print ("time: ", i+ 19 , "   Snow: ", Snow_init[i], "   Water:  ", Water_init[i], "   salt:  ", salt_init[i])
    # print("#########################################################")
    # print ('time:{}      Snow:{}      Water:{}      Salt:{}'.format(i+ 18.5, Snow_init[i], Water_init[i], salt_init[i]))
# print ("_________________________________________________________")
# print ( SnowMass(Snowfall, rainfall, Tps, Tair, Weather_cond, Vwind, Humidity, Snow_init,Water_init,salt_init))

print ("###### Test the model ######## Fujimoto 2013.01.28 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
Water_init = [0,0,0,0,0,0]
Snowfall = 0
rainfall = 0
Tps = [-1.5, -2.4, -3.5, -4.2, -4.5, -5.7]
Tair = [-3.5, -5, -5.5, -6.5, -7.5, -8]
Weather_cond = 3
Vwind = [2,1,2,2,1,1]
Snow_init = [0.78, 0,0,0,0,0, 0]
# salting = False
salt_init = [0,117,0,0,0,0, 0]
# Salt_time_intervals = 8
Humidity = [61, 64, 67, 72, 75, 77]


for i in range (0,6):
    Snow_end, Water_end, Salt_end, Z = SnowMass(Snowfall, rainfall, Tps[i], Tair[i], Weather_cond, Vwind[i], Humidity[i], Snow_init[i],Water_init[i],salt_init[i])
    if Snow_end > 0 :
        Snow_init[i+1] = Snow_end
    if Water_end > 0 :
        Water_init[i+1] = Water_end
    if Salt_end > 0 :
        salt_init[i+1] = Salt_end

    # print ("time: ", i+ 19 , "   Snow: ", Snow_init[i], "   Water:  ", Water_init[i], "   salt:  ", salt_init[i])
    # print("#########################################################")
    # print ('time:{}      Snow:{}      Water:{}      Salt:{}'.format(i+ 18.5, Snow_init[i], Water_init[i], salt_init[i]))




print ("###### Test the model ######## Fujimoto 2013.01.31 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
Water_init = [0,0,0,0,0,0]
Snowfall = 0
rainfall = 0
Tps = [-2.2, -2.8, -3.3, -3.9, -4.5, -5.2]
Tair = [-1, -3, -3.5, -5, -6, -6]
Weather_cond = 3
Vwind = [2,1,1,1,1,0]
Snow_init = [0.79, 0,0,0,0,0, 0]
# salting = False
salt_init = [0,170,0,0,0,0, 0]
# Salt_time_intervals = 8
Humidity = [81, 88, 94, 98, 98, 97]


for i in range (0,6):
    Snow_end, Water_end, Salt_end, Z = SnowMass(Snowfall, rainfall, Tps[i], Tair[i], Weather_cond, Vwind[i], Humidity[i], Snow_init[i],Water_init[i],salt_init[i])
    if Snow_end > 0 :
        Snow_init[i+1] = Snow_end
    if Water_end > 0 :
        Water_init[i+1] = Water_end
    if Salt_end > 0 :
        salt_init[i+1] = Salt_end

    # print ("time: ", i+ 19 , "   Snow: ", Snow_init[i], "   Water:  ", Water_init[i], "   salt:  ", salt_init[i])
    # print("#########################################################")
    # print ('time:{}      Snow:{}      Water:{}      Salt:{}'.format(i+ 18.5, Snow_init[i], Water_init[i], salt_init[i]))


'''

State0 = {'SnowFall': [5.5e-06, 1.08e-05, 1.62e-05, 2.16e-05, 2.16e-05, 2.7e-06, 0, 5.4e-05, 1.08e-05, 2.7e-06, 3.24e-05, 4.05e-05, 5.4e-05, 0],
          'T_air': [-3, -1, 0, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1], 'T_ps': [-5, -2, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 0, 0],
          'Vwind': [10, 10, 15, 10, 10, 15, 10, 0, 0, 15, 10, 15, 0, 5], 'Humidity': [100, 20, 40, 40, 80, 40, 40, 40, 20, 80, 60, 20, 20, 60],
          'Weather_cond': [3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1]}
n_episodes = 13
initail_snow_for_step = 0
initail_water_for_step = 0
initail_salt_for_step = 0
Material = [0,0,0]
snow = []
water = []
salt = []
Stat = []
for episode in range(0, n_episodes):
    snowfall = State0['SnowFall'][episode]
    t_air = State0['T_air'][episode]
    t_ps = State0['T_ps'][episode]
    vwind = State0['Vwind'][episode]
    humidity = State0['Humidity'][episode]
    weather_cond = State0['Weather_cond'][episode]

    initail_snow_for_step, initail_water_for_step, initail_salt_for_step, stat = SnowMass(Snowfall=snowfall,
                                                                      rainfall=0, Tps=t_air, Tair=t_air,
                                                                      Weather_cond=weather_cond, Vwind=vwind,
                                                                      Humidity=humidity, Snow_init=initail_snow_for_step
                                                                      , Water_init=initail_water_for_step,
                                                                      salt_init=initail_salt_for_step)

    snow.append(initail_snow_for_step)
    water.append(initail_water_for_step)
    salt.append(initail_salt_for_step)
    Stat.append(stat)

# print ("snow", snow)
# print("water", water)
# print ("salt", salt)
# print("status", Stat)