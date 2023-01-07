import random
import math

student_name = "Divya Kumari"


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        # initialise all required variables here and also declare the q_table that stores values against state, action pairs
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.q_table = {}

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        # if state, action pair found in q_table, return it's value else return 0 if doesn't exist
        if (state, action) in self.q_table:
            return self.q_table[state, action]
        else:
            return 0

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """

        actions = self.game.get_actions(state)  #get all actions that can be performed on this state
        if len(actions) == 0:   #corner case
            return 0 

        max_val = -math.inf #initialise max value

        # for every action in actions, get the q_value and check against the max_value. If it is greater, replace max value with current q_value and return
        for action in actions:  
            q_val = self.get_q_value(state, action)
            if q_val > max_val:
                max_val = q_val
        return max_val  # TODO

    def get_best_policy(self, state):
        """Compute the best action to take in the state using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        max_val = -math.inf #initialise max value
        best_policies = []
        actions = self.game.get_actions(state)  #get all actions that can be performed on this state

        #for every action actions, get the q_value and check against max value. If it is greater, replace max value with current q_value and update best_policy
        for action in actions:
            q_val = self.get_q_value(state, action)
            if q_val > max_val:
                max_val = q_val
                best_policies = [action]
            elif q_val == max_val:  #in the case when q_value and max value are same, just add to the list of best policies
                best_policies.append(action)
        
        best_policy = random.choice(best_policies)  #pick random action incase multiple actions are present
        return best_policy

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        # update q_table with values after computing the above equation
        self.q_table[(state, action)] = (1-self.learning_rate) * self.get_q_value(state, action) + self.learning_rate * (reward + self.discount * (self.get_value(next_state)))

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """

        actions = list(self.game.get_actions(state))     #get all actions that can be performed on this state

        # for exploration probability we use random.random() and randomly choose an action. If probability for exploration is greater, act randomly or else just get best policy
        if random.random() < self.explore_prob:
            random_action = random.choice(actions)
            return random_action
        else:
            return self.get_best_policy(state)


# 3. Bridge Crossing Revisited
def question3():
    return 'NOT POSSIBLE'
    epsilon = 0.80
    learning_rate = 0.45
    return epsilon, learning_rate
    # If not possible, return 'NOT POSSIBLE'

# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        # initialise all required variables here and also declare the weight_table that stores weights against feature value
        super().__init__(*args)
        self.extractor = extractor
        self.weight_table = {}

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        # if feature found in weight_table, return it's weight else return 0 if doesn't exist
        if feature in self.weight_table:
            return self.weight_table[feature]
        else:
            return 0

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product of feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        q_val = 0   # initialise q_val
        e_items = self.extractor(state, action).items() # get all feature, weight pairs from feature extractor as a dictionary
        # for every feature weight pair, compute q_val and return
        for feature, weight in e_items:
            q_val += self.get_weight(feature) * weight

        return q_val

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        diff = (reward + (self.discount * self.get_value(next_state)) - self.get_q_value(state, action)) # calculate difference acc. to least-squares approximation
        e_items = self.extractor(state, action).items() # get all feature, weight pairs from feature extractor as a dictionary
        
         # for every feature weight pair, update weight against the feature
        for feature, weight in e_items:
            self.weight_table[feature] = self.get_weight(feature) + self.learning_rate * diff * weight


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = 5

feedback_question_2 = """
I found approx Q learning (Q5) update function a little tricky. 
I wasn't about what values to put in the formulas in the beginning considering extractor function returns features and weight 
and the formula for calculating weights for that particular feature was a little confusing. 
"""

feedback_question_3 = """
I loved working on the entire solution! I genuinely felt like I'm building something and putting theory into practice. 
"""
