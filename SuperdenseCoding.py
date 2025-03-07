from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import matplotlib.pyplot as plt

# Take user input on what state to send.
Transmitted_state = input("Enter the state to send (00, 01, 10, 11): ")
Valid_states = ["00", "01", "10", "11"]

if Transmitted_state not in Valid_states:
    print("Invalid state. Try again using a state from the set {00, 01, 10, 11}.")
    exit()

print(f"Transmitted state: {Transmitted_state}")

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
if Transmitted_state == "10" or Transmitted_state == "11":
    qc.z(0)
if Transmitted_state == "01" or Transmitted_state == "11":
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
bitstring2 = result.data.beta.get_bitstrings(0)


print(f"Received state: {bitstring2[0]}{bitstring[0]}")

if Transmitted_state == f"{bitstring2[0]}{bitstring[0]}":
    print(" ✅ The state was successfully transmitted.")
else:
    raise Exception("The state was not successfully transmitted.")

exit()
