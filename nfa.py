import sys
from nfa_stdin import NFAStdin
from collections import OrderedDict
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

    def is_string_in_language(self, possible_accepted_string, current_state_value):
        current_state = self.find_state_in_machine(current_state_value)
        states_to_expand = []
        graveyard = []
        states_to_expand.append(current_state)
        graveyard.append(current_state)
        lambdad_states_based_on_expansion = []
        lambdad_states_with_transitions_based_on_expansion = []
        strings_to_expand = []
        if len(self.machine.accept_states) == 0:
            return False
        while len(states_to_expand) != 0:
            states_to_expand = [] if len(states_to_expand) == 1 else states_to_expand[1::]   
            if len(possible_accepted_string) == 0 and current_state.accepted:
                    return True
            else:
                filtered_states_with_transitions_based_on_expansion = []
                for x in current_state.transitions:
                    if len(possible_accepted_string) > 0:
                        if possible_accepted_string[0] in x:
                            filtered_states_with_transitions_based_on_expansion.append(x)
                        if LAMBDA in x:
                            filtered_states_with_transitions_based_on_expansion.append(x)
                            lambdad_states_with_transitions_based_on_expansion.append(x) 
                    else:
                        if LAMBDA in x:
                            filtered_states_with_transitions_based_on_expansion.append(x)
                            lambdad_states_with_transitions_based_on_expansion.append(x) 
                lambdad_states_based_on_expansion = [y for x in lambdad_states_with_transitions_based_on_expansion for y in x if y == x[1]]
                filtered_states_based_on_expansion = [y for x in filtered_states_with_transitions_based_on_expansion for y in x if y == x[1]]
                reconstructed_states_to_expand = []
                reconstructed_strings_to_expand = []
                cycled = False
                if len(filtered_states_based_on_expansion) > 0:
                    for state in filtered_states_based_on_expansion:
                        if state in graveyard:
                            continue
                        else:
                            if not cycled:
                                if current_state.value == state:
                                    cycled = True
                                if state in lambdad_states_based_on_expansion:
                                    reconstructed_strings_to_expand.append(possible_accepted_string)
                                else:
                                    shortened_possible_accepted_string_after_expansion = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]
                                    reconstructed_strings_to_expand.append(shortened_possible_accepted_string_after_expansion)
                                reconstructed_states_to_expand.append(self.find_state_in_machine(state))
                            else:
                                if current_state.value != state:
                                    shortened_possible_accepted_string_after_expansion = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]
                                    reconstructed_strings_to_expand.insert(0, shortened_possible_accepted_string_after_expansion)
                                    reconstructed_states_to_expand.insert(0, self.find_state_in_machine(state))
                for state in states_to_expand:
                    if state in reconstructed_states_to_expand:
                        if cycled: 
                            reconstructed_strings_to_expand.append(strings_to_expand[[x.value for x in states_to_expand].index(state.value)])
                            reconstructed_states_to_expand.append(state)
                        else:
                            continue
                    else:
                        reconstructed_states_to_expand.append(state)
                        reconstructed_strings_to_expand.append(strings_to_expand[[x.value for x in states_to_expand].index(state.value)])
                states_to_expand = reconstructed_states_to_expand
                strings_to_expand = reconstructed_strings_to_expand
                if len(states_to_expand) > 0:
                    next_state = states_to_expand[0]  
                    prev_state = current_state
                    graveyard.append(next_state)
                    current_state = next_state
                    possible_accepted_string = "" if len(strings_to_expand) == 0 else strings_to_expand[[x.value for x in states_to_expand].index(current_state.value)]
                    if len(strings_to_expand) != 0:
                        del strings_to_expand[[x.value for x in states_to_expand].index(current_state.value)]
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

def main():
    try:
        stdin = NFAStdin(sys.argv[1])
        machine = NFA(stdin.states, stdin.transitions, stdin.transition_function, stdin.start_state, stdin.accept_states)
        string = ""  if len(sys.argv) < 3 else sys.argv[2]
        problem = NFAProblem(string, machine)
    except Exception:
        print("Bad input")
    print(problem.is_string_in_language(problem.to_check, problem.machine.start_state))

if __name__ == "__main__":
    main()