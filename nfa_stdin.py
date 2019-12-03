LAMBDA = ""
import sys 
from pathlib import Path

class NFAStdin:
    start_state = None
    accept_states = []
    states = []
    first = True
    transitions_switch = {}
    transition_function = None
    transitions = []
    # handle in main filename, string_to_test
    def __int__(self, pathname, possible_string):
        for line in sys.stdin:
            if first:
                line = line.split("START=")[1::].split(";")
                start_state = line[0]
                line = line.split("ACCEPT=")[1::]
                accept_states = line.split(",")
                states = accept_states
                first = False
            else: 
                if ":" in line:
                    line = line.split(":")
                    state = line[0]
                    line = line.split("->")
                    transition = line[0]
                    to_transition_to = line[1]
                else:                    
                    line = line.split("->")
                    state = line[0]
                    transition = LAMBDA
                    to_transition_to = line[1]
                if state not in states:
                    states.append(state)
                if transition not in transitions:
                    transitions.append(transition)
                if (state, transition) not in transitions_switch:
                    transitions_switch[(state, transition)] = [to_transition_to]
                else:
                    transitions_switch[(state, transition)].append(to_transition_to)
        transition_function = self.transition
    
    def transition(self, state_value, transition):
        if (state_value, transition) in transitions_switch.keys():
            return transitions_switch[(state_value, transition)] 
        return None
