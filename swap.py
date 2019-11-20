from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, QuantumRegister
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram, circuit_drawer
from qiskit import execute, Aer, BasicAer
import numpy as np
import matplotlib.pyplot as plt
from resizeimage import resizeimage
from PIL import Image

import frqi

def image_normalization(image):
    image = resizeimage.resize_cover(image, [32, 32])
    w, h = 32, 32
    image = np.array([[image.getpixel((x,y))[0] for x in range(w)] for y in range(h)])

    # 2-dimentional data convert to 1-dimentional array
    image = image.flatten()
    # change type
    image = image.astype('float64')
    # Normalization(0~pi/2)
    image /= 255.0
    generated_image = np.arcsin(image)

    return generated_image

def swap_12(circuit, q0, q1, q2, classic):
    
    circuit.tdg(q0[0])
    circuit.h(q0[0])

    for i in range(len(q1)):
        circuit.cswap(q0[0], q1[i], q2[i])
    
    circuit.h(q0[0])
    circuit.tdg(q0[0])

    circuit.measure(q0[0], classic)

    numOfShots = 1024
    result = execute(circuit, provider.get_backend('ibmq_qasm_simulator'), shots=numOfShots).result()

    return result.get_counts(circuit)

if __name__ == '__main__':
    imageNames = ["Ref_Tokyo_grayscale.jpg", "Tokyo_grayscale.jpg", "Sapporo_grayscale.jpg"]
    imgnum1 = 0
    imgnum2 = 2

    img1 = Image.open(imageNames[imgnum1]).convert('LA')
    img2 = Image.open(imageNames[imgnum2]).convert('LA')
    
    img1 = image_normalization(img1)
    img2 = image_normalization(img2)

    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q-keio', group='keio-internal', project='keio-students')

    targetQubit = QuantumRegister(1, 'target')
    ref = QuantumRegister(11, 'ref')
    original = QuantumRegister(11, 'original')
    anc = QuantumRegister(1, 'anc')

    c = ClassicalRegister(1)

    qc = QuantumCircuit(targetQubit, ref, original, anc, c)


    # apply hadamard gates
    for i in range(1, len(ref)):
        qc.h(ref[i])

    for i in range(1, len(original)):
        qc.h(original[i])

    #qc.h([ref[i] for i in range(1,len(ref))])
    #qc.h([original[i] for i in range(1,len(original))])

    # encode ref image
    for i in range(len(img1)):
            if img1[i] != 0:
                    frqi.c10ry(qc, 2 * img1[i], format(i, '010b'), ref[0], anc[0], [ref[j] for j in range(1,len(ref))])

    # encode original image
    for i in range(len(img2)):
            if img2[i] != 0:
                    frqi.c10ry(qc, 2 * img2[i], format(i, '010b'), original[0], anc[0], [original[j] for j in range(1,len(original))])

    print(swap_12(qc, targetQubit, ref, original, c))