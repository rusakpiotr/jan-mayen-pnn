import random
import torch
import numpy as np
import matplotlib.pyplot as plt

from jan_mayen_pnn.tools.handle_json import load_data, get_weather_type_dict

import torch
import torch.nn as nn

class PatternLayer(nn.Module):
    def __init__(self, patterns, sigma=0.1):
        super().__init__()

        patterns = torch.as_tensor(patterns, dtype=torch.float32)

        mean = patterns.mean(dim=0)
        std = patterns.std(dim=0, correction=0).clamp_min(1e-6)

        self.register_buffer("mean", mean)
        self.register_buffer("std", std)
        self.register_buffer("patterns", (patterns - mean) / std)

        if sigma <= 0:
            raise ValueError("Sigma must be positive")

        self.sigma = sigma

    def forward(self, x):
        x = torch.as_tensor(
            x, dtype=self.patterns.dtype,
            device=self.patterns.device
        )

        if x.ndim == 1:
            x = x.unsqueeze(0)

        x = (x - self.mean) / self.std

        distances = torch.cdist(x, self.patterns)

        similarities = torch.exp(
            -distances.square() / (2 * self.sigma**2)
        )

        return similarities[0]

class AgregationLayer(torch.nn.Module):
    def __init__(self, labels):
        super().__init__()
        self.register_buffer(
            "labels",
            torch.tensor(labels, dtype=torch.long)
        )

    def forward(self, x):
        temp = torch.zeros(len(labels))
        for i in range(len(self.labels)):
            temp[self.labels[i]] += x[i]
        return temp

class DecisiveLayer(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        temp = np.argmax(x, axis=0)
        return temp

if __name__ == "__main__":
    data = load_data("dataset/observations.json")

    for _ in range(1):
        temp = [i for i in range(len(data))]
        test_indicies = random.choices(temp, k=len(data)//5)

        test_data = [data[n] for n in test_indicies]
        training_data = [data[n] for n in range(len(data)) if n not in test_indicies]

        patterns = [training_data[i][:-1] for i in range(len(training_data))]
        labels = [training_data[i][-1] for i in range(len(training_data))]

        pattern_layer = PatternLayer(patterns=patterns)
        agregation_layer = AgregationLayer(labels=labels)
        decisive_layer = DecisiveLayer()

        pnn = torch.nn.Sequential(
            pattern_layer,
            agregation_layer,
            decisive_layer
        )

        accuracies = dict()
        quantities = dict()

        for record in test_data:
            if pnn(torch.tensor(record[:-1], dtype=torch.float32).unsqueeze(0)) == record[-1]:
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
