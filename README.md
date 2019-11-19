# Q-CAN (quantum-cities-at-night)
Quantum image processing for mapping the Earth at night.

# Project Background and Motivation
Cities at Night (www.citiesatnight.org) is an ongoing project by Alejandro Sanchez de Miguel (U. of Exeter) et al. focused on the creation of a hight resolution map of the Earth at night, using color photographs taken by astronauts onboard the ISS. 

NASA has a database with almost 1 million cluttered, unlabeled pictures taken from space over the years. In order to create a high resolution world map, these photographs must be matched with their precise location in the globe's surface, a task for which the use of classical machine learning algorithms has been deemed ineffective. The current alternative has been to use citizen science and benefit from the manual matchings carried out by thousands of volunteers, but .... could this approach be improved?

We think the answer is YES!, and for this hackathon we have decided to explore the benefits quantum computing can bring to this and many other computer vision based science intiatives, using current public available tools such as IBM Qiskit.

# Goals
The aim of the project is to develop a python-based module to perform image matching using quantum computing tools (Qiskit). As an inital approach, the image matching process has been divided into the following tasks:

1. Classical image preparation 
2. Quantum encoding
3. Quantum edge detection
4. Quantum matching

These tasks will be studied in order to fullfill the **main goal of the project: a minimally viable product (MVP) where 3 classical images (1 reference and 2 proposals) are inputted, encoded, compared and matched**; such as the proposal that best fits the reference is matched with it.  

# Proposed Implementation

- **Step 1: Image Preparation**

This step involves preparing the inital images to adapt our problem to the scope of the hackathon by:
    - changing from RGB to grayscale format
    - reducing the resolution to 32 x 32 pixels (this will later mean using 24 qubits in our coputation, with the current limit of the qasm simulator being 32 quibts)
    - discarding particularly challenging pictures: those that are cropped, taken from a strange perspective.... 


- **Step 2: Quantum Encoding**

- **Step 3: Image Preparation**

- **Step 4: Image Preparation**
# 
