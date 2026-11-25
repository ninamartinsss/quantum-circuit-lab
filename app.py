import streamlit as st
import numpy as np
from quantum import GATES, Operation, simulate, probabilities, sample

st.set_page_config(page_title='QUANTUM | Circuit Lab', page_icon='⚛', layout='wide')
st.title('QUANTUM — Circuit Lab')
st.caption('An educational, ideal state-vector simulator · NumPy + Streamlit')
if 'ops' not in st.session_state:
    st.session_state.ops = []
if 'n' not in st.session_state:
    st.session_state.n = 2
with st.sidebar:
    st.header('Circuit controls')
    if st.button('Bell state'):
        st.session_state.n = 2
        st.session_state.ops = [Operation('H', 0), Operation('CX', 1, 0)]
    if st.button('GHZ state'):
        st.session_state.n = 3
        st.session_state.ops = [Operation('H', 0), Operation('CX', 1, 0), Operation('CX', 2, 0)]
    n = st.slider('Qubits', 1, 8, key='n', on_change=lambda: st.session_state.update(ops=[]))
    gate = st.selectbox('Gate', list(GATES) + (['CX'] if n > 1 else []))
    target = st.selectbox('Target', list(range(n)))
    control = st.selectbox('Control', [i for i in range(n) if i != target]) if gate == 'CX' else None
    if st.button('Add gate', disabled=len(st.session_state.ops) >= 100):
        st.session_state.ops.append(Operation(gate, target, control))
    if st.button('Undo', disabled=not st.session_state.ops):
        st.session_state.ops.pop()
    if st.button('Clear'):
        st.session_state.ops = []
    shots = st.slider('Measurement shots', 100, 10000, 1000, step=100)
    seed = st.number_input('Random seed', min_value=0, max_value=2**32-1, value=42)
ops = st.session_state.ops
state = simulate(n, ops)
p = probabilities(state)
counts = sample(state, shots, int(seed))
labels = [format(i, f'0{n}b') for i in range(2**n)]
a,b,c = st.columns(3)
a.metric('Qubits', n); b.metric('Gates', len(ops)); c.metric('State norm', f'{np.linalg.norm(state):.6f}')
st.subheader('Circuit')
# Text diagram uses fixed-width columns, one operation per column.
lines = []
for q in range(n):
    cells = ['  ●  ' if op.control == q else f' {op.gate:^3} ' if op.target == q else '─────' for op in ops]
    lines.append(f'q{q}: |0> ─' + '─'.join(cells))
st.code('\n'.join(lines), language=None)
st.caption('Bit strings are ordered q[n−1] … q[0]. ● marks the control of CX.')
left,right = st.columns(2)
with left:
    st.subheader('Exact probabilities')
    st.bar_chart({'basis': labels, 'probability': p}, x='basis', y='probability')
with right:
    st.subheader('Sampled measurements')
    st.bar_chart({'basis': labels, 'counts': counts}, x='basis', y='counts')
with st.expander('Complex amplitudes'):
    st.dataframe({'basis': labels, 'real': state.real, 'imaginary': state.imag, 'probability': p, 'counts': counts})
st.info('Ideal pure states only: no hardware, noise, mid-circuit measurements or real quantum speedup. Sampling does not modify the displayed state.')
