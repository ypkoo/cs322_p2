from __future__ import print_function
from eNFA import *
from automata import *


__author__ = 'koo'


class Converter:
    def states_to_names(self, states):
        names = []
        for state in states:
            names.append(state.get_name())
        return " ".join(names)

    def names_to_states(self, enfa, names):
        states = []
        state_names = names.split()

        for state_name in state_names:
            states.append(enfa.get_state(state_name))
        return states

    def construct_table1(self, enfa):
        table = {}

        for state in enfa.get_all_states():
            table[state.get_name()] = {}
            for symbol in enfa.get_voca():
                if symbol == "epsilon":
                    table[state.get_name()][symbol] = self.states_to_names(state.get_e_closure())
                else:
                    table[state.get_name()][symbol] = self.states_to_names(state.trans(symbol))

        return table

    def construct_table2(self, enfa, table1):
        table2 = {}

        init_states = enfa.get_init_state().get_e_closure()
        state_set = set([self.states_to_names(init_states)])
        state_set_ = set([])

        while state_set != state_set_:
            for state_names in state_set - state_set_:
                table2[state_names] = {}
                for symbol in enfa.get_voca():
                    if symbol != "epsilon":
                        result1 = ""
                        result2 = ""
                        names = state_names.split()
                        for name in names:
                            if table1[name][symbol] != "dead_state":
                                result1 = result1 + " " + table1[name][symbol]
                        if result1 == "":
                            result1 = "dead_state"
                        else:
                            result1 = result1[1:]
                        for s in list(set(result1.split())):
                            result2 = result2 + " " + table1[s]["epsilon"]
                        result2 = result2[1:]
                        result2 = " ".join(list(set(result2.split())))
                        table2[state_names][symbol] = result2
                        if result2 != []:
                            state_set.add(result2)
                        state_set_.add(state_names)

        return table2, self.states_to_names(init_states)

    def convert(self, enfa):

        table1 = self.construct_table1(enfa)
        table2, init_state_name = self.construct_table2(enfa, table1)

        automata = Automata("dfa")

        for key in table2.keys():
            automata.add_state(key)
        #automata.add_state("dead_state")

        automata.set_voca(enfa.get_voca_without_e())

        dead_state = automata.get_state("dead_state")
        for state in automata.get_all_states():
            if not state is dead_state:
                for symbol in automata.get_voca():
                    next = table2[state.get_name()][symbol]
                    next_state = automata.get_state(next)
                    state.set_trans_func(symbol, next_state)
            else:
                for symbol in automata.get_voca():
                    state.set_trans_func(symbol, dead_state)

        automata.set_init_state(automata.get_state(init_state_name))

        final_state_names = []
        for state in enfa.get_final_states():
            final_state_names.append(state.get_name())
        final_state_names = set(final_state_names)

        for state in automata.get_all_states():
            state_names = set(state.get_name().split())
            if state_names & final_state_names:
                automata.add_final_state(state)

        return automata

class Minimizer:
    def init_table(self, dfa):
        table = {}
        for state1 in dfa.get_all_states():
            if state1 != dfa.get_state("dead_state"):
                table[state1.get_name()] = {}
                for state2 in dfa.get_all_states():
                    if state2 != dfa.get_state("dead_state"):
                        table[state1.get_name()][state2.get_name()] = False
        return table

    def is_distinct(self, dfa, table, state1, state2):
        if state1 in dfa.get_final_states() and state2 not in dfa.get_final_states():
            return True
        if state2 in dfa.get_final_states() and state1 not in dfa.get_final_states():
            return True
        for symbol in dfa.get_voca():
            next1 = state1.trans(symbol)
            next2 = state2.trans(symbol)
            if next1.get_name() == "dead_state" and next2 in dfa.get_final_states():
                return True
            if next2.get_name() == "dead_state" and next1 in dfa.get_final_states():
                return True
            if next1.get_name() == "dead_state" and next2.get_name() == "dead_state":
                continue
            try:
                if table[next1.get_name()][next2.get_name()] or table[next2.get_name()][next1.get_name()]:
                    return True
            except:
                return True
        return False

    def construct_table(self, dfa):
        table = self.init_table(dfa)
        while True:
            table_old = table
            for i in range(2):
                for state1 in dfa.get_all_states():
                    if state1 != dfa.get_state("dead_state"):
                        for state2 in dfa.get_all_states():
                            if state2 != dfa.get_state("dead_state"):
                                name1 = state1.get_name()
                                name2 = state2.get_name()
                                if table[name1][name2] == False or table[name2][name1] == False:
                                    table[name1][name2] = self.is_distinct(dfa, table, state1, state2)
                                    table[name2][name1] = self.is_distinct(dfa, table, state1, state2)
            if table == table_old:
                break
        return table

    def minimize(self, dfa):
        table = self.construct_table(dfa)
        not_distinct_sets = []

        for key1 in table.keys():
            for key2 in table[key1].keys():
                if not table[key1][key2]:
                    if key1 != key2:
                        inserted = False
                        not_distinct_set = set([key1, key2])
                        for s in not_distinct_sets:
                            if s & not_distinct_set:
                                s = s | not_distinct_set
                                inserted = True
                        if not inserted:
                            not_distinct_sets.append(not_distinct_set)

        m_dfa = Automata("m_dfa")

        m_dfa.set_voca(dfa.get_voca())

        for state in dfa.get_all_states():
            is_in = False
            for s in not_distinct_sets:
                if state.get_name() in s:
                    is_in = True
            if not is_in:
                m_dfa.add_state(state.get_name())

        new_states = []
        new_mapping = {}
        for s in not_distinct_sets:
            new_state = ""
            for s_ in s:
                new_state = new_state + " " + s_
            new_states.append(" ".join(set(new_state.split())))
            new_mapping[" ".join(set(new_state.split()))] = s

        for new_state in new_states:
            m_dfa.add_state(new_state)

        for state in m_dfa.get_all_states():
            for symbol in m_dfa.get_voca():
                if state.get_name() not in new_states:
                    next = dfa.get_state(state.get_name()).trans(symbol)
                else:
                    cur_state = list(new_mapping[state.get_name()])[0]
                    next = dfa.get_state(cur_state).trans(symbol)

                for key in new_mapping.keys():
                    if next in new_mapping[key]:
                        next = m_dfa.get_state(key)
                        break

                state.set_trans_func(symbol, next)

        initial_state_name = dfa.get_init_state().get_name()
        initial_state = dfa.get_init_state()
        for key in new_mapping.keys():
            if initial_state_name in new_mapping[key]:
                initial_state = m_dfa.get_state(key)
                break
        m_dfa.set_init_state(initial_state)

        final_states = dfa.get_final_states()
        for state in final_states:
            final_state = state
            for key in new_mapping.keys():
                if state.get_name() in new_mapping[key]:
                    final_state = m_dfa.get_state(key)
                    break
            m_dfa.add_final_state(final_state)

        return m_dfa

if __name__ == "__main__":
    enfa = make_e_nfa()
    con = Converter()
    min = Minimizer()
    dfa = con.convert(enfa)
    print("######### e_nfa to dfa ###")
    dfa.info()
    m_dfa = min.minimize(dfa)
    print()
    print("######## dfa to m_dfa ###")
    m_dfa.info()
    accept_test(m_dfa)