import sys
from nfa_stdin import NFAStdin
from collections import OrderedDict
LAMBDA = ""
#CHECK YOU DONT GET ACCEPTED WHEN AT ACCEPT STATE BUT STILL A STRING LEFT 
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
        graveyard.append(current_state)
        lambdas = []
        lambda_transitions = []
        current_strings = []
        while len(current_states_to_check_current_transitions_on) != 0:
            
            current_states_to_check_current_transitions_on = [] if len(current_states_to_check_current_transitions_on) == 1 else current_states_to_check_current_transitions_on[1::]   
            print("current state value: " + str(current_state.value))
            print("to expand: ")
            print([x.value for x in current_states_to_check_current_transitions_on])
            if len(possible_accepted_string) == 0 and current_state.accepted:
                    return True
            else:
                filtered_transitions = []
                for x in current_state.transitions:
                    if len(possible_accepted_string) > 0:
                        if possible_accepted_string[0] in x:
                            filtered_transitions.append(x)
                        if LAMBDA in x:
                            filtered_transitions.append(x)
                            lambda_transitions.append(x) 
                    else:
                        if LAMBDA in x:
                            filtered_transitions.append(x)
                            lambda_transitions.append(x) 
                lambdas = [y for x in lambda_transitions for y in x if y == x[1]]
                print("lambdas: ")
                print(lambdas)
                filtered_states = [y for x in filtered_transitions for y in x if y == x[1]]
                new_start_of_transitions = []
                current_strings1 = []
                if len(filtered_states) > 0:
                    for state in filtered_states:
                        if state in graveyard:
                            continue
                        else:
                            new_start_of_transitions.append(self.find_state_in_machine(state))
                            if state in lambdas:
                                current_strings1.append(possible_accepted_string)
                            else:
                                part_time_string = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]
                                current_strings1.append(part_time_string)
                for state in current_states_to_check_current_transitions_on:
                    if state in new_start_of_transitions:
                        continue
                    else:
                        new_start_of_transitions.append(state)
                        if state in lambdas:
                            current_strings1.append(possible_accepted_string)
                        else:
                            part_time_string = "" if len(possible_accepted_string) <= 1 else possible_accepted_string[1::]
                            current_strings1.append(part_time_string)
                current_states_to_check_current_transitions_on = new_start_of_transitions
                current_strings = current_strings1
                print("please god strings:")
                print(current_strings)
                print("to expand2: ")
                print([x.value for x in current_states_to_check_current_transitions_on])

                if len(current_states_to_check_current_transitions_on) > 0:
                    state_to_pass = current_states_to_check_current_transitions_on[0]  
                    prev_state = current_state
                    graveyard.append(state_to_pass)
                    current_state = state_to_pass
                    if current_state.value not in lambdas:
                        print("made it")
                    if len(current_strings) > 0:
                        possible_accepted_string = current_strings[[x.value for x in current_states_to_check_current_transitions_on].index(current_state.value)]
                        del current_strings[[x.value for x in current_states_to_check_current_transitions_on].index(current_state.value)]
                        print(possible_accepted_string)
                    print("strings:")
                    print(current_strings)
                print(possible_accepted_string)
                print("--------\n")
            
        # if len(possible_accepted_string) == 0 and current_state.accepted:
        #             return True
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