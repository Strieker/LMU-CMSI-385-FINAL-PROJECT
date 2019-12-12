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
    # handle in main filename, string_to_test
    # HANDLE IF NO ACCEPT STATES
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

# n1 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa1.in")
# print(n1.start_state)
# print(n1.accept_states)
# print(n1.states)
# print(n1.transitions_switch)
# print(n1.transitions)

# n2 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa2.in")
# print(n2.start_state)
# print(n2.accept_states)
# print(n2.states)
# print(n2.transitions_switch)
# print(n2.transitions)

# n3 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa3.in")
# print(n3.start_state)
# print(n3.accept_states)
# print(n3.states)
# print(n3.transitions_switch)
# print(n3.transitions)


# n4 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa4.txt")
# print(n4.start_state)
# print(n4.accept_states)
# print(n4.states)
# print(n4.transitions_switch)
# print(n4.transitions)

# n5 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa5.txt")
# print(n5.start_state)
# print(n5.accept_states)
# print(n5.states)
# print(n5.transitions_switch)
# print(n5.transitions)

# n6 = NFAStdin("/Users/sas/Desktop/McLovin It/Junior Year/Work Hard/theory/LMU-CMSI-385-FINAL-PROJECT/nfa6.in")
# print(n6.start_state)
# print(n6.accept_states)
# print(n6.states)
# print(n6.transitions_switch)
# print(n6.transitions)