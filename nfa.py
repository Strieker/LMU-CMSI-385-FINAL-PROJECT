import sys
from nfa_stdin import NFAStdin
LAMBDA = ""
# WEIRD CASE WHERE YOU GO TO ANOTHER VALUE AND THE STRING THINGS ACCEPTED WHEN IT'S NOT 
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

    # clean it up so it's recursive 
    # call it accepts 
    def is_string_in_language(self, possible_accepted_string, current_state_value):
        current_state = self.find_state_in_machine(current_state_value)
        current_states_to_check_current_transitions_on = []
        graveyard = []
        current_states_to_check_current_transitions_on.append(current_state)
        lambdas = []
        lambda_transitions = []
        while len(current_states_to_check_current_transitions_on) != 0:
            if len(possible_accepted_string) == 0 and current_state.accepted:
                    return True
            else:
                filtered_transitions = []
                for x in current_state.transitions:
                    if len(possible_accepted_string) > 0:
                        if possible_accepted_string[0] in x:
                            filtered_transitions.append(x)
                        elif LAMBDA in x:
                            filtered_transitions.append(x)
                            lambda_transitions.append(x)
                lambdas = [y for x in lambda_transitions for y in x if y == x[1]]
                filtered_states = [y for x in filtered_transitions for y in x if y == x[1]]
                if len(filtered_states) > 0:
                    for state in filtered_states:
                        if state not in current_states_to_check_current_transitions_on and state not in graveyard:
                            current_states_to_check_current_transitions_on.append(self.find_state_in_machine(state))
                state_to_pass = current_states_to_check_current_transitions_on[0]  
                current_states_to_check_current_transitions_on = current_states_to_check_current_transitions_on[1::]
                graveyard.append(state_to_pass)
                current_state = state_to_pass
            if(current_state.value not in lambdas):
                possible_accepted_string = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]
        if len(possible_accepted_string) == 0 and current_state.accepted:
                    return True
        return False

    def find_state_in_machine(self, state_value):
        for state in self.machine.states:
            if state.value == state_value:
                return state

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
n2Problem = NFAProblem("100001", n2)
print(n2Problem.is_string_in_language(n2Problem.to_check, n2Problem.machine.start_state))

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
print(n5Problem.is_string_in_language(n5Problem.to_check, n5Problem.machine.start_state))
print(n5Problem2.is_string_in_language(n5Problem2.to_check, n5Problem.machine.start_state))
# n4Problem = NFAProblem("1010", n4)
# n4Problem.is_string_in_language(n4Problem.to_check, n4Problem.machine.states[0])

def main():
    stdin = NFAStdin(sys.argv[1])
    string = sys.argv[2]
    machine = NFA(stdin.states, stdin.transitions, stdin.transition_function, stdin.start_state, stdin.accept_states)
    problem = NFAProblem(string, machine)
    print(problem.is_string_in_language(problem.to_check, problem.machine.start_state))

if __name__ == "__main__":
    main()