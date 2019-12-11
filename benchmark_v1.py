from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
import numpy as np
from QRAM_encoding import qRAM_encoding
from qiskit.visualization import plot_histogram
from matplotlib.pyplot import savefig

n_qubits = 5
sigma = 1
mu = 2**(n_qubits - 1)

def gaussienne(sigma, mu, nb_points):
    gaussienne = []
    for i in range(nb_points):
        gaussienne.append(np.exp(-float((i - mu)**2) / (2 * sigma)))
    gaussienne = np.array(gaussienne)/sum(gaussienne)
    return gaussienne
    

circuit = qRAM_encoding(gaussienne(sigma, mu, 2**(n_qubits)), n_qubits)

q = circuit.qubits
c = circuit.clbits
circuit.measure(q, c)

backend = Aer.get_backend('qasm_simulator')

job_sim = execute(circuit, backend, shots=10000)

sim_result = job_sim.result()
plot_histogram(sim_result.get_counts(circuit)).savefig('gaussian_5_qubits.png')
