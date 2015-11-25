from __future__ import print_function
from automata import Automata

__author__ = 'koo'

class ENFA(Automata):
    class State(Automata.State):
        def set_trans_func(self, input, next_states):
            self.trans_func[input] = next_states

        def trans(self, input):
            if input in self.trans_func.keys():
                return self.trans_func[input]
            else:
                return False

        def get_e_closure(self):
            e_closure = []

            def get_e_closure_rec(state, e_closure):

                states = state.trans("epsilon")
                for state_ in states:
                    if state_ not in e_closure:
                        e_closure.append(state_)
                        e_closure = get_e_closure_rec(state_, e_closure)

                return e_closure

            return get_e_closure_rec(self, e_closure)

    def get_voca_without_e(self):
        voca_ = []
        for symbol in self.get_voca():
            if symbol != "epsilon":
                voca_.append(symbol)
        return voca_


    def is_acceptable(self, input_string):

        for symbol in input_string:
            if symbol not in self.voca:
                print("wrong input string.")
                return False

        cur_state = self.get_init_state().get_e_closure()

        def is_acceptable_rec(states, input_string):
            if len(input_string) == 0:
                for state in states:
                    if state in self.final_states:
                        return True

            else:
                for state in states:
                    states_ = state.trans(input_string[0])
                    for state_ in states_:
                        if is_acceptable_rec(state_.get_e_closure(), input_string[1:]):
                            return True

                return False


        return is_acceptable_rec(cur_state, input_string)




# make and save a new e_NFA
def make_e_nfa():
    print("Make a new e-NFA.\n")
    enfa_name = raw_input("e-NFA name? ")

    enfa = ENFA(enfa_name)

    voca = raw_input("vocabulary? (seperated by space) ")
    voca = list(set(voca.split()))
    voca.append("epsilon")

    enfa.set_voca(voca)

    print("Vocabulary (duplicates are removed and epsilon for e-move is included.)")
    enfa.show_voca()

    names = raw_input("Enter state names. (seperated by space) ")

    for name in names.split():
        enfa.add_state(name)

    dead_state = enfa.add_state("dead_state")

    print("%d states are created. (including dead state)" % (len(names.split()) + 1))
    enfa.show_all_states()
    print()

    states = enfa.get_all_states()
    voca = enfa.get_voca()

    print("Setting state transition function...")
    print("You can input any number of states. Just make sure they are seperated by space. (e.g., delta(q0, x) -> q1 q2)")
    print("If you don't want to specify transition, enter 'None' (for allowing partial function)\n")

    for state in states:
        if state is not dead_state:
            for input_symbol in voca:
                success = False
                while not success:
                    next = raw_input("delta(%s, %s) -> " % (state.get_name(), input_symbol))
                    if next == "None": # daed state
                        if input_symbol == "epsilon":
                            next_states = []
                        else:
                            next_states = [enfa.get_state("dead_state")]
                        success = True
                    else:
                        next_states = []
                        for state_ in next.split():
                            if enfa.get_state(state_):
                                next_states.append(enfa.get_state(state_))
                            else:
                                next_states = False
                                break

                    if input_symbol == "epsilon":
                        if state not in next_states:
                            next_states.append(state)


                    if next_states:
                        state.set_trans_func(input_symbol, next_states)
                        success = True
                    else:
                        print("State doesn't exist. Please try again.")
        else:
            for input_symbol in voca:
                dead_state.set_trans_func(input_symbol, [dead_state])


    init_state = raw_input("initial state? ")
    final_states = raw_input("final states? (seperated by space) ")
    final_states = final_states.split()

    enfa.set_init_state(enfa.get_state(init_state))
    for state in final_states:
        enfa.add_final_state(enfa.get_state(state))

    """
    success = False
    while not success:
        save = raw_input("Do you want to save current automata? (y/n)")
        if save == "y" or save == "Y" or save == "n" or save == "N":
            success = True
        else:
            print("wrong input.")

    if save == "y" or save == "Y":
        save_automata(automata)
        print("Current automata is saved as configs/%s.xml" % automata.get_name())
    """

    return enfa

def accept_test(enfa):
    print("Acceptance test of e-NFA %s" % enfa.get_name())
    print("If you want to input null string, enter 'epsilon'")
    while True:
        input_string = raw_input("input string? ")

        if enfa.is_acceptable(input_string):
            print("string accepted.")
        else:
            print("string not accepted.")

