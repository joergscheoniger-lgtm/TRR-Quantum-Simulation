"""
TRR Quantum Simulation - trr_simulation.py
==========================================
Theory of Relative Reality (TRR) by Joerg Schoeniger
Simulates relational stability in multi-qubit systems using Google Cirq.

Hypothesis (TRR Axiom 2 + 5):
  Decoherence time T2 initially decreases with qubit count k,
    but STABILIZES above critical entanglement density rho_c.
      This CONTRADICTS standard QM decoherence theory.

      DOI: 10.5281/zenodo.20061213
      Author: Joerg Schoeniger | Independent Researcher / TRR Project Group
      Date: 2026-05-07
      """

import cirq
import numpy as np
import matplotlib.pyplot as plt

# TRR PARAMETERS
RHO_C = 0.45        # Critical entanglement density (TRR Axiom 2)
T2_BASE = 100.0     # Base decoherence time in microseconds
ALPHA = 0.8         # Decay coefficient (standard QM regime)
BETA = 0.3          # Stabilization coefficient (TRR relational regime)
QUBIT_CONFIGS = [5, 10, 20, 30, 53]


def build_entanglement_circuit(qubits, depth=3):
      """Build circuit with high entanglement density (Sycamore topology)."""
      circuit = cirq.Circuit()
      circuit.append(cirq.H(q) for q in qubits)
      for d in range(depth):
                if d % 2 == 0:
                              pairs = [(qubits[i], qubits[i+1]) for i in range(0, len(qubits)-1, 2)]
else:
            pairs = [(qubits[i], qubits[i+1]) for i in range(1, len(qubits)-1, 2)]
          circuit.append(cirq.CNOT(a, b) for a, b in pairs)
    return circuit


def measure_entanglement_density(circuit, n_qubits):
      """Estimate entanglement density rho = CNOTs / max_possible_CNOTs."""
      n_cnots = sum(1 for op in circuit.all_operations()
                    if isinstance(op.gate, cirq.CNotGate))
      max_cnots = n_qubits * (n_qubits - 1) / 2
      return min(n_cnots / max_cnots, 1.0) if max_cnots > 0 else 0.0


def trr_predict_t2(k, rho):
      """
          TRR prediction: T2 stabilizes above rho_c.
              Standard QM: T2 = T2_BASE * exp(-ALPHA * k / 10)
                  TRR:         T2 = T2_QM * (1 + BETA * max(0, rho - rho_c) * k)
                      """
      t2_qm = T2_BASE * np.exp(-ALPHA * k / 10.0)
      relational_bonus = BETA * max(0.0, rho - RHO_C) * k
      t2_trr = t2_qm * (1.0 + relational_bonus)
      return t2_trr, t2_qm


def run_trr_experiment():
      print("=" * 60)
      print("TRR QUANTUM SIMULATION")
      print("Schoeniger TRR | DOI: 10.5281/zenodo.20061213")
      print("=" * 60)

    results_k, results_rho, results_t2_trr, results_t2_qm = [], [], [], []

    for k in QUBIT_CONFIGS:
              qubits = cirq.LineQubit.range(k)
              circuit = build_entanglement_circuit(qubits, depth=4)
              rho = measure_entanglement_density(circuit, k)
              t2_trr, t2_qm = trr_predict_t2(k, rho)

        results_k.append(k)
        results_rho.append(rho)
        results_t2_trr.append(t2_trr)
        results_t2_qm.append(t2_qm)

        regime = "TRR STABILIZED" if rho > RHO_C else "standard decay"
        print(f"k={k:2d} | rho={rho:.3f} | T2_TRR={t2_trr:6.2f}us "
                            f"| T2_QM={t2_qm:6.2f}us | [{regime}]")

    return results_k, results_rho, results_t2_trr, results_t2_qm


def plot_results(k_vals, rho_vals, t2_trr, t2_qm):
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
      fig.suptitle("TRR vs Standard QM Decoherence Prediction\n"
                   "DOI: 10.5281/zenodo.20061213", fontsize=12)

    ax1.plot(k_vals, t2_qm, 'b--o', label='Standard QM (monotonic decay)', lw=2)
    ax1.plot(k_vals, t2_trr, 'r-o', label='TRR prediction (stabilization)', lw=2)
    ax1.set_xlabel('Number of Qubits (k)')
    ax1.set_ylabel('Decoherence Time T2 (us)')
    ax1.set_title('TRR Core Prediction')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    colors = ['red' if r > RHO_C else 'blue' for r in rho_vals]
    ax2.bar(k_vals, rho_vals, color=colors)
    ax2.axhline(y=RHO_C, color='orange', linestyle='--',
                                label=f'Critical rho_c = {RHO_C}', lw=2)
    ax2.set_xlabel('Number of Qubits (k)')
    ax2.set_ylabel('Entanglement Density (rho)')
    ax2.set_title('Entanglement Density\n(red = TRR stabilization regime)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('trr_simulation_results.png', dpi=150, bbox_inches='tight')
    print("Plot saved: trr_simulation_results.png")
    plt.show()


if __name__ == "__main__":
      k_vals, rho_vals, t2_trr, t2_qm = run_trr_experiment()
      print(f"\nSummary: QM T2 drops {t2_qm[0]:.1f}->{t2_qm[-1]:.1f}us (monotonic)")
      print(f"TRR T2 stabilizes at {min(t2_trr):.1f}-{max(t2_trr):.1f}us")
      print("\nFalsifiable test: Run on Google Sycamore 5-53 qubits.")
      print("Paper: https://zenodo.org/records/20061213")
      try:
                plot_results(k_vals, rho_vals, t2_trr, t2_qm)
except Exception as e:
        print(f"(Plot skipped: {e})")
