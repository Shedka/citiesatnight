from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
import log_concave_encoding_v2

A = [0, 0.25, 0.25, 0]
angles = log_concave_encoding_v2.angles(A, 2)

q = QuantumRegister(2)
c = ClassicalRegister(2)
circuit = QuantumCircuit(q, c)

circuit.u3(2 * angles[0][0], 0, 0, q[1]) #Ry d'angle 2*theta
circuit.x(q[1])
circuit.cu3(2 * angles[1][0], 0, 0, q[1], q[0])
circuit.x(q[1])
circuit.cu3(2 * angles[1][1], 0, 0, q[1], q[0])
circuit.measure(q, c)


backend = Aer.get_backend('qasm_simulator')
job_sim = execute(circuit, backend, shots=10000)

sim_result = job_sim.result()
print(sim_result.get_counts(circuit))



#A = [1, 0, 0, 0, 0, 0, 0, 0]
#theta = theta(A, 3)

#q = QuantumRegister(3)
#c = ClassicalRegister(3)
#circuit = QuantumCircuit(q, c)

#Ry sur le qubit de poids fort

#circuit.u3(2 * theta[0][0], 0, 0, q[2]) 

#cRy sur le deuxième qubit

#circuit.x(q[2])
#circuit.cu3(2 * theta[1][0], 0, 0, q[2], q[1])
#circuit.x(q[2])
#circuit.cu3(2 * theta[1][1], 0, 0, q[2], q[1])

#cRy sur le qubit de poids faible





#circuit.measure(q, c)


#backend = Aer.get_backend('qasm_simulator')
#job_sim = execute(circuit, backend, shots=10000)

#sim_result = job_sim.result()
#print(sim_result.get_counts(circuit))


