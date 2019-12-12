LAMBDA = ""
import sys 
from pathlib import Path
import copy

class NFAStdin:
    start_state = None
    accept_states = []
    states = []
    first = True
    transitions_switch = {}
    transition_function = None
    transitions = []
    pathname = ""
    def __init__(self, path):
        self.pathname = path
        sys.stdin = open(self.pathname, 'r')
        for line in sys.stdin:
            if self.first:
                line = line.strip()
                line = "".join(line.split("START="))
                line = line.split(";")
                self.start_state = line[0]
                line = "".join(line[1::])
                if line.find("ACCEPT") != -1:
                    line = "".join(line.split("ACCEPT=")[1::])
                    self.accept_states = line.split(",")
                    self.states = copy.deepcopy(self.accept_states)
                    self.first = False
            else:
                if line == "\n":
                    continue
                if ":" in line:
                    line = line.strip()
                    line = line.split(":")
                    state = line[0]
                    line = "".join(line[1::]).split("->")
                    transition = line[0]
                    to_transition_to = line[1]
                else:            
                    line = line.strip()        
                    line = line.split("->")
                    state = line[0]
                    transition = LAMBDA
                    to_transition_to = line[1]
                if state not in self.states:
                    self.states.append(state)
                if transition not in self.transitions:
                    self.transitions.append(transition)
                if (state, transition) not in self.transitions_switch:
                    self.transitions_switch[(state, transition)] = [to_transition_to]
                else:
                    self.transitions_switch[(state, transition)].append(to_transition_to)
        self.transition_function = self.transition
    
    def transition(self, state_value, transition):
        if (state_value, transition) in self.transitions_switch.keys():
            return self.transitions_switch[(state_value, transition)] 
        return None