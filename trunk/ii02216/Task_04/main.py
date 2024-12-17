from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(7, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[2])
circuit.h(qreg_q[1])
circuit.h(qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[3])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.ccx(qreg_q[2], qreg_q[3], qreg_q[5])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[4])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.measure(qreg_q[3], creg_c[0])
circuit.ccx(qreg_q[4], qreg_q[5], qreg_q[6])
circuit.measure(qreg_q[6], creg_c[1])
circuit.draw(output='mpl')