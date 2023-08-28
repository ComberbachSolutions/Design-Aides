import cProfile
import pstats
import operator
import math
from Passives import Resistors, Capacitors
from Passives import readable_frequency
from Passives import readable_resistance
from Passives import readable_capacitance

def low_pass_sallen_key_simple():
    # Resistors and capacitors are all the same value
    # There is no gain
    # Q is alway 0.5
    resistors = Resistors("Custom Resistors").values
    capacitors = Capacitors("Custom Capacitors").values
    target_min_frequency = 1000.0
    target_max_frequency = 10000.0
    minResistance = 100.0
    maxResistance = 100000.0
    minCapacitance = 100.0e-12
    maxCapacitance = 100.0e-6

    solutions = []
    for R in resistors:
        if R == 0:
             continue
        for C in capacitors:
            if C == 0:
                 continue
            Fc = 1 / (2 * math.pi * R * C)
            Q = 0.5

            if ((R >= minResistance and R <= maxResistance) and
                (C >= minCapacitance and C <= maxCapacitance) and
                (Fc >= target_min_frequency and Fc <= target_max_frequency)):
                    solutions.append({"R1":{"Raw":R, "Human Readable":readable_resistance(R)},
                                     "R2":{"Raw":R, "Human Readable":readable_resistance(R)},
                                     "C1":{"Raw":C, "Human Readable":readable_capacitance(C)},
                                     "C2":{"Raw":C, "Human Readable":readable_capacitance(C)},
                                    "-3dB Frequency":{"Raw":Fc, "Human Readable":readable_frequency(Fc)},
                                     "Q":{"Raw":0.5}})

    for sample in solutions:
        print(f"R1 = {sample['R1']['Human Readable']}\tR2 = {sample['R2']['Human Readable']}\tC1 = {sample['C1']['Human Readable']}\tC1 = {sample['C2']['Human Readable']}\tFc = {sample['-3dB Frequency']['Human Readable']}\tQ = {sample['Q']}")

low_pass_sallen_key_simple()

