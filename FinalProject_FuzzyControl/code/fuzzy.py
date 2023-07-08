'''
fuzzy project function
'''
# import lib
## read pc info.
import psutil

## fuzzy control
import skfuzzy as fuzz
import skfuzzy.control as fuzz_ctrl

import numpy as np

# define domain
# Range

## range of cpu. & ram & battery & level 
### 建立membership function 的全域範圍，下面numpy只是一個範圍還沒真正定義出模糊的區間
x_cpu_range = np.arange(0,101,1,np.float32)
x_ram_range = np.arange(0,101,1,np.float32)
y_power_range = np.arange(0,11,1,np.float32)

x_power_range = np.arange(0,11,1,np.float32)
x_battery_range = np.arange(0,101,1,np.float32)
y_level_range = np.arange(0,11,1,np.float32)
##　variable and membership functions
### 建立四個模糊區間：cpu(input), ram(input), battery(input), level(output)
'''
class Antecedent(
    universe: Any,
    label: str
)
'''
x_cpu = fuzz_ctrl.Antecedent(x_cpu_range, "cpu")
x_ram = fuzz_ctrl.Antecedent(x_ram_range, "ram")

x_power = fuzz_ctrl.Antecedent(x_power_range, "power")
x_battery = fuzz_ctrl.Antecedent(x_battery_range, "battery")

'''
class Consequent(
    universe: NDArray[float32],
    label: str,
    defuzzify_method: str = 'centroid'
)
'''
y_power = fuzz_ctrl.Consequent(y_power_range, "power")
y_level = fuzz_ctrl.Consequent(y_level_range, "level")

## 質心模糊
y_power.defuzzify_method = "centroid" # 預設就是COG
y_level.defuzzify_method = "centroid" # 預設就是COG

# domain 1
# fuzz.trimf通常用於定義具有 三角形 形狀的模糊集合
# fuzzy.trapmf通常用於定義具有 梯形 形狀的模糊集合

## cpu 定義4個fuzzy set (input1)
x_cpu["low"] = fuzz.trapmf(x_cpu_range,[0,0,10,30])
x_cpu["normal"] = fuzz.trapmf(x_cpu_range,[20,40,60,75])
x_cpu["high"] = fuzz.trimf(x_cpu_range,[50,70,90])
x_cpu["higher"] = fuzz.trapmf(x_cpu_range,[80,90,100,100])

## ram 定義3個fuzzy set (input2)
x_ram["low"] = fuzz.trapmf(x_ram_range,[0,0,15,30])
x_ram["normal"] = fuzz.trapmf(x_ram_range,[25,40,60,75])
x_ram["high"] = fuzz.trapmf(x_ram_range,[60,80,100,100])

## power 定義3個fuzzy set (output)
y_power["low"] = fuzz.trapmf(y_power_range,[0,0,2,4])
y_power["normal"] = fuzz.trapmf(y_power_range,[3,4,6,7])
y_power["high"] = fuzz.trapmf(y_power_range,[6,8,10,10])

# rule1
## 輸出規則
rule_power_high = fuzz_ctrl.Rule(antecedent=((x_cpu["higher"]&x_ram["low"])|
                                             (x_cpu["higher"]&x_ram["normal"])|
                                             (x_cpu["higher"]&x_ram["high"])|
                                             (x_cpu["high"]&x_ram["normal"])|
                                             (x_cpu["high"]&x_ram["high"])|
                                             (x_cpu["normal"]&x_ram["high"])),
                                             consequent = y_power["high"],label="high")

rule_power_med = fuzz_ctrl.Rule(antecedent=((x_cpu["high"]&x_ram["low"])|
                                            (x_cpu["normal"]&x_ram["normal"])|
                                            (x_cpu["low"]&x_ram["normal"])|
                                            (x_cpu["low"]&x_ram["high"])),
                                            consequent = y_power["normal"],label="med")

rule_power_low = fuzz_ctrl.Rule(antecedent=((x_cpu["low"]&x_ram["low"])|
                                            (x_cpu["normal"]&x_ram["low"])),
                                            consequent = y_power["low"],label="low")

