LAMBDA = ""
class State:
    value = None
    transitions = []
    accepted = False
    def __init__(self, val, transit, accept):
        self.value = val
        self.transitions = transit
        self.accepted = accept

class NPDAProblem:
    def __init__(self, to_check, machine):
        self.to_check = to_check
        self.machine = machine

# HOW HANDLE LAMBDAS COMES LATER MAKE SURE THAT IT'S IN THE ALPHABET IT SHOULD BE FINE BUT NEED 
# TO DOUBLE CHECK THAT 
class NPDA:
    Q = []
    E = []
    d = None
    q0 = ""
    F = []
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.Q = states
        self.E = alphabet
        self.d = transition_function
        self.q0 = start_state
        self.F = accept_states
        self.convert_values_of_q_to_states()

    def convert_values_of_q_to_states(self):
        for i in range(len(self.Q)):
            state_value = self.Q[i]
            if state_value in self.F:
                self.Q[i] = State(state_value, self.add_transitions_between_states(state_value), True)
            else:
                self.Q[i] = State(state_value, self.add_transitions_between_states(state_value), False)

    def add_transitions_between_states(self, state_value):
        transitions = []
        for transition_term in self.E:
            if(self.d(state_value, transition_term) != None):
                for state_to_transition_to in self.d(state_value, transition_term):
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
assert([('A', [(0, 'B'), (1, 'C')], False), ('B', [(0, 'B'), (1, 'D')], False), ('C', [(0, 'B'), (1, 'C')], False), ('D', [(0, 'B'), (1, 'E')], False), ('E', [(0, 'B'), (1, 'C')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n1.Q)])

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
assert([('A', [(0, 'B')], False), ('B', [('', 'F')], True), ('C', [(1, 'D')], False), ('D', [('', 'F')], True), ('E', [('', 'C'), ('', 'A')], True), ('F', [('', 'E')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n2.Q)])
