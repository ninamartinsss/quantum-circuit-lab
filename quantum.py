"""Small ideal state-vector simulator. Qubit 0 is the least significant bit."""
from dataclasses import dataclass
import numpy as np

GATES = {
    'H': np.array([[1, 1], [1, -1]], complex) / np.sqrt(2),
    'X': np.array([[0, 1], [1, 0]], complex),
    'Y': np.array([[0, -1j], [1j, 0]], complex),
    'Z': np.diag([1, -1]).astype(complex),
    'S': np.diag([1, 1j]),
    'T': np.diag([1, np.exp(1j * np.pi / 4)]),
}

@dataclass(frozen=True)
class Operation:
    gate: str
    target: int
    control: int | None = None


def simulate(n: int, operations: list[Operation]) -> np.ndarray:
    if not isinstance(n, int) or not 1 <= n <= 8:
        raise ValueError('Choose 1–8 qubits.')
    state = np.zeros(2**n, dtype=complex)
    state[0] = 1
    for op in operations:
        if not 0 <= op.target < n:
            raise ValueError('Invalid target qubit.')
        mask = 1 << op.target
        if op.gate == 'CX':
            if op.control is None or not 0 <= op.control < n or op.control == op.target:
                raise ValueError('CX requires a distinct valid control.')
            for i in range(len(state)):
                if i & (1 << op.control) and not i & mask:
                    j = i | mask
                    state[i], state[j] = state[j], state[i]
        elif op.gate in GATES and op.control is None:
            for i in range(len(state)):
                if not i & mask:
                    j = i | mask
                    state[[i, j]] = GATES[op.gate] @ state[[i, j]]
        else:
            raise ValueError('Unsupported gate or unexpected control.')
    return state


def probabilities(state: np.ndarray) -> np.ndarray:
    p = np.abs(state)**2
    return p / p.sum()


def sample(state: np.ndarray, shots: int, seed: int | None = None) -> np.ndarray:
    if not isinstance(shots, int) or not 1 <= shots <= 100_000:
        raise ValueError('Shots must be between 1 and 100,000.')
    return np.random.default_rng(seed).multinomial(shots, probabilities(state))