# fuzzy_layer_1
def Fuzzy_layer_1(cpu, ram):
    # 根據前面的規則建立此系統，可以視為建立起整個函數
    system1 = fuzz_ctrl.ControlSystem(rules=[rule_power_low,rule_power_med,rule_power_high])
    # 根據建立起來的membership function（system）去模擬
    sys_sim1= fuzz_ctrl.ControlSystemSimulation(system1)

    # 將數值送入模擬器（根據一開始建立大label)
    sys_sim1.input["cpu"] = cpu
    sys_sim1.input["ram"] = ram

    # system compute
    sys_sim1.compute()
    out = float(sys_sim1.output["power"])
    return out
# domain 2
## power 定義3個fuzzy set (input1)
x_power["low"] = fuzz.trapmf(x_power_range,[0,0,2,4])
x_power["normal"] = fuzz.trapmf(x_power_range,[3,4,6,7])
x_power["high"] = fuzz.trapmf(x_power_range,[6,8,10,10])

## battery 定義5個fuzzy set (input2)
x_battery["less"] = fuzz.trapmf(x_battery_range,[0,0, 20,30])
x_battery["little"] = fuzz.trimf(x_battery_range,[15,30,45])
x_battery["normal"] = fuzz.trimf(x_battery_range,[35,50,65])
x_battery["high"] = fuzz.trimf(x_battery_range,[60,75,90])
x_battery["higher"] = fuzz.trapmf(x_battery_range,[70,80,100,100])

## level 定義3個fuzzy set (output)
y_level["low"] = fuzz.trapmf(y_level_range,[0,0,2,3])
y_level["normal"] = fuzz.trapmf(y_level_range,[2,5,6,7])
y_level["high"] = fuzz.trapmf(y_level_range,[6,8,10,10])

# rule 2
## 輸出規則
rule_high = fuzz_ctrl.Rule(antecedent=((x_power["low"]&x_battery["less"])|
                                          (x_power["normal"]&x_battery["less"])|
                                          (x_power["high"]&x_battery["less"])|
                                          (x_power["normal"]&x_battery["little"])|
                                          (x_power["high"]&x_battery["little"])|
                                          (x_power["high"]&x_battery["normal"])),
                                          consequent = y_level["high"],label="high")

rule_normal = fuzz_ctrl.Rule(antecedent=((x_power["low"]&x_battery["little"])|
                                           (x_power["normal"]&x_battery["normal"])|
                                           (x_power["normal"]&x_battery["high"])|
                                           (x_power["high"]&x_battery["high"])|
                                           (x_power["high"]&x_battery["higher"])),
                                           consequent = y_level["normal"],label="normal")

rule_low = fuzz_ctrl.Rule(antecedent=((x_power["low"]&x_battery["high"])|
                                           (x_power["low"]&x_battery["higher"])|
                                           (x_power["low"]&x_battery["normal"])|
                                           (x_power["normal"]&x_battery["higher"])),
                                           consequent=y_level["low"],label="low")


#fuzzy_layer_2
def Fuzzy_layer_2(power, battery):
    # 根據前面的規則建立此系統，可以視為建立起整個函數
    system2 = fuzz_ctrl.ControlSystem(rules=[rule_low,rule_normal,rule_high])
    # 根據建立起來的membership function（system）去模擬
    sys_sim2= fuzz_ctrl.ControlSystemSimulation(system2)

    # Test
    # 將數值送入模擬器（根據一開始建立大label)
    sys_sim2.input["power"] = power
    sys_sim2.input["battery"] = battery

    # system compute
    sys_sim2.compute()
    out = sys_sim2.output["level"]
    return out
    
# main function
## get pc sensor
def PCsensor():
    # cpu
    cpu_percent = psutil.cpu_percent()
    # ram
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    # print(f"CPU: {cpu_percent}%")
    # print(f"memory: {memory_percent}%")
    # battery
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
        # print(f'Battery percentage: {battery_percent} %')
    else:
        # print('Battery not found')
        None
    return cpu_percent, memory_percent, battery_percent

## use fuzzy
def Fuzzy(cpu, ram, battery):
    power = Fuzzy_layer_1(cpu, ram)
    out = Fuzzy_layer_2(power, battery)

    # print(f"power: {power}, level: {out}.")
    return out