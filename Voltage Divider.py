import operator
import math
from Passives import Resistors, Capacitors



def metric_prefix(value):
    if value < 1.0e-9:
        value = str(round(value * 1.0e12, 2)) + "p"
    elif value < 1.0e-6:
        value = str(round(value * 1.0e9, 2)) + "n"
    elif value < 1.0e-3:
        value = str(round(value * 1.0e6, 2)) + "µ"
    elif value < 1.0e0:
        value = str(round(value * 1.0e3, 2)) + "m"
    elif value < 1.0e3:
        value = str(round(value, 1))
    elif value < 1.0e6:
        value = str(round(value / 1.0e3, 2)) + "k"
    elif value < 1.0e9:
        value = str(round(value / 1.0e6, 2)) + "M"
    elif value < 1.0e12:
        value = str(round(value / 1.0e9, 2)) + "G"
    elif value < 1.0e15:
        value = str(round(value / 1.0e12, 2)) + "T"
    else:
        value = "Greater than T"
    return value

def readable_frequency(frequency):
    return metric_prefix(frequency) + "Hz"

def readable_resistance(resistance):
    return metric_prefix(resistance) + "Ω"

def readable_capacitance(capacitance):
    return metric_prefix(capacitance) + "F"

def readable_inductance(inductance):
    return metric_prefix(inductance) + "H"

resistors = Resistors("Custom Resistors")
# resistors.expand_series()

capacitors = Capacitors("Custom Capacitors")
# capacitors.expand_series()

tolerance = 10
vIn = 1
vTarget = 0.2021
acceptAbove = True
acceptBelow = True
minSeriesResistance = 0
maxSeriesResistance = 999999999
maxRt = 999999999
maxRb = 999999999

tolerance /= 100
allPairs = []
for rt in resistors.values:
    for rb in resistors.values:
        for cb in capacitors.values:
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
                                         "-3dB Frequency":{"Raw":frequency, "Human Readable":readable_frequency(frequency)}}),
                        if vout > vTarget*(1-tolerance) and vout < vTarget*(1+tolerance):
                            print(f"Rt = {readable_resistance(rt)}\tRb = {readable_resistance(rb)}\tCb = {readable_capacitance(cb)}\tAccuracy = {str(round(accuracy, 3))+'%'}\t-3dB Frequency = {readable_frequency(frequency)}")

allPairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in allPairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])

print(f"{'*'*10} Most Accurate {'*'*10}")
print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {str(round(winningPair['Accuracy'], 3))+'%'}\t-3dB Frequency = {winningPair['-3dB Frequency']['Human Readable']}")
