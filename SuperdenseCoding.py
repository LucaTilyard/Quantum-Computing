from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import matplotlib.pyplot as plt
import numpy as np

# Generate bell state
alice = QuantumRegister(1, 'alice')
bob = QuantumRegister(1, 'bob')
alpha = ClassicalRegister(1, 'alpha')
beta = ClassicalRegister(1, 'beta')


qc = QuantumCircuit(alice, bob, alpha, beta)
qc.h(0)
qc.cx(0,1)
qc.barrier()
# Alice is trying to send Bob (1,1)
qc.z(0)
#qc.x(0)
qc.barrier()
# Bob receives the qubits
qc.cx(0,1)
qc.h(0)
qc.barrier()
qc.measure(alice, alpha)
qc.measure(bob, beta)

qc.draw(output='mpl')
plt.show()

# Instantiate a new statevector simulation based sampler object.
sampler = StatevectorSampler()

# Start a job that will return shots for all 100 parameter value sets.
job = sampler.run([qc], shots=256)

# Extract the result for the 0th pub (this example only has one pub).
result = job.result()[0]

# For small registers where it is anticipated to have many counts
# associated with the same bitstrings, we can turn the data from,
# for example, the 22nd sweep index into a dictionary of counts.
counts = result.data.alpha.get_counts(0)

# Or, convert into a list of bitstrings that preserve shot order.
bitstrings = result.data.alpha.get_bitstrings(0)

print(f"First Bit: {bitstrings[0]}")

counts2 = result.data.beta.get_counts(0)

# Or, convert into a list of bitstrings that preserve shot order.
bitstrings2 = result.data.beta.get_bitstrings(0)

print(f"Second Bit: {bitstrings2[0]}")