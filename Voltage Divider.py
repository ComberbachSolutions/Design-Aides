import cProfile
import pstats
import operator
import math
from Passives import Resistors, Capacitors
from Passives import readable_frequency
from Passives import readable_resistance
from Passives import readable_capacitance



def voltage_divider():
    Rtop = Resistors("Custom Resistors").values
    Rbot = Resistors("Custom Resistors").values
    Cbot = Capacitors("Custom Capacitors").values
    tolerance = 1
    vIn = 1
    vTarget = 0.6
    acceptAbove = True
    acceptBelow = True
    minSeriesResistance = 0
    maxSeriesResistance = 999999999
    maxRt = 999999999
    maxRb = 999999999

    tolerance /= 100
    allPairs = []
    validPairs = []
    for rt in Rtop:
        for rb in Rbot:
            for cb in Cbot:
                if rb != 0 and rt != 0 and cb != 0:
                    vout = vIn / (1 + rt / rb)
                    accuracy = (vout / vTarget - 1) * 100
                    frequency = (1 + rb / rt) / (2 * math.pi * cb * rb)
                        
                    if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                        (rt <= maxRt and rb <= maxRb) and
                        ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                            allPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                            "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                            #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                            "Accuracy":accuracy,
                                            "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})
                            if vout > vTarget*(1-tolerance) and vout < vTarget*(1+tolerance):
                                validPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                                "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                                "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                                #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                                "Accuracy":accuracy,
                                                "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})

    validPairs.sort(key=operator.itemgetter("Accuracy"))
    for sample in validPairs:
        print(f"Rt = {sample['Rt']['Human Readable']}\tRb = {sample['Rb']['Human Readable']}\tCb = {sample['Cb']['Human Readable']}\tAccuracy = {sample['Accuracy']:6.3f}%\t-3dB Frequency = {sample['-3dB Frequency']['Human Readable']}")

    allPairs.sort(key=operator.itemgetter("Accuracy"))
    mostAccurate = 1000
    winningPair = []
    for sample in allPairs:
        if abs(sample["Accuracy"]) < mostAccurate:
            winningPair = sample
            mostAccurate = abs(sample["Accuracy"])

    print(f"{'*'*10} Most Accurate {'*'*10}")
    print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {winningPair['Accuracy']:6.3f}%\t-3dB Frequency = {winningPair['-3dB Frequency']['Human Readable']}")

# profile = cProfile.Profile()
# profile.run('voltage_divider()')
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()

voltage_divider()