def make_sample1():
    enfa = ENFA("sample1")
    enfa.set_voca(['a', 'b', 'epsilon'])

    for i in range(5):
        enfa.add_state("q%d" % (i+1))
    enfa.add_state("dead_state")

    dead_state = enfa.get_state("dead_state")
    q0 = enfa.get_state("q1")
    q1 = enfa.get_state("q2")
    q2 = enfa.get_state("q3")
    q3 = enfa.get_state("q4")
    q4 = enfa.get_state("q5")

    q0.set_trans_func('a', [q2])
    q0.set_trans_func('b', [dead_state])
    q0.set_trans_func('epsilon', [q0, q1])

    q1.set_trans_func('a', [q3, q4])
    q1.set_trans_func('b', [dead_state])
    q1.set_trans_func('epsilon', [q1])

    q2.set_trans_func('a', [dead_state])
    q2.set_trans_func('b', [q3])
    q2.set_trans_func('epsilon', [q2])

    q3.set_trans_func('a', [q4])
    q3.set_trans_func('b', [q4])
    q3.set_trans_func('epsilon', [q3])

    q4.set_trans_func('a', [dead_state])
    q4.set_trans_func('b', [dead_state])
    q4.set_trans_func('epsilon', [q4])

    dead_state.set_trans_func('a', [dead_state])
    dead_state.set_trans_func('b', [dead_state])
    dead_state.set_trans_func('epsilon', [dead_state])

    enfa.set_init_state(q0)
    enfa.add_final_state(q4)

    return enfa

def make_sample2():
    enfa = ENFA("sample2")
    enfa.set_voca(['a', 'b', 'epsilon'])

    for i in range(11):
        enfa.add_state("%d" % i)
    enfa.add_state("dead_state")

    dead_state = enfa.get_state("dead_state")
    q0 = enfa.get_state("0")
    q1 = enfa.get_state("1")
    q2 = enfa.get_state("2")
    q3 = enfa.get_state("3")
    q4 = enfa.get_state("4")
    q5 = enfa.get_state("5")
    q6 = enfa.get_state("6")
    q7 = enfa.get_state("7")
    q8 = enfa.get_state("8")
    q9 = enfa.get_state("9")
    q10 = enfa.get_state("10")

    q0.set_trans_func('a', [dead_state])
    q0.set_trans_func('b', [dead_state])
    q0.set_trans_func('epsilon', [q0, q1, q7])

    q1.set_trans_func('a', [dead_state])
    q1.set_trans_func('b', [dead_state])
    q1.set_trans_func('epsilon', [q1, q2, q4])

    q2.set_trans_func('a', [q3])
    q2.set_trans_func('b', [dead_state])
    q2.set_trans_func('epsilon', [q2])

    q3.set_trans_func('a', [dead_state])
    q3.set_trans_func('b', [dead_state])
    q3.set_trans_func('epsilon', [q3, q6])

    q4.set_trans_func('a', [dead_state])
    q4.set_trans_func('b', [q5])
    q4.set_trans_func('epsilon', [q4])

    q5.set_trans_func('a', [dead_state])
    q5.set_trans_func('b', [dead_state])
    q5.set_trans_func('epsilon', [q5, q6])

    q6.set_trans_func('a', [dead_state])
    q6.set_trans_func('b', [dead_state])
    q6.set_trans_func('epsilon', [q1, q6, q7])

    q7.set_trans_func('a', [q8])
    q7.set_trans_func('b', [dead_state])
    q7.set_trans_func('epsilon', [q7])

    q8.set_trans_func('a', [dead_state])
    q8.set_trans_func('b', [q9])
    q8.set_trans_func('epsilon', [q8])

    q9.set_trans_func('a', [dead_state])
    q9.set_trans_func('b', [q10])
    q9.set_trans_func('epsilon', [q9])

    q10.set_trans_func('a', [dead_state])
    q10.set_trans_func('b', [dead_state])
    q10.set_trans_func('epsilon', [q10])

    dead_state.set_trans_func('a', [dead_state])
    dead_state.set_trans_func('b', [dead_state])
    dead_state.set_trans_func('epsilon', [dead_state])

    enfa.set_init_state(q0)
    enfa.add_final_state(q10)

    return enfa


if __name__ == "__main__":
    print ("""
2015 Fall CS322 project. Developed by YP Koo.

Welcome to e-NFA world!
""")

    enfa = make_e_nfa()
    accept_test(enfa)

