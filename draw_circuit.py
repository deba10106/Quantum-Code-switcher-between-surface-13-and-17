import pennylane as qml
import matplotlib.pyplot as plt
import numpy as np
from surface_13_code import TOTAL_QUBITS as S13_QUBITS
from surface_17_code import TOTAL_QUBITS as S17_QUBITS

# Set up a device with enough wires for the larger code (Surface-17)
max_qubits = max(S13_QUBITS, S17_QUBITS)
dev = qml.device("default.qubit", wires=max_qubits)

@qml.qnode(dev)
def conversion_circuit():
    # Step 1: Encode in source code (surface13)
    # Prepare logical |0⟩ state in Surface-13 code
    # Apply X-type stabilizers
    for stab_data in [[0, 3, 6], [2, 5, 8]]:  # S1 and S4
        qml.Hadamard(wires=stab_data[0])
        for i in range(1, len(stab_data)):
            qml.CNOT(wires=[stab_data[0], stab_data[i]])
        qml.Hadamard(wires=stab_data[0])
    # Step 2: Decode from Surface-13 (simplified)
    # Step 3: Encode into Surface-17
    for q in range(1, 9):
        qml.CNOT(wires=[0, q])
    for stab_data in [[0, 1, 3, 4], [1, 2], [4, 5, 7, 8], [6, 7]]:
        qml.Hadamard(wires=stab_data[0])
        for i in range(1, len(stab_data)):
            qml.CNOT(wires=[stab_data[0], stab_data[i]])
        qml.Hadamard(wires=stab_data[0])
    for stab_data in [[0, 3], [1, 2, 4, 5], [3, 4, 6, 7], [5, 8]]:
        for i in range(1, len(stab_data)):
            qml.CZ(wires=[stab_data[0], stab_data[i]])
    # Only draw the circuit, don't return any measurement
    return qml.state()

# Draw and save the circuit as a PNG
fig, ax = qml.draw_mpl(conversion_circuit)()

# Add title, description, and labels
fig.suptitle("Quantum Code Switcher Circuit", y=0.98, fontsize=16)
plt.title("Surface-13 to Surface-17 Conversion Example", fontsize=12)
plt.xlabel("Circuit Depth (Gate Sequence)")
plt.ylabel("Qubit Index (0-8: Data Qubits)")
plt.figtext(
    0.5, 0.01,
    "This circuit includes the encoding (state preparation) portions of both Surface-13 and Surface-17 QEC codes, as well as the switching logic. "
    "It does NOT depict full QEC cycles (syndrome measurement/correction).",
    ha="center", fontsize=11, bbox={"facecolor":"white", "alpha":0.8, "pad":5}
)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig("code_switcher_circuit.png")
plt.close(fig)

print("Quantum code switcher circuit saved as code_switcher_circuit.png with labels and description.")
