import numpy as np

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Reset
from qiskit.circuit.library.standard_gates import (IGate, U1Gate, U2Gate, U3Gate, XGate,
                                                   YGate, ZGate, HGate, SGate, SdgGate, TGate,
                                                   TdgGate, RXGate, RYGate, RZGate, CXGate,
                                                   CYGate, CZGate, CHGate, CRZGate, CU1Gate,
                                                   CU3Gate, SwapGate, RZZGate,
                                                   CCXGate, CSwapGate)
from qiskit.circuit.exceptions import CircuitError
import random 
# from qiskit.util import deprecate_arguments

'''
This is the sourcecode for the random_qubit function from: 
https://github.com/Qiskit/qiskit/blob/7bc7f08bf64aa686694467e8f8be551e0b740213/qiskit/circuit/random/utils.py#L30

I want to only allow operations (per gate) that act on two!! qubits. So if there has been an operation done on two qubits, I don't want another one. 
'''


def random_circuit(num_qubits, depth, max_operands=3, measure=False,
                   conditional=False, reset=False, seed=None):
    
    if max_operands < 1 or max_operands > 3:
        raise CircuitError("max_operands must be between 1 and 3")

    one_q_ops = [IGate, U1Gate, U2Gate, U3Gate, XGate, YGate, ZGate,
                 HGate, SGate, SdgGate, TGate, TdgGate, RXGate, RYGate, RZGate]
    one_param = [U1Gate, RXGate, RYGate, RZGate, RZZGate, CU1Gate, CRZGate]
    two_param = [U2Gate]
    three_param = [U3Gate, CU3Gate]
    two_q_ops = [CXGate , CYGate, CZGate, CHGate, CRZGate, CU1Gate, CU3Gate, SwapGate, RZZGate]
    three_q_ops = [CCXGate, CSwapGate]

    qr = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(num_qubits)

    if measure or conditional:
        cr = ClassicalRegister(num_qubits, 'c')
        qc.add_register(cr)

    if reset:
        one_q_ops += [Reset]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # apply arbitrary random operations at every depth
    for _ in range(depth):
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(num_qubits))

        # only allow one operation on two qubits in total: 
        counterTwoOperands = 0

        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands)) + 1

            # if counterTwoOperands < 1: 
            #     while num_operands == 2: 
            #         num_operands = rng.choice(range(max_possible_operands)) + 1

            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                if counterTwoOperands < 1: 
                    operation = rng.choice(two_q_ops)
                    counterTwoOperands += 1
                else: 
                    continue
            elif num_operands == 3:
                operation = rng.choice(three_q_ops)
            if operation in one_param:
                num_angles = 1
            elif operation in two_param:
                num_angles = 2
            elif operation in three_param:
                num_angles = 3
            else:
                num_angles = 0
            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]
            op = operation(*angles)

            # with some low probability, condition on classical bit values
            if conditional and rng.choice(range(10)) == 0:
                value = rng.integers(0, np.power(2, num_qubits))
                op.condition = (cr, value)

            qc.append(op, register_operands)

    if measure:
        qc.measure(qr, cr)

    return qc












'''
now, one function that only creates one two qubit opertion per gate 
'''

