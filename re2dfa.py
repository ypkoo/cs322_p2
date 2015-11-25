__author__ = 'koo'

from re_parser import *
from enfa2mdfa import *
import eNFA

voca = ['a', 'b', 'c', 'd', 'e', 'f', 'epsilon']
# voca = ['a', 'b', 'c', 'epsilon']

def parse_re():
    s = raw_input('re > ')   # Use raw_input on Python 2
    result = parser.parse(s)
    print result

    return result

def merge_union(dfas):
    nfa = ENFA('new')
    nfa.set_voca(voca)
    init_state = nfa.add_state("init")
    dead_state = nfa.add_state("dead_state")
    final_state = nfa.add_state("final_state")
    #init_state.set_trans_func('epsilon', [init_state])
    for v in voca:
            if v != 'epsilon':
                init_state.set_trans_func(v, [dead_state])
    for v in voca:
        dead_state.set_trans_func(v, [dead_state])
    nfa.set_init_state(init_state)

    i = 0
    init_epsilon = [init_state]
    old_to_new = {}
    new_to_old = {}

    for a in dfas:
        for s in a.get_all_states():
            if s.get_name() == "dead_state":
                old_to_new[s] = dead_state
            else:
                if s is a.get_final_states()[0]:
                    old_to_new[s] = final_state
                else:
                    state = nfa.add_state("q%d" % i)
                    i = i + 1
                    old_to_new[s] = state
                    new_to_old[state] = s

        for s in a.get_all_states():
            state = old_to_new[s]

            for v in voca:
                next = []
                snext = s.trans(v)
                for sn in snext:
                    next.append(old_to_new[sn])
                state.set_trans_func(v, next)

        init_epsilon.append(old_to_new[a.get_init_state()])

    init_state.set_trans_func('epsilon', init_epsilon)
    nfa.add_final_state(final_state)
    return nfa

def merge_star(dfas):
    nfa = dfas[0]
    init_state = nfa.get_init_state()
    final_state = nfa.get_final_states()[0]
    final_state_next = final_state.trans('epsilon')
    final_state_next.append(init_state)
    final_state.set_trans_func('epsilon', final_state_next)
    return nfa

def merge_concat(dfas):
    nfa = dfas[0]
    a = dfas[1]
    init_state = nfa.get_init_state()
    dead_state = nfa.get_state("dead_state")
    final_state = nfa.get_final_states()[0]

    i = len(nfa.get_all_states())
    old_to_new = {}
    new_to_old = {}

    for s in a.get_all_states():
        if s.get_name() == "dead_state":
            old_to_new[s] = dead_state
        else:
            state = nfa.add_state("q%d" % i)
            i = i + 1
            old_to_new[s] = state
            new_to_old[state] = s

    for s in a.get_all_states():
        state = old_to_new[s]

        for v in voca:
            next = []
            snext = s.trans(v)
            for sn in snext:
                next.append(old_to_new[sn])
            state.set_trans_func(v, next)

    init_state1 = old_to_new[a.get_init_state()]
    final_state1 = old_to_new[a.get_final_states()[0]]
    final_state_next = final_state.trans('epsilon')


    final_state_next.append(init_state1)
    #final_state.set_trans_func('epsilon', final_state_next)
    print final_state1.get_name()
    # nfa.final_states.remove(nfa.get_final_states()[0])
    # nfa.add_final_state(final_state1)

    nfa.final_states = [final_state1]


###############
    # nfa = ENFA('new')
    # nfa.set_voca(voca)
    # init_state = nfa.add_state("init")
    # dead_state = nfa.add_state("dead_state")
    # final_state = nfa.add_state("final_state")
    # for v in voca:
    #         if v != 'epsilon':
    #             init_state.set_trans_func(v, [dead_state])
    # for v in voca:
    #     dead_state.set_trans_func(v, [dead_state])
    # nfa.set_init_state(init_state)
    #
    # i = 0
    # init_epsilon = [init_state]
    # old_to_new = {}
    # new_to_old = {}
    #
    # for a in dfas:
    #     for s in a.get_all_states():
    #         if s.get_name() == "dead_state":
    #             old_to_new[s] = dead_state
    #         else:
    #             state = nfa.add_state("q%d" % i)
    #             i = i + 1
    #             old_to_new[s] = state
    #             new_to_old[state] = s
    #
    #     for s in a.get_all_states():
    #         state = old_to_new[s]
    #
    #         for v in voca:
    #             next = []
    #             snext = s.trans(v)
    #             for sn in snext:
    #                 next.append(old_to_new[sn])
    #             state.set_trans_func(v, next)
    #
    # final_state0 = old_to_new[dfas[0].get_final_states()[0]]
    # init_state1 = old_to_new[dfas[1].get_init_state()]
    # final_state1 = old_to_new[dfas[1].get_final_states()[0]]
    # final_state1_next = final_state1.trans('epsilon')
    # final_state1_next.append(final_state)
    # final_state0_next = final_state0.trans('epsilon')
    # final_state0_next.append(init_state1)
    # init_epsilon.append(old_to_new[dfas[0].get_init_state()])
    # init_state.set_trans_func('epsilon', init_epsilon)
    # nfa.add_final_state(final_state)
    return nfa


def convert_ast2dfa(ast):

    if type(ast) == str:
        if ast == '_epsilon':
            nfa = ENFA('hello')
            nfa.set_voca(voca)
            q0 = nfa.add_state("q0")
            dead_state = nfa.add_state("dead_state")

            for v in voca:
                dead_state.set_trans_func(v, [dead_state])

            for v in voca:
                if v == 'epsilon':
                    q0.set_trans_func(v, [q0])
                else:
                    q0.set_trans_func(v, [dead_state])
            nfa.set_init_state(q0)
            nfa.add_final_state(q0)

            return nfa
        else:
            nfa = ENFA('hello')
            nfa.set_voca(voca)
            nfa.add_state("q0")
            nfa.add_state("q1")
            nfa.add_state("dead_state")

            q0 = nfa.get_state("q0")
            q1 = nfa.get_state("q1")
            dead_state = nfa.get_state("dead_state")
            for v in voca:
                dead_state.set_trans_func(v, [dead_state])

            q0.set_trans_func(ast, [q1])

            for v in voca:
                if v != ast:
                    if v == 'epsilon':
                        q0.set_trans_func(v, [q0])
                    else:
                        q0.set_trans_func(v, [dead_state])
                if v == 'epsilon':
                    q1.set_trans_func(v, [q1])
                else:
                    q1.set_trans_func(v, [dead_state])

            nfa.set_init_state(q0)
            nfa.add_final_state(q1)

            return nfa
    else:
        op = ast[0]
        dfas = []

        for i in range(len(ast) - 1):
            dfas.append(convert_ast2dfa(ast[i+1]))

        if op == "+":
            nfa = merge_union(dfas)
        elif op == "*":
            nfa = merge_star(dfas)
        elif op == ".":
            nfa = merge_concat(dfas)

        return nfa




if __name__ == "__main__":
    while True:
        ast = parse_re()
        print type(ast)
        nfa = convert_ast2dfa(ast)
        con = Converter()
        min = Minimizer()
        dfa = con.convert(nfa)
        print("######### e_nfa to dfa ###")
        dfa.info()
        m_dfa = min.minimize(dfa)
        print ''
        print("######## dfa to m_dfa ###")
        m_dfa.info()
        accept_test(m_dfa)
