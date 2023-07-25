import cProfile
import pstats
import operator
import math
from Passives import Resistors
from Passives import readable_frequency
from Passives import readable_resistance



def comparator_with_hysteresis():
    tolerance = 1
    vcc = 3.3
    vSpreadTarget = 0.4
    minSeriesResistance = 0
    maxSeriesResistance = 999999999
    maxVhigh = vcc
    minVlow = 0.0

    tolerance /= 100
    allPairs = []
    validPairs = []
    vlow = 0.0
    vhigh = 0.0
    for rt in Resistors("Custom Resistors").values:
        for rb in Resistors("Custom Resistors").values:
            for rh in Resistors("Custom Resistors").values:
                if rb != 0 and rt != 0 and rh != 0:
                    vlow = vcc * rh * rb / (rh * (rb +rt) + rt * rb)
                    vhigh = vcc * rb * (rh + rt) / (rb * (rh + rt) + rt * rb)
                    vSpread = vhigh - vlow

                    if ((rt + rb >= minSeriesResistance) and (rt + rb <= maxSeriesResistance) and
                        (vhigh <= maxVhigh and vlow >= minVlow)):
                            allPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                            "Rh":{"Raw":rh, "Human Readable":readable_resistance(rh)},
                                            "Vlow":vlow,
                                            "Vhigh":vhigh,
                                            "Spread":vSpread})
                            if vSpread > vSpreadTarget*(1-tolerance) and vSpread < vSpreadTarget*(1+tolerance):
                                validPairs.append({"Rt":{"Raw":rt, "Human Readable":readable_resistance(rt)},
                                            "Rb":{"Raw":rb, "Human Readable":readable_resistance(rb)},
                                            "Rh":{"Raw":rh, "Human Readable":readable_resistance(rh)},
                                            "Vlow":vlow,
                                            "Vhigh":vhigh,
                                            "Spread":vSpread})

    validPairs.sort(reverse=True, key=operator.itemgetter("Spread"))
    for sample in validPairs:
        print(f"Rt = {sample['Rt']['Human Readable']}\tRb = {sample['Rb']['Human Readable']}\tRh = {sample['Rh']['Human Readable']}\tVlow = {sample['Vlow']:6.3f}V\tVHigh = {sample['Vhigh']:6.3f}V\tSpread = {sample['Spread']:6.3f}V")

comparator_with_hysteresis()
# profile = cProfile.Profile()
# profile.run('voltage_divider()')
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()
