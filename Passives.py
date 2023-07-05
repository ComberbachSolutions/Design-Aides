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
