# Q-C@N (quantum-cities-at-night)
Quantum image processing for mapping the Earth at night.

# Project Background and Motivation
Cities at Night (www.citiesatnight.org) is an ongoing project by Alejandro Sanchez de Miguel (U. of Exeter) et al. focused on the creation of a hight resolution map of the Earth at night, using color photographs taken by astronauts onboard the ISS. 

NASA has a database with almost 1 million cluttered, unlabeled pictures taken from space over the years. In order to create a high resolution world map, these photographs must be matched with their precise location in the globe's surface, a task for which the use of classical machine learning algorithms has been deemed ineffective. The current alternative has been to use citizen science and benefit from the manual matchings carried out by thousands of volunteers, but .... could this approach be improved?

We think the answer is YES!, and for this hackathon we have decided to explore the benefits quantum computing can bring to this and many other computer vision based science intiatives, using current public available tools such as IBM Qiskit.

# Goals
The aim of the project is to develop a Python-based module to perform image matching using quantum computing tools (Qiskit). As an inital approach, the image matching process has been divided into the following tasks:

1. Classical image preparation 
2. Quantum encoding
3. Quantum edge detection
4. Quantum image matching

These tasks will be studied in order to fullfill the **main goal of the project: a minimally viable product (MVP) where 3 classical images (1 reference and 2 proposals) are inputted, encoded, compared and matched**; such as the proposal that best fits the reference is matched with it.  

# Proposed Implementation
- **Step 1: Image Preparation**
This step involves preparing the inital images to adapt our problem to the scope of the hackathon by:
   - changing from RGB to grayscale format
   - cropping the image to a square
   - reducing the resolution to 32 x 32 pixels (this will later mean using 24 qubits in our computation, with the current limit of the qasm simulator being 32 quibts)
   - discarding particularly challenging pictures: those that are cropped, taken from a strange perspective.... 

This is step can be performed using multiple Python classical image processing libraries such as PIL, OpenCV, etc.

- **Step 2: Quantum Encoding**
The quantum encoding or Quantum Image Representation (QImR) step involves the transformation of the data from a classical to a quantum image representation model [2]. The chosen quantum representation model is key to determine the types of processing tasks and how well they can be performed. After studying different proposals such as NEQR [3], in order to develop our MVP, we have selected to apply Flexible Representation of Quantum Images (FRQI) [4]. This allows us to encode an image of size *m = n x n* (pixels) into *log2(m)* qubits. One of the drawbacks of this representation is the requirement of *m* gates to perform the encoding of such an image.

- **Step 3: Image Preparation**

- **Step 4: Quantum image matching**


# References
[1] https://arxiv.org/pdf/1801.01465.pdf
[2] 
[3]
[4] https://www.jstage.jst.go.jp/article/fss/25/0/25_0_185/_pdf

