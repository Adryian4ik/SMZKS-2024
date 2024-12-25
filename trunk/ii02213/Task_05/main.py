from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from numpy import pi
from qiskit import QuantumCircuit
from qiskit_aer import Aer

import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

state = "0110101"
n = len(state)


def oracle(qc):
    qc.x(0)
    qc.x(3)
    qc.x(5)

    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n - 1)

    qc.x(0)
    qc.x(3)
    qc.x(5)
def diffusion(qc):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))


def main(debug = False):
    simulator = Aer.get_backend('qasm_simulator')

    correct = []
    iterations = range(15)

    for iteration in iterations:
        qc = QuantumCircuit(n)

        qc.h(range(n))



        for _ in range(iteration):
            oracle(qc)
            diffusion(qc)


        qc.measure_all()
        result = simulator.run(qc, shots=1024).result()

        counts = result.get_counts()
        correct.append(counts.get(state[::-1], 0))
        if debug and 1== iteration:
            qc.draw('mpl')

            plt.show()

    plt.bar(iterations, correct)
    plt.show()



if __name__ == "__main__":
    main(True)
