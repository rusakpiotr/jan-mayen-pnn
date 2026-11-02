

import os
import torch
import torch.nn as nn
import pyro
import pyro.distributions as dist
import pyro.poutine as poutine
from torch.distributions import constraints
from pyro.nn import PyroModule, PyroParam, PyroSample
from pyro.nn.module import to_pyro_module_
from pyro.infer import SVI, Trace_ELBO
from pyro.infer.autoguide import AutoNormal
from pyro.optim import Adam

smoke_test = ('CI' in os.environ)
# assert pyro.__version__.startswith('1.9.1')


class Linear(nn.Module):
    def __init__(self, in_size, out_size):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_size, out_size))
        self.bias = nn.Parameter(torch.randn(out_size))

    def forward(self, input_):
        return self.bias + input_ @ self.weight

linear = Linear(5, 2)
assert isinstance(linear, nn.Module)
assert not isinstance(linear, PyroModule)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)

class PyroLinear(Linear, PyroModule):
    pass

linear = PyroLinear(5, 2)
assert isinstance(linear, nn.Module)
assert isinstance(linear, Linear)
assert isinstance(linear, PyroModule)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)


linear = PyroModule[Linear](5, 2)
assert isinstance(linear, nn.Module)
assert isinstance(linear, Linear)
assert isinstance(linear, PyroModule)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)

linear = Linear(5, 2)
assert isinstance(linear, nn.Module)
assert not isinstance(linear, PyroModule)

to_pyro_module_(linear)  # this operates in-place
assert isinstance(linear, nn.Module)
assert isinstance(linear, Linear)
assert isinstance(linear, PyroModule)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)


pyro.clear_param_store()

# This is not traced:
linear = Linear(5, 2)
with poutine.trace() as tr:
    linear(example_input)
print(type(linear).__name__)
print(list(tr.trace.nodes.keys()))
print(list(pyro.get_param_store().keys()))

# Now this is traced:
to_pyro_module_(linear)
with poutine.trace() as tr:
    linear(example_input)
print(type(linear).__name__)
print(list(tr.trace.nodes.keys()))
print(list(pyro.get_param_store().keys()))

print("params before:", [name for name, _ in linear.named_parameters()])

linear.bias = PyroParam(torch.randn(2).exp(), constraint=constraints.positive)
print("params after:", [name for name, _ in linear.named_parameters()])
print("bias:", linear.bias)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)

print("params before:", [name for name, _ in linear.named_parameters()])

linear.weight = PyroSample(dist.Normal(0, 1).expand([5, 2]).to_event(2))
print("params after:", [name for name, _ in linear.named_parameters()])
print("weight:", linear.weight)
print("weight:", linear.weight)

example_input = torch.randn(100, 5)
example_output = linear(example_input)
assert example_output.shape == (100, 2)

