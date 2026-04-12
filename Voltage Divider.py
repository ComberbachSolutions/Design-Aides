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
    Rtop = Resistors("E All").values
    Rbot = Resistors("E All").values
    Cbot = Capacitors("100nF Capacitor").values
    tolerancePercent = 1
    vIn = 37
    vOutTarget = 1.2
    acceptAbove = True
    acceptBelow = True
    minSeriesResistance = 0
    maxSeriesResistance = 1000000
    minRt = 0
    maxRt = 1000000
    minRb = 0
    maxRb = 1000000

    tolerancePercent /= 100
    allPairs = []
    validPairs = []
    for rt in Rtop:
        if rt == 0:
            continue
        for rb in Rbot:
            if rb == 0:
                continue
            for cb in Cbot:
                if cb == 0:
                    continue

                vout = vIn / (1 + rt / rb)
                accuracy = (vout / vOutTarget - 1) * 100
                frequency = (1 + rb / rt) / (2 * math.pi * cb * rb)

                if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                    (rt >= minRt and rb >= minRb) and
                    (rt <= maxRt and rb <= maxRb) and
                    ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                        allPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                        "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                        "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                        #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                        "Accuracy":accuracy,
                                        "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})
                        if vout > vOutTarget*(1-tolerancePercent) and vout < vOutTarget*(1+tolerancePercent):
                            validPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                            "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                            #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                            "Accuracy":accuracy,
                                            "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})

    validPairs.sort(key=operator.itemgetter("Accuracy"))
    for sample in validPairs:
        print(f"Rt = {sample['Rt']['Human Readable']}\tRb = {sample['Rb']['Human Readable']}\tCb = {sample['Cb']['Human Readable']}\tAccuracy = {sample['Accuracy']:6.3f}%\t-3dB Frequency = {sample['-3dB Frequency']['Human Readable']}\tVout at Vin({vIn}V) = {vIn/(1+sample['Rt']['Raw']/sample['Rb']['Raw']):>.3f}V")

    allPairs.sort(key=operator.itemgetter("Accuracy"))
    mostAccurate = 1000
    winningPair = []
    for sample in allPairs:
        if abs(sample["Accuracy"]) < mostAccurate:
            winningPair = sample
            mostAccurate = abs(sample["Accuracy"])

    print(f"{'*'*10} Most Accurate {'*'*10}")
    print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {winningPair['Accuracy']:6.3f}%\t-3dB Frequency = {winningPair['-3dB Frequency']['Human Readable']}\tVout at Vin({vIn}V) = {vIn/(1+winningPair['Rt']['Raw']/winningPair['Rb']['Raw']):>.3f}V")

def inverse_voltage_divider():
    Rtop = Resistors("SMG Resistors").values
    Rbot = Resistors("SMG Resistors").values
    Cbot = Capacitors("100nF Capacitor").values
    tolerancePercent = 1
    vInTarget = 37
    vOut = 1.2
    acceptAbove = True
    acceptBelow = True
    minSeriesResistance = 21000
    maxSeriesResistance = 1000000
    minRt = 0
    maxRt = 1000000
    minRb = 0
    maxRb = 1000000

    tolerancePercent /= 100
    allPairs = []
    validPairs = []
    for rt in Rtop:
        if rt == 0:
            continue
        for rb in Rbot:
            if rb == 0:
                continue
            for cb in Cbot:
                if cb == 0:
                    continue

                vin = vOut * (1 + rt / rb)
                accuracy = (vin / vInTarget - 1) * 100
                frequency = (1 + rb / rt) / (2 * math.pi * cb * rb)

                if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                    (rt >= minRt and rb >= minRb) and
                    (rt <= maxRt and rb <= maxRb) and
                    ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                        allPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                        "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                        "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                        #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                        "Accuracy":accuracy,
                                        "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})
                        if vin > vInTarget*(1-tolerancePercent) and vin < vInTarget*(1+tolerancePercent):
                            validPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                            "Cb":{"Raw":cb, "Human Readable":readable_capacitance(cb)},
                                            #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                            "Accuracy":accuracy,
                                            "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}})

    validPairs.sort(key=operator.itemgetter("Accuracy"))
    for sample in validPairs:
        print(f"Rt = {sample['Rt']['Human Readable']}\tRb = {sample['Rb']['Human Readable']}\tCb = {sample['Cb']['Human Readable']}\tAccuracy = {sample['Accuracy']:6.3f}%\t-3dB Frequency = {sample['-3dB Frequency']['Human Readable']}\tVin at Vout({vOut}V) = {vOut*(1+sample['Rt']['Raw']/sample['Rb']['Raw']):>.3f}V")

    allPairs.sort(key=operator.itemgetter("Accuracy"))
    mostAccurate = 1000
    winningPair = []
    for sample in allPairs:
        if abs(sample["Accuracy"]) < mostAccurate:
            winningPair = sample
            mostAccurate = abs(sample["Accuracy"])

    print(f"{'*'*10} Most Accurate {'*'*10}")
    print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {winningPair['Accuracy']:6.3f}%\t-3dB Frequency = {winningPair['-3dB Frequency']['Human Readable']}\tVin at Vout({vOut}V) = {vOut*(1+winningPair['Rt']['Raw']/winningPair['Rb']['Raw']):>.3f}V")

# profile = cProfile.Profile()
# profile.run('voltage_divider()')
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()

# scalene "voltage divider.py"
# voltage_divider()
inverse_voltage_divider()
