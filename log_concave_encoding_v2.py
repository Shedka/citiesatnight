from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
from lineic_encoding_preparation import lineic_encoding
import numpy as np


#Verification of the compatibility of the array with the log-concave encoding


def is_distribution(distribution): #is the given array a distribution ?
    distribution = np.array(distribution)
    size = distribution.size
    distribution = lineic_encoding(distribution, vertical=False)
    is_distribution = False
    is_normalized = False
    is_positive = True
    if sum(distribution) == 1:
        is_normalized = True
    for i in range(size):
        if distribution[i] < 0:
            is_positive = False
    if is_normalized == True and is_positive == True:
        is_distribution = True
    return is_distribution

def is_log_concave(distribution): #is the given array a log-concave distribution ?
    something = True #have to define what condition must respect a log-concave distribution
    is_log_concave = False
    if is_distribution(distribution) == True and something == True:
        is_log_concave = True
    return is_log_concave
    
def is_log_concave_encoding_compatible(distribution, n_qubits): #is the given array an n_qubits-implementable log-concave distribution ?
    is_compatible = False
    distribution = np.array(distribution)
    if is_log_concave(distribution) == True and distribution.size % 2**(n_qubits) == 0:
        is_compatible = True
    return is_compatible


#How to map the indices of the arrays with the step number and the region number


def indices_regions(n_qubits): #give the indices of the region, to be improved
    dic = {}
    inter = 0
    for step in range(n_qubits):
        dic[step] = np.arange(2**(step + 1)) + inter
        inter = dic[step][-1] + 1
    return dic


def find_step(n_qubits, index): #if not break, error because of n_qubits + 1
    indices_search = list(indices_regions(n_qubits).values())
    for step in range(n_qubits + 1):
        if index in list(indices_search[step]):
            break
    return step


#Calculation of the angles needed for the log-concave encoding


def probabilities_values(distribution, n_qubits):
    distribution = np.array(distribution)
    size = distribution.size
    distribution = lineic_encoding(distribution, vertical=False) #add the possibility to use the vertical option
    if is_log_concave_encoding_compatible(distribution, n_qubits) == True:
        probabilities = {}
        for step in range(n_qubits):
            inter = []
            n_regions = 2**(step + 1)
            ones = np.ones(int(size / n_regions))
            identity = np.eye(n_regions)
            for index_region in range(n_regions):
                inter.append(np.dot(distribution, np.kron(identity[index_region, :], ones)))
            probabilities[step] = inter
        return probabilities
    else:
        raise NameError('The distribution is not compatible with the number of qubits or is not normalized or has negative values.')


def conditional_probabilities(distribution, n_qubits): #tested for n_qubits = 1 and 2
    conditional_probabilities = list(probabilities_values(distribution, n_qubits).values())
    for step in range(1, n_qubits):
        for index_region in range(2**(step + 1)):
            if conditional_probabilities[step - 1][index_region//2] == 0:
                conditional_probabilities[step][index_region] = 0
            else:
                conditional_probabilities[step][index_region] = conditional_probabilities[step][index_region] / conditional_probabilities[step - 1][index_region//2]
    return conditional_probabilities

def angles(distribution, n_qubits):
    sigma = conditional_probabilities(distribution, n_qubits)
    theta = np.zeros((n_qubits, 2**(n_qubits)))
    for step in range(n_qubits):
        for index_region in range(2**(step)):
            theta[step][index_region] = np.arccos(np.sqrt(sigma[step][2 * index_region]))
    return theta


#Log-concave encoding

            
#def log_concave_encoding(distribution, n_qubits):
#    return probabilities_values(distribution, n_qubits)
