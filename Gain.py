# import cProfile
# import pstats
# import scalene
import operator
import math
from Passives import Resistors, Capacitors
from Passives import readable_frequency
from Passives import readable_resistance
from Passives import readable_capacitance



def voltage_divider():
    Rtop = Resistors("Custom Resistors").values
    Rbot = Resistors("Custom Resistors").values
    Rbot2 = Resistors("Custom Resistors").values
    Cbot = Capacitors("Custom Capacitors").values
    tolerancePercent = 1
    targetGain = 37.5
    acceptAbove = True
    acceptBelow = True
    minSeriesResistance = 10000
    maxSeriesResistance = 1000000
    maxRt = 1000000
    maxRb = 1000000

    tolerancePercent /= 100
    allPairs = []
    validPairs = []
    for rt in Rtop:
        if rt == 0:
            continue
        for rb in Rbot:
            for rb2 in Rbot2:
                if rb == 0:
                    continue
                if rb2 == 0:
                    continue
                for cb in Cbot:
                    if cb == 0:
                        continue

                    gain = rt / (rb+rb2)
                    accuracy = (gain / targetGain - 1) * 100
                        
                    if ((rt + (rb+rb2) >= minSeriesResistance) and (rt + (rb+rb2) <= maxSeriesResistance) and
                        (rt <= maxRt and (rb+rb2) <= maxRb) and
                        (rb > (100*rb2)) and
                        ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                            allPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":(rb), "Human Readable":readable_resistance((rb))},
                                            "Rb2":{"Raw":(rb2), "Human Readable":readable_resistance((rb2))},
                                            "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                            #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                            "Accuracy":accuracy,})
                            if gain > targetGain*(1-tolerancePercent) and gain < targetGain*(1+tolerancePercent):
                                validPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                                "Rb":{"Raw":(rb), "Human Readable":readable_resistance((rb))},
                                                "Rb2":{"Raw":(rb2), "Human Readable":readable_resistance((rb2))},
                                                "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                                #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                                "Accuracy":accuracy,})

    validPairs.sort(key=operator.itemgetter("Accuracy"))
    for sample in validPairs:
        print(f"Rt = {sample['Rt']['Human Readable']}\tRb = {sample['Rb']['Human Readable']}\tRb2 = {sample['Rb2']['Human Readable']}\tCb = {sample['Cb']['Human Readable']}\tAccuracy = {sample['Accuracy']:6.3f}%")

    allPairs.sort(key=operator.itemgetter("Accuracy"))
    mostAccurate = 1000
    winningPair = []
    for sample in allPairs:
        if abs(sample["Accuracy"]) < mostAccurate:
            winningPair = sample
            mostAccurate = abs(sample["Accuracy"])

    print(f"{'*'*10} Most Accurate {'*'*10}")
    print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tRb2 = {sample['Rb2']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {winningPair['Accuracy']:6.3f}%")

# profile = cProfile.Profile()
# profile.run('voltage_divider()')
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()

# scalene "voltage divider.py"
voltage_divider()
