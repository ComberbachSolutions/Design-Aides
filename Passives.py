class Passive():
    def __init__(self, series):
        match series:
            case "E6":
                with open('E Series\E6.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "E12":
                with open('E Series\E12.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "E24":
                with open('E Series\E24.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "E48":
                with open('E Series\E48.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "E96":
                with open('E Series\E96.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "E192":
                with open('E Series\E192.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "Custom Resistors":
                with open('Custom Resistors.txt', 'r') as file:
                    self.values = file.read().split("\n")
            case "Custom Capacitors":
                with open('Custom Capacitors.txt', 'r') as file:
                    self.values = file.read().split("\n")
        
        self.values = self.string_list_to_floats(self.values)

    def string_list_to_floats(self, string_list):
        return [float(x) for x in string_list]

    def combine_series(self, seriesList1, seriesList2):
        seriesList1.extend(seriesList2)
        seriesList1 = list(set(seriesList1))
        seriesList1.sort()
        return seriesList1

class Resistors(Passive):
    def expand_series(self):
        for value in self.values[::-1]:
            self.values.extend([value/100.0])
            self.values.extend([value/10.0])
            self.values.extend([value*10.0])
            self.values.extend([value*100.0])
            self.values.extend([value*1000.0])
        self.values.extend([1000000.0])
        self.values.extend([999999999.0])
        self.values.sort()

class Capacitors(Passive):
    def expand_series(self):
        for value in self.values[::-1]:
            self.values.extend([value/100000000000000.0])
            self.values.extend([value/10000000000000.0])
            self.values.extend([value/1000000000000.0])
            self.values.extend([value/100000000000.0])
            self.values.extend([value/10000000000.0])
            self.values.extend([value/1000000000.0])
            self.values.extend([value/100000000.0])
            self.values.extend([value/10000000.0])
            self.values.extend([value/1000000.0])
            self.values.remove(value)
        self.values.extend([0.001])
        self.values.sort()

class Inductors(Passive):
    def expand_series(self):
        for value in self.values[::-1]:
            self.values.extend([value/100000000000000.0])
            self.values.extend([value/10000000000000.0])
            self.values.extend([value/1000000000000.0])
            self.values.extend([value/100000000000.0])
            self.values.extend([value/10000000000.0])
            self.values.extend([value/1000000000.0])
            self.values.extend([value/100000000.0])
            self.values.extend([value/10000000.0])
            self.values.extend([value/1000000.0])
            self.values.remove(value)
        self.values.extend([0.001])
        self.values.sort()

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
