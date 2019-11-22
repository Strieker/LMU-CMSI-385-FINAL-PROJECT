LAMBDA = ""

class State:
    value = None
    transitions = []
    accepted = False
    def __init__(self, V, T, A):
        self.value = V
        self.transitions = T
        self.accepted = A

class NPDAProblem:
    def __init__(self, S, M):
        self.to_check = S
        self.machine = M

# HOW HANDLE LAMBDAS COMES LATER MAKE SURE THAT IT'S IN THE ALPHABET IT SHOULD BE FINE BUT NEED 
# TO DOUBLE CHECK THAT 
class NPDA:
    states = []
    alphabet = []
    transition_function = None
    start_state = ""
    accept_states = []
    def __init__(self, Q, E, d, q0, F):
        self.states = Q
        self.alphabet = E
        self.transition_function = d
        self.start_state = q0
        self.accept_states = F
        self.convert_values_of_q_to_states()

    def convert_values_of_q_to_states(self):
        for i in range(len(self.states)):
            state_value = self.states[i]
            if state_value in self.accept_states:
                self.states[i] = State(state_value, self.add_transitions_between_states(state_value), True)
            else:
                self.states[i] = State(state_value, self.add_transitions_between_states(state_value), False)

    def add_transitions_between_states(self, state_value):
        transitions = []
        for transition_term in self.alphabet:
            states_to_transition_to = self.transition_function(state_value, transition_term) 
            if(states_to_transition_to != None):
                for state_to_transition_to in states_to_transition_to:
                    transitions.append((transition_term, state_to_transition_to))
        return transitions

# TEST 1 
def d1(state_value, transition):
    switch = {
        ("A", 0): ["B"],
        ("A", 1): ["C"],
        ("B", 0): ["B"],
        ("B", 1): ["D"],
        ("C", 0): ["B"],
        ("C", 1): ["C"],
        ("D", 0): ["B"],
        ("D", 1): ["E"],
        ("E", 0): ["B"],
        ("E", 1): ["C"],
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n1 = NPDA(["A", "B", "C", "D", "E"], [0, 1], d1, "A", ["E"])
# map(lambda state: (state.value, state.transitions, state.accepted), n1.Q)
assert([('A', [(0, 'B'), (1, 'C')], False), ('B', [(0, 'B'), (1, 'D')], False), ('C', [(0, 'B'), (1, 'C')], False), ('D', [(0, 'B'), (1, 'E')], False), ('E', [(0, 'B'), (1, 'C')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n1.states)])

#TEST 2
def d2(state_value, transition):
    switch = {
        ("A", 0): ["B"],
        ("B", LAMBDA): ["F"],
        ("C", 1): ["D"],
        ("D", LAMBDA): ["F"],
        ("E", LAMBDA): ["C", "A"],
        ("F", LAMBDA): ["E"],
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n2 = NPDA(["A", "B", "C", "D", "E", "F"], [0, 1, LAMBDA], d2, "F", ["B", "D", "F", "E"])
assert([('A', [(0, 'B')], False), ('B', [('', 'F')], True), ('C', [(1, 'D')], False), ('D', [('', 'F')], True), ('E', [('', 'C'), ('', 'A')], True), ('F', [('', 'E')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n2.states)])

