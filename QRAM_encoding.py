from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from data_preparation import lineic_encoding, is_stochastic_vector
import numpy as np
from numpy.linalg import norm
from qiskit.aqua.circuits.gates import mcry



def euclidean_norm(sub_distribution):
    if type(sub_distribution) == int or type(sub_distribution) == float:
        return np.sqrt(sub_distribution ** 2)
    else:
        return norm(sub_distribution)


def is_log_concave(distribution): #is the given array a log-concave stochastic vector ?
    something = True #have to define what condition must respect a log-concave distribution
    is_log_concave = False
    if is_stochastic_vector(distribution) == True and something == True:
        is_log_concave = True
    return is_log_concave
    

def is_log_concave_encoding_compatible(distribution, n_qubits): #is the given array an n_qubits-implementable log-concave distribution ?
    is_compatible = False
    distribution = np.array(distribution)
    if is_log_concave(distribution) == True and distribution.size % 2**(n_qubits) == 0:
        is_compatible = True
    return is_compatible


def to_bin(region, step):
    to_bin = format(region, 'b')
    if len(to_bin) != step:
        difference = step - len(to_bin)
        while(difference != 0):
            to_bin = '0' + to_bin
            difference = difference - 1
    return to_bin


def angles(distribution, n_qubits):       
    distribution = np.array(distribution)
    size = distribution.size
    distribution = lineic_encoding(distribution, vertical=False)
    if is_log_concave_encoding_compatible(distribution, n_qubits) == True:
        distribution = np.sqrt(distribution)
        angles = {}
        for step in range(n_qubits):
            inter = 2**(step)
            limit_region = int(size / (inter * 2)) * np.arange(inter * 2 + 1)
            inter_list = []
            for region in range(inter):
                if  euclidean_norm(distribution[limit_region[2 * region]:limit_region[2 * region + 1]]) == 0:
                    inter_list.append(np.pi/2)
                else:
                    inter_list.append(np.arctan2(euclidean_norm(distribution[limit_region[2 * region + 1]:limit_region[2 * region + 2]]), euclidean_norm(distribution[limit_region[2 * region]:limit_region[2 * region + 1]])))
            angles[step] = inter_list
        return angles
    else:
        raise NameError('The distribution is not compatible with the number of qubits or is not normalized or has negative values.')
        
        
def x_gates_region(circuit, string):
    qubits = circuit.qubits
    n_qubits = circuit.n_qubits
    for i in range(len(string)):
        if string[i] == '0':
              circuit.x(qubits[n_qubits - i - 1])
    return circuit 
        

def qRAM_encoding(distribution, n_qubits):
    theta = angles(distribution, n_qubits)
    qubits = QuantumRegister(n_qubits)
    clbits = ClassicalRegister(n_qubits)
    circuit = QuantumCircuit(qubits, clbits)   
    circuit.u3(2 * theta[0][0], 0, 0, qubits[n_qubits - 1])
    for step in range(n_qubits - 1):
        step = step + 1
        controller_qubits = list(map(lambda x: qubits[n_qubits - x - 1], range(step)))
        for region in range(2 ** step):
            circuit = x_gates_region(circuit, to_bin(region, step))
            circuit.mcry(- 2 * theta[step][region], controller_qubits, qubits[n_qubits - step - 1], None, 'noancilla')
            circuit = x_gates_region(circuit, to_bin(region, step))        
    return circuit
