import sys
from nfa import NFA, NFAProblem, LAMBDA
from nfa_stdin import NFAStdin

class Test:
    def d1(self, state_value, transition):
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

    def test1(self):
        n1 = NFA(["A", "B", "C", "D", "E"], ["0", "1"], self.d1, "A", ["E"])
        assert([('A', [("0", 'B'), ("1", 'C')], False), ('B', [("0", 'B'), ("1", 'D')], False), ('C', [("0", 'B'), ("1", 'C')], False), ('D', [("0", 'B'), ("1", 'E')], False), ('E', [("0", 'B'), ("1", 'C')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n1.states)])

    def d2(self, state_value, transition):
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
        
    def test2(self):
        n2 = NFA(["A", "B", "C", "D", "E", "F"], ["0", "1", LAMBDA], self.d2, "F", ["B", "D", "F", "E"])
        assert([('A', [("0", 'B')], False), ('B', [('', 'F')], True), ('C', [("1", 'D')], False), ('D', [('', 'F')], True), ('E', [('', 'C'), ('', 'A')], True), ('F', [('', 'E')], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n2.states)])

    def d3(self, state_value, transition):
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

    def test3(self):
        n3 = NFA(["AE", "BF", "CE", "CF", "DE", "DF"], ["0", "1"], self.d3, "AE", ["DE", "AE", "CE", "CF"])
        assert([('AE', [("0", 'BF'), ("1", 'DE')], True), ('BF', [("0", 'CE'), ("1", 'CF')], False), ('CE', [("0", 'DF'), ("1", 'DE')], True), ('CF', [("0", 'DE'), ("1", 'DF')], True), ('DE', [("0", 'DF'), ("1", 'DE')], True), ('DF', [("0", 'DE'), ("1", 'DF')], False)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n3.states)])
 
    def d4(self, state_value, transition):
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
        
    def test4(self):
        n4 = NFA(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], ["0", "1", LAMBDA], self.d4, "A", ["B", "E", "H", "I", "J"])
        assert([('A', [('', 'B'), ('', 'F')], False), ('B', [('', 'C'), ('', 'I')], True), ('C', [("1", 'D')], False), ('D', [("0", 'E')], False), ('E', [('', 'B'), ('', 'I')], True), ('F', [("0", 'G')], False), ('G', [("1", 'H')], False), ('H', [('', 'I')], True), ('I', [("0", 'J')], True), ('J', [], True)]
 == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n4.states)])


    def d5(self, state_value, transition):
        switch = {
            ("A", "0"): ["A", "B"],
            ("A", "1"): ["A"],
            ("B", "0"): ["C"],
            ("B", "1"): ["C"]
        }
        if (state_value, transition) in switch.keys():
            return switch[(state_value, transition)] 
        return None
    
    def test5(self):
        n5 = NFA(["A", "B", "C"], ["0", "1"], self.d5, "A", ["C"])
        assert([('A', [('0', 'A'), ('0', 'B'), ('1', 'A')], False), ('B', [('0', 'C'), ('1', 'C')], False), ('C', [], True)] == [state for state in map(lambda state: (state.value, state.transitions, state.accepted), n5.states)])


    def test6(self):
        stdin1 = NFAStdin("nfa1.in")
        machine1 = NFA(stdin1.states, stdin1.transitions, stdin1.transition_function, stdin1.start_state, stdin1.accept_states)
        assert(NFAProblem("a", machine1).is_string_in_language(NFAProblem("a", machine1).to_check, NFAProblem("a", machine1).machine.start_state))
        assert(NFAProblem("", machine1).is_string_in_language(NFAProblem("", machine1).to_check, NFAProblem("", machine1).machine.start_state) == False)
        assert(NFAProblem("aa", machine1).is_string_in_language(NFAProblem("aa", machine1).to_check, NFAProblem("aa", machine1).machine.start_state))
        assert(NFAProblem("aaaaaaaaaaaaaaaaa", machine1).is_string_in_language(NFAProblem("aaaaaaaaaaaaaaaaa", machine1).to_check, NFAProblem("aaaaaaaaaaaaaaaaa", machine1).machine.start_state))

    def test7(self):
        stdin2 = NFAStdin("nfa2.in")
        machine2 = NFA(stdin2.states, stdin2.transitions, stdin2.transition_function, stdin2.start_state, stdin2.accept_states)
        assert(NFAProblem("011", machine2).is_string_in_language(NFAProblem("011", machine2).to_check, NFAProblem("011", machine2).machine.start_state))
        assert(NFAProblem("0000000011", machine2).is_string_in_language(NFAProblem("0000000011", machine2).to_check, NFAProblem("0000000011", machine2).machine.start_state))
        assert(NFAProblem("011101011", machine2).is_string_in_language(NFAProblem("011101011", machine2).to_check, NFAProblem("011101011", machine2).machine.start_state))
        assert(NFAProblem("11111100001011", machine2).is_string_in_language(NFAProblem("11111100001011", machine2).to_check, NFAProblem("11111100001011", machine2).machine.start_state))
        assert(NFAProblem("0110", machine2).is_string_in_language(NFAProblem("0110", machine2).to_check, NFAProblem("0110", machine2).machine.start_state) == False)
        assert(NFAProblem("0111", machine2).is_string_in_language(NFAProblem("0111", machine2).to_check, NFAProblem("0111", machine2).machine.start_state) == False)
        assert(NFAProblem("01110", machine2).is_string_in_language(NFAProblem("01110", machine2).to_check, NFAProblem("01110", machine2).machine.start_state) == False)
        assert(NFAProblem("11", machine2).is_string_in_language(NFAProblem("11", machine2).to_check, NFAProblem("11", machine2).machine.start_state) == False)
        assert(NFAProblem("111111000010110", machine2).is_string_in_language(NFAProblem("111111000010110", machine2).to_check, NFAProblem("111111000010110", machine2).machine.start_state) == False)
        assert(NFAProblem("", machine2).is_string_in_language(NFAProblem("", machine2).to_check, NFAProblem("", machine2).machine.start_state) == False)


    def test8(self):
        stdin3 = NFAStdin("nfa3.in")
        machine3 = NFA(stdin3.states, stdin3.transitions, stdin3.transition_function, stdin3.start_state, stdin3.accept_states)
        assert(NFAProblem("", machine3).is_string_in_language(NFAProblem("", machine3).to_check, NFAProblem("", machine3).machine.start_state))
        assert(NFAProblem("00", machine3).is_string_in_language(NFAProblem("00", machine3).to_check, NFAProblem("00", machine3).machine.start_state))
        assert(NFAProblem("010", machine3).is_string_in_language(NFAProblem("010", machine3).to_check, NFAProblem("010", machine3).machine.start_state))
        assert(NFAProblem("0", machine3).is_string_in_language(NFAProblem("0", machine3).to_check, NFAProblem("0", machine3).machine.start_state))
        assert(NFAProblem("1", machine3).is_string_in_language(NFAProblem("1", machine3).to_check, NFAProblem("1", machine3).machine.start_state))


    def test9(self):
        stdin4 = NFAStdin("nfa4.txt")
        machine4 = NFA(stdin4.states, stdin4.transitions, stdin4.transition_function, stdin4.start_state, stdin4.accept_states)
        assert(NFAProblem("", machine4).is_string_in_language(NFAProblem("", machine4).to_check, NFAProblem("", machine4).machine.start_state))
        assert(NFAProblem("1", machine4).is_string_in_language(NFAProblem("1", machine4).to_check, NFAProblem("1", machine4).machine.start_state))
        assert(NFAProblem("001", machine4).is_string_in_language(NFAProblem("001", machine4).to_check, NFAProblem("001", machine4).machine.start_state))
        assert(NFAProblem("00011101", machine4).is_string_in_language(NFAProblem("00011101", machine4).to_check, NFAProblem("00011101", machine4).machine.start_state))
        assert(NFAProblem("01", machine4).is_string_in_language(NFAProblem("01", machine4).to_check, NFAProblem("01", machine4).machine.start_state))
        assert(NFAProblem("010", machine4).is_string_in_language(NFAProblem("010", machine4).to_check, NFAProblem("010", machine4).machine.start_state))
        assert(NFAProblem("0101", machine4).is_string_in_language(NFAProblem("0101", machine4).to_check, NFAProblem("0101", machine4).machine.start_state))
        assert(NFAProblem("01111101", machine4).is_string_in_language(NFAProblem("01111101", machine4).to_check, NFAProblem("01111101", machine4).machine.start_state))
        assert(NFAProblem("1011101", machine4).is_string_in_language(NFAProblem("1011101", machine4).to_check, NFAProblem("1011101", machine4).machine.start_state))
        assert(NFAProblem("0", machine4).is_string_in_language(NFAProblem("0", machine4).to_check, NFAProblem("0", machine4).machine.start_state) == False)
        assert(NFAProblem("000", machine4).is_string_in_language(NFAProblem("000", machine4).to_check, NFAProblem("000", machine4).machine.start_state) == False)
        assert(NFAProblem("0001", machine4).is_string_in_language(NFAProblem("0001", machine4).to_check, NFAProblem("0001", machine4).machine.start_state) == False)
        assert(NFAProblem("000111", machine4).is_string_in_language(NFAProblem("000111", machine4).to_check, NFAProblem("000111", machine4).machine.start_state) == False)
        assert(NFAProblem("00011101101", machine4).is_string_in_language(NFAProblem("00011101101", machine4).to_check, NFAProblem("00011101101", machine4).machine.start_state) == False)
        assert(NFAProblem("011111", machine4).is_string_in_language(NFAProblem("011111", machine4).to_check, NFAProblem("011111", machine4).machine.start_state) == False)
        assert(NFAProblem("00000", machine4).is_string_in_language(NFAProblem("00000", machine4).to_check, NFAProblem("00000", machine4).machine.start_state) ==  False)

    def test10(self):
        stdin5 = NFAStdin("nfa5.txt")
        machine5 = NFA(stdin5.states, stdin5.transitions, stdin5.transition_function, stdin5.start_state, stdin5.accept_states)
        assert(NFAProblem("10", machine5).is_string_in_language(NFAProblem("10", machine5).to_check, NFAProblem("10", machine5).machine.start_state))
        assert(NFAProblem("100", machine5).is_string_in_language(NFAProblem("100", machine5).to_check, NFAProblem("100", machine5).machine.start_state))
        assert(NFAProblem("01", machine5).is_string_in_language(NFAProblem("01", machine5).to_check, NFAProblem("01", machine5).machine.start_state))
        assert(NFAProblem("010", machine5).is_string_in_language(NFAProblem("010", machine5).to_check, NFAProblem("010", machine5).machine.start_state))
        assert(NFAProblem("1010100", machine5).is_string_in_language(NFAProblem("1010100", machine5).to_check, NFAProblem("1010100", machine5).machine.start_state))
        assert(NFAProblem("", machine5).is_string_in_language(NFAProblem("", machine5).to_check, NFAProblem("", machine5).machine.start_state))
        assert(NFAProblem("00", machine5).is_string_in_language(NFAProblem("00", machine5).to_check, NFAProblem("00", machine5).machine.start_state) == False)
        assert(NFAProblem("1000", machine5).is_string_in_language(NFAProblem("1000", machine5).to_check, NFAProblem("1000", machine5).machine.start_state) == False)
        assert(NFAProblem("1000000000000000", machine5).is_string_in_language(NFAProblem("1000000000000000", machine5).to_check, NFAProblem("1000000000000000", machine5).machine.start_state) == False)
        assert(NFAProblem("1111111111111111", machine5).is_string_in_language(NFAProblem("1111111111111111", machine5).to_check, NFAProblem("1111111111111111", machine5).machine.start_state) == False)
        assert(NFAProblem("000000000000000", machine5).is_string_in_language(NFAProblem("000000000000000", machine5).to_check, NFAProblem("000000000000000", machine5).machine.start_state) == False)

    def test11(self):
        stdin6 = NFAStdin("nfa6.in")
        machine6 = NFA(stdin6.states, stdin6.transitions, stdin6.transition_function, stdin6.start_state, stdin6.accept_states)
        assert(NFAProblem("000", machine6).is_string_in_language(NFAProblem("000", machine6).to_check, NFAProblem("000", machine6).machine.start_state))
        assert(NFAProblem("00", machine6).is_string_in_language(NFAProblem("00", machine6).to_check, NFAProblem("00", machine6).machine.start_state))
        assert(NFAProblem("1111101", machine6).is_string_in_language(NFAProblem("1111101", machine6).to_check, NFAProblem("1111101", machine6).machine.start_state))
        assert(NFAProblem("1111100", machine6).is_string_in_language(NFAProblem("1111100", machine6).to_check, NFAProblem("1111100", machine6).machine.start_state))
        assert(NFAProblem("1010000000", machine6).is_string_in_language(NFAProblem("1010000000", machine6).to_check, NFAProblem("1010000000", machine6).machine.start_state))
        assert(NFAProblem("00000001", machine6).is_string_in_language(NFAProblem("00000001", machine6).to_check, NFAProblem("00000001", machine6).machine.start_state))
        assert(NFAProblem("", machine6).is_string_in_language(NFAProblem("", machine6).to_check, NFAProblem("", machine6).machine.start_state) == False)
        assert(NFAProblem("0", machine6).is_string_in_language(NFAProblem("0", machine6).to_check, NFAProblem("0", machine6).machine.start_state) == False)
        assert(NFAProblem("010", machine6).is_string_in_language(NFAProblem("010", machine6).to_check, NFAProblem("010", machine6).machine.start_state) == False)
        assert(NFAProblem("01010", machine6).is_string_in_language(NFAProblem("01010", machine6).to_check, NFAProblem("01010", machine6).machine.start_state) == False)
        assert(NFAProblem("111110", machine6).is_string_in_language(NFAProblem("111110", machine6).to_check, NFAProblem("111110", machine6).machine.start_state) == False)
        assert(NFAProblem("00000000000001111110", machine6).is_string_in_language(NFAProblem("00000000000001111110", machine6).to_check, NFAProblem("00000000000001111110", machine6).machine.start_state) == False)
        assert(NFAProblem("1110", machine6).is_string_in_language(NFAProblem("1110", machine6).to_check, NFAProblem("1110", machine6).machine.start_state) == False)
        assert(NFAProblem("sdfghkl;kjhgfdsfghjkl", machine6).is_string_in_language(NFAProblem("sdfghkl;kjhgfdsfghjkl", machine6).to_check, NFAProblem("sdfghkl;kjhgfdsfghjkl", machine6).machine.start_state) == False)

    def test12(self):
        stdin7 = NFAStdin("nfa7.txt")
        machine7 = NFA(stdin7.states, stdin7.transitions, stdin7.transition_function, stdin7.start_state, stdin7.accept_states)
        assert(NFAProblem("000000000000000", machine7).is_string_in_language(NFAProblem("000000000000000", machine7).to_check, NFAProblem("000000000000000", machine7).machine.start_state) == False)
        assert(NFAProblem("", machine7).is_string_in_language(NFAProblem("", machine7).to_check, NFAProblem("", machine7).machine.start_state))

    def test13(self):
        stdin8 = NFAStdin("nfa8.in")
        machine8 = NFA(stdin8.states, stdin8.transitions, stdin8.transition_function, stdin8.start_state, stdin8.accept_states)
        assert(NFAProblem("000000000000000", machine8).is_string_in_language(NFAProblem("000000000000000", machine8).to_check, NFAProblem("000000000000000", machine8).machine.start_state) == False)
        assert(NFAProblem("", machine8).is_string_in_language(NFAProblem("", machine8).to_check, NFAProblem("", machine8).machine.start_state) == False)
        assert(NFAProblem("asdfghgfdsa", machine8).is_string_in_language(NFAProblem("asdfghgfdsa", machine8).to_check, NFAProblem("asdfghgfdsa", machine8).machine.start_state) == False)

def main():
    test = Test()
    # UNCOMMENT ONE FUNCTION CALL AT A TIME 
    # test.test1()
    # test.test2()
    # test.test3()
    # test.test4()
    # test.test5()
    # test.test6()
    # test.test7()
    # test.test8()
    # test.test9()
    # test.test10()
    # test.test11()
    # test.test12()
    # test.test13()

if __name__ == "__main__":
    main()