############################################################
# CIS 521: Perceptrons Homework
############################################################

student_name = "Divya Kumari"

############################################################
# Imports
############################################################

# import perceptrons_data as data

# Include your imports here, if any are used.
import math


############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):

        self.weights = dict()
        for i in range(iterations):
            for x, y in examples:
                dotProduct = 0
                for label in x:
                    if label not in self.weights:
                        self.weights[label] = 0
                    dotProduct = dotProduct + self.weights[label] * x[label]
                if dotProduct > 0 and y == False:
                    for label in x:
                        self.weights[label] = self.weights[label] - x[label]
                if dotProduct <= 0 and y == True:
                    for label in x:
                        self.weights[label] = self.weights[label] + x[label]


    def predict(self, x):

        dotProduct = 0
        for label in x:
            if label not in self.weights:
                self.weights[label] = 0
            dotProduct = dotProduct + self.weights[label] * x[label]

        if dotProduct > 0:
            return True
        else:
            return False
            

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):

        self.weights = dict()
        for i in range(iterations):
            for x, y in examples:
                if y not in self.weights:
                    self.weights[y] = {}
                maxDotProduct = -math.inf
                for key in self.weights:
                    dotProduct = 0
                    for label in x:
                        if label not in self.weights[key]:
                            self.weights[key][label]=0
                        dotProduct = dotProduct + self.weights[key][label] * x[label]
                    if maxDotProduct < dotProduct:
                        maxDotProduct = dotProduct
                        predicateLabel = key
                if predicateLabel != y:
                    for label in x:
                        self.weights[y][label] = self.weights[y][label] + x[label]
                        self.weights[predicateLabel][label] = self.weights[predicateLabel][label] - x[label]


    def predict(self, x):
        maxDotProduct = -math.inf
        for key in self.weights:
            dotProduct = 0
            for label in x:
                if label not in self.weights[key]:
                    self.weights[key][label] = 0
                dotProduct = dotProduct + x[label] * self.weights[key][label]
            if maxDotProduct < dotProduct:
                maxDotProduct = dotProduct
                predicateLabel = key

        return predicateLabel

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        iterations = 40
        samples = []
        for measure, species in data:
            dataDict = dict()
            for i in range(4):
                dataDict["x"+ str(i)] = measure[i]
            samples.append((dataDict, species))

        self.perceptron = MulticlassPerceptron(samples,iterations)

    def classify(self, instance):
        dataDict = dict()
        for i in range(4):
            dataDict["x"+ str(i)] = instance[i]

        prediction = self.perceptron.predict(dataDict)
            
        return prediction

class DigitClassifier(object):

    def __init__(self, data):
        iterations = 9
        samples = []
        for pixels, label in data:
            dataDict = dict()
            for i in range(64):
                dataDict["x"+ str(i)] = pixels[i]
            samples.append((dataDict, label))

        self.perceptron = MulticlassPerceptron(samples,iterations)

    def classify(self, instance):
        dataDict = dict()
        for i in range(64):
            dataDict["x"+ str(i)] = instance[i]
            
        prediction = self.perceptron.predict(dataDict)
            
        return prediction

class BiasClassifier(object):

    def __init__(self, data):
        iterations = 5
        samples = []
        for realNum, binaryLabel in data:
            dataDict = dict()
            dataDict["x1"] = realNum - 1
            samples.append((dataDict, binaryLabel))

        self.perceptron = BinaryPerceptron(samples,iterations)

    def classify(self, instance):
        dataDict = dict()
        dataDict["x1"] = instance - 1
       
        prediction = self.perceptron.predict(dataDict)
            
        return prediction

class MysteryClassifier1(object):

    def __init__(self, data):
        iterations = 5
        samples = []
        for realNum, binaryLabel in data:
            dataDict = dict()
            dataDict["x1"] = (realNum[0] ** 2 + realNum[1] ** 2) - 5
            samples.append((dataDict, binaryLabel))

        self.perceptron = BinaryPerceptron(samples,iterations)

    def classify(self, instance):
        dataDict = dict()
        dataDict["x1"] = (instance[0] ** 2 + instance[1] ** 2) - 5
    
        prediction = self.perceptron.predict(dataDict)
            
        return prediction

class MysteryClassifier2(object):

    def __init__(self, data):
            iterations = 5
            samples = []
            for realNum, binaryLabel in data:
                dataDict = dict()
                dataDict["x1"] = (realNum[0] * realNum[1] * realNum[2])
                samples.append((dataDict, binaryLabel))

            self.perceptron = BinaryPerceptron(samples,iterations)

    def classify(self, instance):
            dataDict = dict()
            dataDict["x1"] = (instance[0] * instance[1] * instance[2])
        
            prediction = self.perceptron.predict(dataDict)
                
            return prediction

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = 10

feedback_question_2 = """
The most challenging aspect for me was visualizing the dataset of mystery classifiers and understanding the activation functions.
"""

feedback_question_3 = """
I really enjoyed implementing the applications part of the homework where you see the perceptron models working against different samples. 
"""