def randomCircuitTwoQubits(num_qubits, depth, max_operands=3, measure=False,
                   conditional=False, reset=False, seed=None):
    
    if max_operands < 1 or max_operands > 3:
        raise CircuitError("max_operands must be between 1 and 3")

    one_q_ops = [IGate, U1Gate, U2Gate, U3Gate, XGate, YGate, ZGate,
                 HGate, SGate, SdgGate, TGate, TdgGate, RXGate, RYGate, RZGate]
    one_param = [U1Gate, RXGate, RYGate, RZGate, RZZGate, CU1Gate, CRZGate]
    two_param = [U2Gate]
    three_param = [U3Gate, CU3Gate]
    two_q_ops = [CXGate , CYGate, CZGate, CHGate, CRZGate, CU1Gate, CU3Gate, SwapGate, RZZGate]

    qr = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(num_qubits)

    if measure or conditional:
        cr = ClassicalRegister(num_qubits, 'c')
        qc.add_register(cr)

    if reset:
        one_q_ops += [Reset]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # was inside the _ for loop 
    remaining_qubits = list(range(num_qubits))

    num_operands = 2 

    rng.shuffle(remaining_qubits)
    operands = remaining_qubits[:num_operands]



    # apply arbitrary random operations at every depth
    for _ in range(depth):
        # choose either 1, 2, or 3 qubits for the operation

        # now only one qubit operations 
        operandsTwo = operands
        for j in range(2): 

            operands = [operandsTwo[j]]

            operation = rng.choice(one_q_ops)

            if operation in one_param:
                num_angles = 1
            elif operation in two_param:
                num_angles = 2
            elif operation in three_param:
                num_angles = 3
            else:
                num_angles = 0


            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]
            op = operation(*angles)

            # do the one qubit operations only with a 0.5 percent probability
            randomNumber = random.random()

            if randomNumber <= 0.5:
                qc.append(op, register_operands)



        # REVERSED ORDER OF TWO AND ONE OPERATION GATES 
        operands = operandsTwo

        # remaining_qubits = [q for q in remaining_qubits if q not in operands]
        # if num_operands == 2:

        # number of operands is two! 
        operation = rng.choice(two_q_ops)

        if operation in one_param:
            num_angles = 1
        elif operation in two_param:
            num_angles = 2
        elif operation in three_param:
            num_angles = 3
        else:
            num_angles = 0
        angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
        register_operands = [qr[i] for i in operands]

        op = operation(*angles)

        # with some low probability, condition on classical bit values
        if conditional and rng.choice(range(10)) == 0:
            value = rng.integers(0, np.power(2, num_qubits))
            op.condition = (cr, value)

        qc.append(op, register_operands)




    if measure:
        qc.measure(qr, cr)



    return qc, operands











'''
New Try 
'''


def randomCircuitNew(num_qubits, depth, max_operands=3, measure=False,
                   conditional=False, reset=False, seed=None):
    
    if max_operands < 1 or max_operands > 3:
        raise CircuitError("max_operands must be between 1 and 3")

    one_q_ops = [IGate, U1Gate, U2Gate, U3Gate, XGate, YGate, ZGate,
                 HGate, SGate, SdgGate, TGate, TdgGate, RXGate, RYGate, RZGate]
    one_param = [U1Gate, RXGate, RYGate, RZGate, RZZGate, CU1Gate, CRZGate]
    two_param = [U2Gate]
    three_param = [U3Gate, CU3Gate]
    two_q_ops = [CXGate , CYGate, CZGate, CHGate, CRZGate, CU1Gate, CU3Gate, SwapGate, RZZGate]
    three_q_ops = [CCXGate, CSwapGate]

    qr = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(num_qubits)

    if measure or conditional:
        cr = ClassicalRegister(num_qubits, 'c')
        qc.add_register(cr)

    if reset:
        one_q_ops += [Reset]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # apply arbitrary random operations at every depth
    for _ in range(depth):
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(num_qubits))

        # only allow one operation on two qubits in total: 
        counterTwoOperands = 0

        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands)) + 1

            # if counterTwoOperands < 1: 
            #     while num_operands == 2: 
            #         num_operands = rng.choice(range(max_possible_operands)) + 1

            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                if counterTwoOperands < 1: 
                    operation = rng.choice(two_q_ops)
                    counterTwoOperands += 1
                else: 
                    continue
            elif num_operands == 3:
                operation = rng.choice(three_q_ops)
            if operation in one_param:
                num_angles = 1
            elif operation in two_param:
                num_angles = 2
            elif operation in three_param:
                num_angles = 3
            else:
                num_angles = 0
            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]
            op = operation(*angles)

            # with some low probability, condition on classical bit values
            if conditional and rng.choice(range(10)) == 0:
                value = rng.integers(0, np.power(2, num_qubits))
                op.condition = (cr, value)

            qc.append(op, register_operands)

    if measure:
        qc.measure(qr, cr)

    return qc, operands





