from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
from log_concave_encoding_v3 import angles
from qiskit.aqua.circuits.gates import mcry

A = np.array([0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]) #FAIRE LES ROTATIONS

#With 3 qubits

theta_3 = angles(A, 3)

q_3 = QuantumRegister(3)
c_3 = ClassicalRegister(3)
circuit_3 = QuantumCircuit(q_3, c_3)


circuit_3.u3(2 * theta_3[0][0], 0, 0, q_3[2])

circuit_3.x(q_3[2])
circuit_3.mcry(2 * theta_3[1][0], [q_3[2]], q_3[1], None)
circuit_3.x(q_3[2])
circuit_3.mcry(2 * theta_3[1][1], [q_3[2]], q_3[1], None)

circuit_3.x(q_3[2]) #Rotation 00
circuit_3.x(q_3[1])
circuit_3.mcry(2 * theta_3[2][0], [q_3[2], q_3[1]], q_3[0], None)
circuit_3.x(q_3[2])
circuit_3.x(q_3[1])

circuit_3.x(q_3[2]) #Rotation 01
circuit_3.mcry(2 * theta_3[2][1], [q_3[2], q_3[1]], q_3[0], None)
circuit_3.x(q_3[2])

circuit_3.x(q_3[1]) #Rotation 10
circuit_3.mcry(2 * theta_3[2][2], [q_3[2], q_3[1]], q_3[0], None)
circuit_3.x(q_3[1])

circuit_3.mcry(2 * theta_3[2][3], [q_3[2], q_3[1]], q_3[0], None) #Rotation 11


circuit_3.measure(q_3, c_3)


backend = Aer.get_backend('qasm_simulator')

job_sim = execute(circuit_3, backend, shots=10000)

sim_result = job_sim.result()
print(sim_result.get_counts(circuit_3))

#Avec log_concave_encoding

n_qubits = 3

circuit = log_concave_encoding(A, n_qubits)
q = circuit.qubits
c = circuit.clbits
circuit.measure(q, c)

backend = Aer.get_backend('qasm_simulator')

job_sim = execute(circuit, backend, shots=10000)

sim_result = job_sim.result()
print(sim_result.get_counts(circuit))