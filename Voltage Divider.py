import operator
import math
from Passives import Resistors, Capacitors



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
                if frequency < 1.0e3:
                    critical_frequency = str(round(frequency, 1)) + "Hz"
                elif frequency < 1.0e6:
                    critical_frequency = str(round(frequency / 1.0e3, 1)) + "kHz"
                elif frequency < 1.0e9:
                    critical_frequency = str(round(frequency / 1.0e6, 1)) + "MHz"
                elif frequency < 1.0e12:
                    critical_frequency = str(round(frequency / 1.0e9, 1)) + "GHz"
                elif frequency < 1.0e15:
                    critical_frequency = str(round(frequency / 1.0e12, 1)) + "THz"
                else:
                    print("Error")
                    
                if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                    (rt <= maxRt and rb <= maxRb) and
                    ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                        allPairs.append({"Rt":rt,"Rb":rb, "Cb":cb, "Accuracy":accuracy, "-3dB Frequency":critical_frequency})
                        if vout > vTarget*(1-tolerance) and vout < vTarget*(1+tolerance):
                            print(f"Rt = {rt}\tRb = {rb}\tCb = {cb}\tAccuracy = {accuracy}\t-3dB Frequency = {critical_frequency}")

allPairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in allPairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])

print(winningPair)
