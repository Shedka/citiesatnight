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
import quantum_edge_detection as qed

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q-keio', group='keio-internal', project='keio-students')

anc = QuantumRegister(1, "anc")
img = QuantumRegister(11, "img")
anc2 = QuantumRegister(1, "anc2")
c = ClassicalRegister(12)

qc = QuantumCircuit(anc, img, anc2, c)

imageNames = ["Ref_Tokyo_grayscale.jpg", "Tokyo_grayscale.jpg", "Sapporo_grayscale.jpg"]
imageNum1 = 0
imageNum2 = 2

image1 = Image.open(imageNames[imageNum1]).convert('LA')
image2 = Image.open(imageNames[imageNum2]).convert('LA')

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

image1 = image_normalization(image1)
image2 = image_normalization(image2)


# apply hadamard gates
for i in range(1, len(img)):
    qc.h(img[i])

# encode ref image
for i in range(len(image1)):
        if image1[i] != 0:
                frqi.c10ry(qc, 2 * image1[i], format(i, '010b'), img[0], anc2[0], [img[j] for j in range(1,len(img))])

qed.quantum_edge_detection(qc)
qc.measure(anc, c[0])
qc.measure(img, c[1:12])
print(qc.depth())
numOfShots = 8192
result = execute(qc, provider.get_backend('ibmq_qasm_simulator'), shots=numOfShots, backend_options={"fusion_enable":True}).result()
#circuit_drawer(qc).show()
#plot_histogram(result.get_counts(qc))

print(result.get_counts(qc))

# generated image
genimg = np.array([])

#### decode
for i in range(len(image1)):
        try:
                genimg = np.append(genimg,[np.sqrt(result.get_counts(qc)[format(i, '010b')+'10']/numOfShots)])
        except KeyError:
                genimg = np.append(genimg,[0.0])

# inverse nomalization
genimg *= 32.0 * 255.0

# convert type
genimg = genimg.astype('int')

# back to 2-dimentional data
genimg = genimg.reshape((32,32))

plt.imshow(genimg, cmap='gray', vmin=0, vmax=255)
plt.savefig('gen_'+str(imageNum1)+'.png')
plt.show()