from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute
import numpy as np
from math import pi, acos
from qiskit import Aer
import matplotlib.pyplot as plt

n_qubits = 2
n = 2**(n_qubits)
mu = 1
sigma = 0.001

gaussian = np.zeros(n)

for i in range(n):
    gaussian[i] = np.exp(-(mu - i)**2 / (2 * sigma))
    
gaussian = gaussian / np.sum(gaussian)
    
qubits = QuantumRegister(n_qubits)
clbits = ClassicalRegister(n_qubits)
circuit = QuantumCircuit(qubits, clbits)

identity_0 = np.eye(2)
ones = np.ones(2)

p_l = np.dot(gaussian, np.kron(ones, identity_0[0, :]))
p_r = np.dot(gaussian, np.kron(ones, identity_0[1, :]))

cp_ll = gaussian[0] / p_l
cp_lr = gaussian[1] / p_l
cp_rl = gaussian[2] / p_r
cp_rr = gaussian[3] / p_r

theta_l = np.arccos(np.sqrt(p_l))
theta_ll = np.arccos(np.sqrt(cp_ll))
theta_rl = np.arccos(np.sqrt(cp_rl))


circuit.u3(2 * theta_l, 0, 0, qubits[-1])
circuit.cu3(2 * theta_ll, 0, 0, qubits[-1], qubits[-2])
circuit.x(qubits[-2])
circuit.cu3(2 * theta_rl, 0, 0, qubits[-1], qubits[-2])
circuit.x(qubits[-1])
circuit.measure(qubits, clbits)

backend = Aer.get_backend('qasm_simulator')
job_sim = execute(circuit, backend,)
sim_result = job_sim.result()

blob = sim_result.get_counts(circuit)

#histogram = np.zeros(4)

#histogram[0] = blob['00']
#histogram[1] = blob['01']
#histogram[2] = blob['10']
#histogram[3] = blob['11']

#print(blob)
"plt.plot(histogram)"
"plt.show()"

