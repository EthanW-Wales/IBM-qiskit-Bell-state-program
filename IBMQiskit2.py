#==========================Imports==========================

# Core Qiskit imports
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from matplotlib import pyplot as plt

# IBM Runtime specific imports
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService

import sys

import qiskit
import qiskit_aer
import qiskit_ibm_runtime

#======================Version Controle==========================

print("Python:", sys.version.split()[0])
print("qiskit:", qiskit.__version__)
print("qiskit-aer:", qiskit_aer.__version__)
print("qiskit-ibm-runtime:", qiskit_ibm_runtime.__version__)

#=======================Bell State Circuit========================

def create_bell_state_circuit1():
    circuit = QuantumCircuit(2)

    circuit.h(0)  # Apply Hadamard gate to qubit 0
    circuit.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target

    circuit.measure_all()  # Measure both qubits
    # creates a classical register named "meas"

    return circuit

def create_bell_state_circuit2():
    circuit = QuantumCircuit(2)

    circuit.h(0)  # Apply Hadamard gate to qubit 0
    circuit.x(1)  # Apply X gate to qubit 1
    circuit.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target

    circuit.measure_all()  # Measure both qubits

    return circuit

#========================Visualize Circuit========================

#bell = create_bell_state_circuit1()
#bell2 = create_bell_state_circuit2()
#bell.draw("mpl")
#plt.show()
#bell2.draw("mpl")
#plt.show()

#=======================Define Process to interact with IBM quantum computer========================

def run_circuit_and_get_counts(circuit, backend, shots=1000):
    """
    Runs a quantum circuit on a specified backend and returns the measurement counts.

    Args:
        circuit (QuantumCircuit): The quantum circuit to run.
        backend: The Qiskit backend (real device or simulator).
        shots (int): The number of shots to run the circuit.

    Returns:
        dict: A dictionary of measurement counts.
    """
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)

    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()

    return result[0].data.meas.get_counts()

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="insert token here",
    overwrite=True,
    set_as_default=True,
)
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# Load saved credentials
service = QiskitRuntimeService()

# Use the least busy backend, or uncomment the loading of a specific backend like "ibm_fez".
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
# backend = service.backend("ibm_fez")
print(backend.name)

#=======================Run Circuit and Plot Histogram========================

print("1 for |phi^+> state, 2 for |psi^+1> state")
statechoice = input("Enter your choice: ")
if statechoice == "1":
    print("You have chosen the |phi^+> state.")
    bell = create_bell_state_circuit1()
    #bell.draw("mpl")
    #plt.show()
    print("1 for real quantum computer, 2 for simulator")
    
    input_choice = input("Enter your choice: ")
    
    if input_choice == "1":
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
        print("Running on real quantum computer:", backend.name)   
        counts = run_circuit_and_get_counts(bell, backend, shots=1000)
        plot_histogram(counts)
        
    if input_choice == "2":
        backend = AerSimulator()
        print("Running on simulator:", backend.name)
        counts = run_circuit_and_get_counts(bell, backend, shots=1000)
        plot_histogram(counts)
        plt.show()

if statechoice == "2":
    print ("You have chosen the |psi^+> state.")
    bell = create_bell_state_circuit2()
    #bell.draw("mpl")
    #plt.show()

    print("1 for real quantum computer, 2 for simulator")
    relsimchoice = input("Enter your choice: ")
    if relsimchoice == "1":
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
        print("Running on real quantum computer:", backend.name)   
        counts = run_circuit_and_get_counts(bell, backend, shots=1000)
        plot_histogram(counts)

    if relsimchoice == "2":
        backend = AerSimulator()
        print("Running on simulator:", backend.name)
        counts = run_circuit_and_get_counts(bell, backend, shots=1000)
        plot_histogram(counts)
        plt.show()
    


