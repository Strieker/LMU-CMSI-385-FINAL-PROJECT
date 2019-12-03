LAMBDA = ""

class State:
    value = None
    transitions = []
    accepted = False
    def __init__(self, V, T, A):
        self.value = V
        self.transitions = T
        self.accepted = A

class NFAProblem:
    def __init__(self, S, M):
        self.to_check = S
        self.machine = M 

    def is_string_in_language(self, possible_accepted_string, current_state):
        # for each letter for each state if it has transitions for each letter then add it to the current states and check the 
        # check for lambda moves go through lambda moves 
        current_states_to_check_current_transitions_on = self.machine.initial_state_values
        graveyard = []
        while current_states_to_check_current_transitions_on != None:
            if len(possible_accepted_string) == 0:
                    return current_state.accepted
            else:
                filtered_transitions = [x for x in current_state.transitions if (possible_accepted_string[0] in x or LAMBDA in x)]
                print(filtered_transitions)
                filtered_states = [y for x in filtered_transitions for y in x if y == x[1]]
                print("----------------")
                print(filtered_states)
                if len(filtered_states) > 0:
                    for state in filtered_states:
                        print(possible_accepted_string)
                        print("///////////////////")
                        if state not in current_states_to_check_current_transitions_on and state not in graveyard:
                            current_states_to_check_current_transitions_on.append(state)
                state_to_pass = current_states_to_check_current_transitions_on.pop()   
                if len(current_states_to_check_current_transitions_on) != 0:
                    print("IM THE STATE")
                    print(state)
                    graveyard.append(state_to_pass)
                    current_state = self.find_state_in_machine(state_to_pass)
                print("\n")
            possible_accepted_string = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]

    def get_next_letter(self, possible_accepted_string, position_in_string):
        return - 1 if position_in_string + 1 == len(possible_accepted_string) else position_in_string + 1

    def find_state_in_machine(self, state_value):
        for state in self.machine.states:
            if state.value == state_value:
                return state

# RECONSIDER THE STUCTURES YOU USED FOR SOME OF THESE 
class NFA:
    initial_state_values = []
    states = []
    alphabet = []
    transition_function = None
    start_state = ""
    accept_states = []
    def __init__(self, Q, E, d, q0, F):
        self.initial_state_values = Q
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
        ("A", "0"): ["B"],
        ("A", "1"): ["C"],
        ("B", "0"): ["B"],
        ("B", "1"): ["D"],
        ("C", "0"): ["B"],
        ("C", "1"): ["C"],
        ("D", "0"): ["B"],
        ("D", "1"): ["E"],
        ("E", "0"): ["B"],
        ("E", "1"): ["C"],
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n1 = NFA(["A", "B", "C", "D", "E"], ["0", "1"], d1, "A", ["E"])
assert([('A', [("0", 'B'), ("1", 'C')], False), ('B', [("0", 'B'), ("1", 'D')], False), ('C', [("0", 'B'), ("1", 'C')], False), ('D', [("0", 'B'), ("1", 'E')], False), ('E', [("0", 'B'), ("1", 'C')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n1.states)])

#TEST 2
def d2(state_value, transition):
    switch = {
        ("A", "0"): ["B"],
        ("B", LAMBDA): ["F"],
        ("C", "1"): ["D"],
        ("D", LAMBDA): ["F"],
        ("E", LAMBDA): ["C", "A"],
        ("F", LAMBDA): ["E"],
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n2 = NFA(["A", "B", "C", "D", "E", "F"], ["0", "1", LAMBDA], d2, "F", ["B", "D", "F", "E"])
assert([('A', [("0", 'B')], False), ('B', [('', 'F')], True), ('C', [("1", 'D')], False), ('D', [('', 'F')], True), ('E', [('', 'C'), ('', 'A')], True), ('F', [('', 'E')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n2.states)])

#TEST 3
def d3(state_value, transition):
    switch = {
        ("AE", "0"): ["BF"],
        ("AE", "1"): ["DE"],
        ("BF", "0"): ["CE"],
        ("BF", "1"): ["CF"],
        ("CE", "0"): ["DF"],
        ("CE", "1"): ["DE"],
        ("CF", "0"): ["DE"],
        ("CF", "1"): ["DF"],
        ("DE", "0"): ["DF"],
        ("DE", "1"): ["DE"],
        ("DF", "0"): ["DE"],
        ("DF", "1"): ["DF"],
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n3 = NFA(["AE", "BF", "CE", "CF", "DE", "DF"], ["0", "1"], d3, "AE", ["DE", "AE", "CE", "CF"])
assert([('AE', [("0", 'BF'), ("1", 'DE')], True), ('BF', [("0", 'CE'), ("1", 'CF')], False), ('CE', [("0", 'DF'), ("1", 'DE')], True), ('CF', [("0", 'DE'), ("1", 'DF')], True), ('DE', [("0", 'DF'), ("1", 'DE')], True), ('DF', [("0", 'DE'), ("1", 'DF')], False)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n3.states)])

#TEST 4 WEIRD CASE TO LOOK FOR LATER WHERE CAN TAKE MULTIPLE PATHS 
# WITH THE SAME TRANSITION 
def d4(state_value, transition):
    switch = {
        ("A", LAMBDA): ["B", "F"],
        ("B", LAMBDA): ["C", "I"],
        ("C", "1"): ["D"],
        ("D", "0"): ["E"],
        ("E", LAMBDA): ["B", "I"],
        ("F", "0"): ["G"],
        ("G", "1"): ["H"],
        ("H", LAMBDA): ["I"],
        ("I", "0"): ["J"]
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n4 = NFA(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], ["0", "1", LAMBDA], d4, "A", ["B", "E", "H", "I", "J"])
assert([('A', [('', 'B'), ('', 'F')], False), ('B', [('', 'C'), ('', 'I')], True), ('C', [("1", 'D')], False), ('D', [("0", 'E')], False), ('E', [('', 'B'), ('', 'I')], True), ('F', [("0", 'G')], False), ('G', [("1", 'H')], False), ('H', [('', 'I')], True), ('I', [("0", 'J')], True), ('J', [], True)]
 == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n4.states)])

 # TEST 5 WHICH IS ALSO A WEIRD EDGE CASE TO WATCH OUT FOR LATER 
def d5(state_value, transition):
    switch = {
        ("A", "0"): ["A", "B"],
        ("A", "1"): ["A"],
        ("B", "0"): ["C"],
        ("B", "1"): ["C"]
    }
    if (state_value, transition) in switch.keys():
        return switch[(state_value, transition)] 
    return None
n5 = NFA(["A", "B", "C"], ["0", "1"], d5, "A", ["C"])
assert([('A', [('0', 'A'), ('0', 'B'), ('1', 'A')], False), ('B', [('0', 'C'), ('1', 'C')], False), ('C', [], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n5.states)])
n5Problem = NFAProblem("10", n5)
n5Problem2 = NFAProblem("10101", n5)
print(n5Problem.is_string_in_language(n5Problem2.to_check, n5Problem.machine.states[0]))
# print(n5Problem2.is_string_in_language(n5Problem2.to_check, n5Problem2.machine.states[0]))
# n4Problem = NFAProblem("1010", n4)
# n4Problem.is_string_in_language(n4Problem.to_check, n4Problem.machine.states[0])

