from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import matplotlib.pyplot as plt


# Generate bell state.
alice = QuantumRegister(1, 'alice')
bob = QuantumRegister(1, 'bob')
alpha = ClassicalRegister(1, 'alpha')
beta = ClassicalRegister(1, 'beta')

# Construst the circuit.
qc = QuantumCircuit(alice, bob, alpha, beta)
qc.h(0)
qc.cx(0,1)
qc.barrier()

# Add gates depending on the message.
# 00 -> Do nothing
# 10 -> Apply Z gate
# 01 -> Apply X gate
# 11 -> Apply Z and X gate
qc.z(0)
qc.x(0)

qc.barrier()

# Send Qubits to Bob.
qc.cx(0,1)
qc.h(0)
qc.barrier()
qc.measure(alice, alpha)
qc.measure(bob, beta)

# Draw and optionally save image of the circuit.
qc.draw(output='mpl')
#plt.savefig("11.png")
plt.show()


# Instantiate a new statevector simulation based sampler object.
sampler = StatevectorSampler()

# Start a job.
job = sampler.run([qc], shots=1)

# Extract the result for the 0th pub (this example only has one pub).
result = job.result()[0]


# Convert into a list of bitstrings.
bitstring = result.data.alpha.get_bitstrings(0)
print(f"First Bit: {bitstring[0]}")

# Convert into a list of bitstrings.
bitstring2 = result.data.beta.get_bitstrings(0)
print(f"Second Bit: {bitstring2[0]}")

