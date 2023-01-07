# Include your imports here, if any are used.

import math


student_name = "Divya Kumari"

# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.state_vals = {}
        for state in self.game.states: 
            self.state_vals[state] = 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        if state not in self.state_vals.keys():
            return 0
        return self.state_vals.get(state)

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        # if action is None:
        #     return None
        transitions = self.game.get_transitions(state, action)
        q_val = 0
        for state_next, prob in transitions.items():
            reward = self.game.get_reward(state, action, state_next)
            q_val += prob*(reward + (self.discount*self.get_value(state_next)))

        return q_val

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        max = -math.inf
        for action in self.game.get_actions(state):
            new_q = self.get_q_value(state, action)
            if new_q > max:
                max = new_q
                action_best = action
        return action_best

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        action_vals = dict()
        for state in self.game.states: 
            action_best = self.get_best_policy(state)
            q_val = self.get_q_value(state, action_best)
            action_vals[state] = q_val

        self.state_vals = action_vals


# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function or
    override ValueIterationAgent's methods, you can add them as well.
    """

    def __init__(self, game, discount):
        super().__init__(game, discount)
        self.policy = {}
        for state in game.states: 
            for action in game.get_actions(state):
                self.policy[state] = action
                break


    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6
        
        delta = math.inf

        while delta > epsilon:
            delta = -math.inf
            for state in self.game.states:
                action = self.policy.get(state)
                q_val = self.get_q_value(state, action)

                if abs(q_val - self.get_value(state)) > delta:
                    delta = abs(q_val - self.get_value(state))

                self.state_vals[state] = q_val

        for state in self.game.states: 
            self.policy[state] = self.get_best_policy(state)
        

# 3. Bridge Crossing Analysis
def question_3():
    discount = 0.9
    noise = 0.016
    return discount, noise

# 4. Policies
def question_4a():
    discount = 0.3
    noise = 0.01
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.3
    noise = 0.2
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.6
    noise = 0.01
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.6
    noise = 0.2
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 1.0
    noise = 0.0
    living_reward = 1.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'

# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
Policy Iteration was pretty hard to understand, but interesting to implement. 
"""

feedback_question_3 = """
Q3 and Q4 were really fun to play with, and seeing the agent "learn" was exciting!
"""
