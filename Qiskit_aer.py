# === Fully updated optional Qiskit RNG cell (modern syntax) ===
!pip install qiskit qiskit-aer -q

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Simple 4-qubit circuit to generate quantum random bits
# (you can use these to seed Alice's modulation in a hybrid simulation)
qc = QuantumCircuit(4, 4)
qc.h(range(4))           # superposition → true randomness
qc.measure(range(4), range(4))

backend = AerSimulator()           # recommended in Qiskit 1.x
job = backend.run(qc, shots=1024)  # ← use backend.run() instead of execute()
result = job.result()
counts = result.get_counts()

print("Quantum random bitstrings (sample):", list(counts.keys())[:8])
print("Total shots:", sum(counts.values()))
