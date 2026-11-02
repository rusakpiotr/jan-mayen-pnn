import random
import numpy as np
import matplotlib.pyplot as plt

from jan_mayen_pnn.tools.handle_json import load_data, get_weather_type_dict

class Neuron:
    def __init__(self, pattern, label, sigma=1.0):
        self.pattern = np.asarray(pattern, dtype=float)
        self.l = label
        self.sigma = sigma
        self.o = 0.0

    def f(self, x):
        x = np.asarray(x, dtype=float)

        distance_squared = np.sum((x - self.pattern) ** 2)

        return np.exp(
            -distance_squared / (2 * self.sigma ** 2)
        )

class PNN:
    def __init__(self, training_data):
        self.training_data = training_data
        self.probabilistic_layer: list[Neuron] = self._fit()

    def _fit(self):
        probabilistic_layer = []
        for data in self.training_data:
            probabilistic_layer.append(Neuron(data[:-1], data[-1]))
        return probabilistic_layer

    def _calc_prob_layer(self, input: list) -> None:
        for i in range(len(self.probabilistic_layer)):
            n = self.probabilistic_layer[i]
            n.o = n.f(input)

    def _calc_argeg_layer(self) -> list:
        output = dict()
        for n in self.probabilistic_layer:
            if n.l not in output.keys():
                output[n.l] = 0
            output[n.l] += n.o
        return output

    def run(self, input: list):
        self._calc_prob_layer(input=input)
        result = None
        ma = float('-inf')
        for key, value in self._calc_argeg_layer().items():
            if value > ma:
                result = key
                ma = value
        return result

if __name__ == "__main__":
    data = load_data("dataset/observations.json")

    for _ in range(1):
        temp = [i for i in range(len(data))]
        test_indicies = random.choices(temp, k=len(data)//5)

        test_data = [data[n] for n in test_indicies]
        training_data = [data[n] for n in range(len(data)) if n not in test_indicies]

        pnn = PNN(training_data=training_data)

        accuracies = dict()
        quantities = dict()

        for record in test_data:
            if pnn.run(record[:-1]) == record[-1]:
                if record[-1] in accuracies.keys():
                    accuracies[record[-1]] += 1
                else:
                    accuracies[record[-1]] = 1
            if record[-1] in quantities.keys():
                quantities[record[-1]] += 1
            else:
                quantities[record[-1]] = 1

        print(f"Accuracy: {sum(accuracies.values())/len(test_data)}")

        codes = get_weather_type_dict()

        for key in accuracies.keys():
            accuracies[key] = accuracies[key] / quantities[key]
            print(f"{codes[key]}: {accuracies[key]}")
