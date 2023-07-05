import operator
import math
from Passives import Resistors, Capacitors



def metric_prefix_frequency(frequency):
    if frequency < 1.0e3:
        frequency = str(round(frequency, 1)) + "Hz"
    elif frequency < 1.0e6:
        frequency = str(round(frequency / 1.0e3, 1)) + "kHz"
    elif frequency < 1.0e9:
        frequency = str(round(frequency / 1.0e6, 1)) + "MHz"
    elif frequency < 1.0e12:
        frequency = str(round(frequency / 1.0e9, 1)) + "GHz"
    elif frequency < 1.0e15:
        frequency = str(round(frequency / 1.0e12, 1)) + "THz"
    else:
        frequency = "Greater than THz"
    return frequency

def metric_prefix_resistance(resistance):
    if resistance < 1.0e3:
        resistance = str(round(resistance, 2)) + "Ω"
    elif resistance < 1.0e6:
        resistance = str(round(resistance / 1.0e3, 2)) + "kΩ"
    elif resistance < 1.0e9:
        resistance = str(round(resistance / 1.0e6, 2)) + "MΩ"
    elif resistance < 1.0e12:
        resistance = str(round(resistance / 1.0e9, 2)) + "GΩ"
    elif resistance < 1.0e15:
        resistance = str(round(resistance / 1.0e12, 2)) + "TΩ"
    else:
        resistance = "Greater than T"
    return resistance

def metric_prefix_capacitance(capacitance):
    if capacitance < 1.0e-9:
        capacitance = str(round(capacitance * 1.0e12, 2)) + "pF"
    elif capacitance < 1.0e-6:
        capacitance = str(round(capacitance * 1.0e9, 2)) + "nF"
    elif capacitance < 1.0e-3:
        capacitance = str(round(capacitance * 1.0e6, 2)) + "µF"
    elif capacitance < 1.0:
        capacitance = str(round(capacitance * 1.0e3, 2)) + "mF"
    else:
        capacitance = "Greater than F"
    return capacitance

def metric_prefix_inductance(inductance):
    if inductance < 1.0e-12:
        inductance = str(round(inductance * 1.0e12, 2)) + "pH"
    elif inductance < 1.0e-9:
        inductance = str(round(inductance * 1.0e9, 2)) + "nH"
    elif inductance < 1.0e-6:
        inductance = str(round(inductance * 1.0e6, 2)) + "µH"
    elif inductance < 1.0e-3:
        inductance = str(round(inductance * 1.0e3, 2)) + "mH"
    else:
        inductance = "Greater than H"
    return inductance

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
                        allPairs.append({"Rt":{"Raw":rt, "Human Readable":metric_prefix_resistance(rt)},
                                         "Rb":{"Raw":rb, "Human Readable":metric_prefix_resistance(rb)},
                                         "Cb":{"Raw":cb, "Human Readable":metric_prefix_capacitance(cb)},
                                        #  "Accuracy":{"Raw":accuracy, "Human Readible":str(round(accuracy, 2))+"%"},
                                         "Accuracy":accuracy,
                                         "-3dB Frequency":{"Raw":frequency, "Human Readable":metric_prefix_frequency(frequency)}}),
                        if vout > vTarget*(1-tolerance) and vout < vTarget*(1+tolerance):
                            print(f"Rt = {metric_prefix_resistance(rt)}\tRb = {metric_prefix_resistance(rb)}\tCb = {metric_prefix_capacitance(cb)}\tAccuracy = {str(round(accuracy, 3))+'%'}\t-3dB Frequency = {metric_prefix_frequency(frequency)}")

allPairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in allPairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])

print(f"{'*'*10} Most Accurate {'*'*10}")
print(f"Rt = {winningPair['Rt']['Human Readable']}\tRb = {winningPair['Rb']['Human Readable']}\tCb = {winningPair['Cb']['Human Readable']}\tAccuracy = {str(round(winningPair['Accuracy'], 3))+'%'}\t-3dB Frequency = {winningPair['-3dB Frequency']['Human Readable']}")
