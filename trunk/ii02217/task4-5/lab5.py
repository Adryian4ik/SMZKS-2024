from qiskit import QuantumCircuit
from qiskit_aer import Aer

import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt



state = '1110101'
n = 7

def oracle(circuit):
    for i, bit in enumerate(state):
        if bit == '0':
            circuit.x(i)

    circuit.h(n-1)
    circuit.mcx(list(range(n-1)), n-1)
    circuit.h(n-1)

    for i, bit in enumerate(state):
        if bit == '0':
            circuit.x(i)

    circuit.barrier()

def diffuser(circuit):
    circuit.h(range(n))
    circuit.x(range(n))
    circuit.h(n-1)
    circuit.mcx(list(range(n-1)), n-1)
    circuit.h(n-1)
    circuit.x(range(n))
    circuit.h(range(n))

    circuit.barrier()
    circuit.barrier()

def main(debug = False):
    simulator = Aer.get_backend('qasm_simulator')

    correct = []
    iterations = range(15)

    for iteration in iterations:
        qc = QuantumCircuit(n)

        qc.h(range(n))
        qc.barrier()
        qc.barrier()


        for _ in range(iteration):
            oracle(qc)
            diffuser(qc)


        qc.measure_all()
        result = simulator.run(qc).result()

        counts = result.get_counts()
        correct.append(counts.get(state[::-1], 0))
        if debug and 1== iteration:
            qc.draw('mpl')

            plt.show()

    plt.bar(iterations, correct)
    plt.show()


if __name__ == "__main__":
    main(True)