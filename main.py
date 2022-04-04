# Nicholas Lormand
# njl160030
#imports
import csv
import sys


class Transition(object):
    def __init__(self):
        self.probability = 0
        self.next_state = None


class Action(object):
    def __init__(self):
        self.transition_list = []
        self.name = ''
        self.value = 0


class State(object):
    def __init__(self):
        self.name = ''
        self.action_list = []
        self.reward = 0
        self.j = 0
        self.optimal_action = None

    # Function to find max action value given a state
    def findMaxAction(self):
        value = 0.0
        # Calculates the maxarg action
        max_value = 0
        for action in self.action_list:
            if max_value == 0:
                max_value = action.value
                self.optimal_action = action
            elif max_value < action.value:
                max_value = action.value
                self.optimal_action = action

        return self.optimal_action

    def update_action_values(self):
        for action in self.action_list:
            value = 0
            for transition in action.transition_list:
                value += transition.probability * transition.next_state.j
            action.value = value

        self.optimal_action = self.action_list[0]
        for action in self.action_list:
            if action.value> self.optimal_action.value:
                self.optimal_action = action

class MDP(object):
    def __init__(self):
        self.state_list = []
        self.discount = 0
        self.num_states = 0
        self.num_actions = 0
        self.current_state = None

    def calculateJValues(self):
        """
        Function to calculate all J-Values
        :return:
        """
        # For every state in MDP state list
        for state in self.state_list:
            state.update_action_values()
        for state in self.state_list:
            state.j = state.reward + (float(self.discount) * state.findMaxAction().value)


# get args from command prompt
input_file = None
if len(sys.argv) == 5:
    num_states = sys.argv[1]
    num_actions = sys.argv[2]
    input_file = sys.argv[3]
    discount_factor = sys.argv[4]

    # turns training data into 2-D list
    with open(input_file) as f:
        reader = csv.reader(f, delimiter="\t")

        list = []
        string = ''
        for line in reader:
            list.append(line[0].rsplit('('))

    #print(list)
    mdp = MDP()
    mdp.discount = discount_factor
    mdp.num_states = num_states
    mdp.num_actions = num_actions
    for line in list:
        #print(line)
        state = State()
        for item in line:
            data = item.rsplit(')')
            #print(data)
            if data[0].find('s') == 0:
                new_data = data[0].strip().rsplit(' ')
                state.name = new_data[0]
                state.reward = float(new_data[1])
                #print('state name: %s' %(state.name))
                #print('state reward: %s' %(state.reward))
            if data[0].find('s') == 3:
                if len(state.action_list) == 0:
                    new_data = data[0].strip().rsplit(' ')
                    #print(new_data)
                    transition = Transition()
                    action = Action()
                    action.name = new_data[0]
                    transition.next_state = new_data[1]
                    transition.probability = float(new_data[2])
                    #print('    new action: %s' % action.name)
                    #print('    next state: %s' % transition.next_state)
                    #print('    transition probability: %s' % transition.probability)
                    action.transition_list.append(transition)
                    state.action_list.append(action)
                else:
                    exists = False
                    new_data = data[0].strip().rsplit(' ')
                    #print(new_data)
                    for action in state.action_list:
                        if action.name == data[0][0:2]:
                            exists = True
                            transition = Transition()
                            transition.next_state = new_data[1]
                            transition.probability = float(new_data[2])
                            #print('    existing action: %s' % action.name)
                            #print('    next state: %s' % transition.next_state)
                            #print('    transition probability: %s' % transition.probability)
                            action.transition_list.append(transition)
                    if not exists:
                        transition = Transition()
                        action = Action()
                        action.name = new_data[0]
                        transition.next_state = new_data[1]
                        transition.probability = float(new_data[2])
                        #print('    new action: %s' % action.name)
                        #print('    next state: %s' % transition.next_state)
                        #print('    transition probability: %s' % transition.probability)
                        action.transition_list.append(transition)
                        state.action_list.append(action)
        mdp.state_list.append(state)
    for state in mdp.state_list:
        for action in state.action_list:
            # change values from string to object
            for transition in action.transition_list:
                for x in mdp.state_list:
                    if transition.next_state == x.name:
                        transition.next_state = x

    count = 1
    while count <=20:
        mdp.calculateJValues()
        print('After iteration %s:  ' %count)
        for state in mdp.state_list:
            print('(%s %s %s) ' %(state.name, state.optimal_action.name, round(state.j, 4))
                  , end = '')
        count +=1
        print('\n')

else:
    string1 = 'Incorrect Input: : (1) the number of states of the MDP '
    string2 = '(2) the number of possible actions, '
    string3 = '(3) the input file as described above, '
    string4 = 'and (4) the discount factor (γ).'
    print('%s%s%s%s' %(string1, string2, string3, string4))


