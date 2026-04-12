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
    resistors = Resistors("E96").values
    capacitors = Capacitors("E6").values
    target_min_frequency = 500000.0
    target_max_frequency = 600000.0
    minResistance = 1000.0
    maxResistance = 100000.0
    minCapacitance = 100.0e-12
    maxCapacitance = 1.0e-6

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

    # pi = 3.14159

    # print("Sallen-Key Knee frequency")
    # K = 1 + 2/10
    # # RcustomSeries = expand_series(e96)
    # CcustomSeries = [0.1 / 1000000, 0.033 / 1000000]
    # for R1 in RcustomSeries:
    #     for R2 in RcustomSeries:
    #         for C1 in CcustomSeries:
    #             for C2 in CcustomSeries:
    #                 if R1 == 0.0 or R2 == 0.0:
    #                     continue
    #                 Fc=1/(2*pi*(R1*C1*R2*C2)**0.5)
    #                 Rtest = R1/R2
    #                 Radd = R1+R2
    #                 Ctest = C1/C2
    #                 if Ctest > 2 and Rtest >3.5 and Rtest <3.9 and Fc < 1000:
    #                     print(f"Fc = {Fc}\tR1 = {R1}\tR2 = {R2}\tC1 = {C1*1000000000}nF\tC2 = {C2*1000000000}nF")
    # print("\n")
