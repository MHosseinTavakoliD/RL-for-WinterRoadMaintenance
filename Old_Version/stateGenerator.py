
import random
import numpy as np


def state_generation(Step_limit):
    SnowFall = []
    T_ps = []
    T_air = []
    Weather_cond = []
    Vwind = []
    Humidity = []

    SnowFall_batch = [0, 0, 0, 0, 0, 0, 2.7e-6, 2.7e-6, 2.7e-6, 2.7e-6, 5.5e-6, 5.5e-6, 5.5e-6, 8.1e-6, 8.1e-6, 1.08e-5,
                      1.62e-5, 2.16e-5, 3.24e-5, 4.05e-5, 5.4e-5]  # m/s
    # T_ps_batch = [-20, -15, -13, -11, -10, -9, -8, -7, -6, -5, -4 ,-3, -2, -1, 0, 1, 2, 3, 4] #c
    # T_air_batch = [-20, -15, -13, -11, -10, -9, -8, -7, -6, -5, -4 ,-3, -2, -1, 0, 1, 2, 3, 4] #c
    Weather_cond_batch = [1, 2, 3]  # ["sunny", "cloudy", "overcast"]
    Vwind_batch = [0, 5, 5, 10, 10, 15, 15, 20]  # m/s
    Humidity_batch = [20, 40, 60, 60, 80, 80, 100]  # %

    # Creating T_air
    x = random.randint(0, 30)
    # print(x)
    a_sin_batch = [2, 3, 5, 7, 9]
    a = random.sample(a_sin_batch, 1)
    # print(a[0])
    for i in range(0, Step_limit):
        T_air.append(int(12 * np.sin(x / a[0]) - 8))
        x = x + 1

    # Creating Surface_temp based on the air temp
    for i in range(0, Step_limit):
        if i == 0:
            T_ps.append((T_air[i] - 2))  # We assume that the surface temp is equalt to air temp minus 2
            # print(i, "1")
        if i == Step_limit - 1:
            T_ps.append((T_ps[-1]) + 1.165992 * (T_air[i] - T_air[i - 1]) - 0.24251 * (
                    (T_ps[-1]) - T_air[i]))
            # print(i, "2")
        if i > 0 and i < Step_limit - 1:
            T_ps.append((T_ps[-1]) + 1.165992 * (T_air[i + 1] - T_air[i]) - 0.24251 * (
                    (T_ps[-1]) - T_air[i + 1]))
            # print(i, "3")
    T_ps = [int(x) for x in T_ps]

    # Creating Snowfall # Creating Wind data # Creating Humidity data # Weather cond
    for i in range(0, Step_limit):
        SnowFall.append(SnowFall_batch[random.randint(0, len(SnowFall_batch) - 1)])
        Vwind.append(Vwind_batch[random.randint(0, len(Vwind_batch) - 1)])
        Humidity.append(Humidity_batch[random.randint(0, len(Humidity_batch) - 1)])
        if SnowFall[i] == 0:
            Weather_cond.append(Weather_cond_batch[random.randint(0, len(Weather_cond_batch) - 1)])
        else:
            Weather_cond.append(3)
    # Snow_init.append(0)
    # Water_init.append(0)

    return {"SnowFall": SnowFall, "T_air": T_air, "T_ps": T_ps, "Vwind": Vwind, "Humidity": Humidity,
            "Weather_cond": Weather_cond}

for i in range (0,3 ):
    States = state_generation(Step_limit=13)

    print (States)