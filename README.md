# QUANTUM — Circuit Lab

An educational quantum circuit simulator built with Python, NumPy and Streamlit. Explore superposition, phase, entanglement and measurement on an ideal state vector of up to eight qubits.

## Quick start

Requires Python 3.10+ (3.12 recommended).

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. Select a gate and target, add it to the circuit, and compare exact probabilities with seeded measurement counts. Bell and GHZ presets provide examples; changing qubit count clears the circuit. The circuit lives in the current Streamlit session.

## Model and conventions

The initial state is |0...0>. Qubit 0 is the least significant bit. H, X, Y, Z, S and T apply 2×2 unitary matrices to amplitude pairs; CX swaps pairs when its control bit is set. Each gate takes O(2^n) time and the state requires O(2^n) memory. Born probabilities are squared amplitude magnitudes. Measurement counts use a seeded multinomial draw, without collapsing the displayed state.

Bell example: H on q0, CX from q0 to q1 yields (|00> + |11>)/sqrt(2), with equal probabilities for 00 and 11. GHZ extends this correlation to three qubits.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Docker

```bash
docker build -t quantum-circuit-lab .
docker run --rm -p 8501:8501 quantum-circuit-lab
```

## Architecture and limitations

`quantum.py` contains the independent numerical engine; `app.py` is the interactive presentation layer; `tests/` validates known states, normalization, input errors and reproducible sampling. GitHub Actions runs tests and syntax checks. This is a classical, ideal pure-state simulator, not a quantum hardware interface. No noise model, mid-circuit collapse, arbitrary rotations, or hardware execution. No credentials or external services are required.

## License

MIT.
