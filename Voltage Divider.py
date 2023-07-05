import operator
from Passives import Resistors



resistors = Resistors("Custom")
# resistors.expand_series()

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
        if rb != 0:
            vout = vIn / (1 + rt / rb)
            accuracy = (vout / vTarget - 1) * 100
            if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                (rt <= maxRt and rb <= maxRb) and
                ((accuracy >= 0 and acceptAbove == True) or (accuracy <= 0 and acceptBelow == True))):
                    allPairs.append({"Rt":rt,"Rb":rb, "Accuracy":accuracy})
                    if vout > vTarget*(1-tolerance) and vout < vTarget*(1+tolerance):
                        print(f"Rt = {rt}\tRb = {rb}\tAccuracy = {accuracy}")

allPairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in allPairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])

print(winningPair)
