import operator



with open('E6.txt', 'r') as file:
    e6 = file.read().split("\n")
with open('E12.txt', 'r') as file:
    e12 = file.read().split("\n")
with open('E24.txt', 'r') as file:
    e24 = file.read().split("\n")
with open('E48.txt', 'r') as file:
    e48 = file.read().split("\n")
with open('E96.txt', 'r') as file:
    e96 = file.read().split("\n")
with open('E192.txt', 'r') as file:
    e192 = file.read().split("\n")
with open('Custom.txt', 'r') as file:
    custom = file.read().split("\n")

def convert_string_to_int(stringList):
    return [int(x) for x in stringList]

def expand_series(series):
    series = convert_string_to_int(series)
    for baseValue in series[::-1]:
        series.extend([int(baseValue)/100])
        series.extend([int(baseValue)/10])
        series.extend([int(baseValue)*10])
        series.extend([int(baseValue)*100])
        series.extend([int(baseValue)*1000])
    series.extend([1000000])
    series.sort()
    return series

def combine_series(seriesList1, seriesList2):
    seriesList1.extend(seriesList2)
    seriesList1 = list(set(seriesList1))
    seriesList1.sort()
    return seriesList1


resistors = convert_string_to_int(custom)

parallel_target = 609
series_target = 280
accuracy_target = 0.01
series_pairs = []
parallel_pairs = []

for r1 in resistors:
    for r2 in resistors:
        for r3 in resistors:
            if r1 < 1000000 and r2 < 1000000 and r3 < 1000000:
                series = r1 + r2 + r3
                series_accuracy = (series/series_target-1)*100
                series_pairs.append({"R1":r1, "R2":r2, "R3":r3, "Accuracy":series_accuracy})

            if r1 != 0 and r2 != 0 and r3 != 0:
                parallel = 1/(1/r1+1/r2)
                parallel_accuracy = (parallel/parallel_target-1)*100
                parallel_pairs.append({"R1":r1, "R2":r2, "Accuracy":parallel_accuracy})

series_pairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in series_pairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])
print(f"Series Winner: {winningPair}")

parallel_pairs.sort(key=operator.itemgetter("Accuracy"))
mostAccurate = 1000
winningPair = []
for sample in parallel_pairs:
    if abs(sample["Accuracy"]) < mostAccurate:
        winningPair = sample
        mostAccurate = abs(sample["Accuracy"])
print(f"Parallel Winner: {winningPair}")
