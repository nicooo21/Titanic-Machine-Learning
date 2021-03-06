"""
Author      : Yi-Chieh Wu, Sriram Sankararaman
Description : Titanic
"""

# Use only the provided packages!
import math
import csv
from util import *
import numpy as np
from collections import Counter

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

######################################################################
# classes
######################################################################

class Classifier(object) :
    """
    Classifier interface.
    """
    
    def fit(self, X, y):
        raise NotImplementedError()
        
    def predict(self, X):
        raise NotImplementedError()


class MajorityVoteClassifier(Classifier) :
    
    def __init__(self) :
        """
        A classifier that always predicts the majority class.
        
        Attributes
        --------------------
            prediction_ -- majority class
        """
        self.prediction_ = None
    
    def fit(self, X, y) :
        """
        Build a majority vote classifier from the training set (X, y).
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes
        
        Returns
        --------------------
            self -- an instance of self
        """
        majority_val = Counter(y).most_common(1)[0][0]
        self.prediction_ = majority_val
        return self
    
    def predict(self, X) :
        """
        Predict class values.
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
        
        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.prediction_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")
        
        n,d = X.shape
        y = [self.prediction_] * n 
        return y


class RandomClassifier(Classifier) :
    
    def __init__(self) :
        """
        A classifier that predicts according to the distribution of the classes.
        
        Attributes
        --------------------
            probabilities_ -- class distribution dict (key = class, val = probability of class)
        """
        self.probabilities_ = {}
    
    def fit(self, X, y) :
        """
        Build a random classifier from the training set (X, y).
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes
        
        Returns
        --------------------
            self -- an instance of self
        """
        
        ### ========== TODO : START ========== ###
        # part b: set self.probabilities_ according to the training set
        
        # Gets distribution of classes
        distribution = Counter(y).most_common(2)
        
        # size of examples
        n,d = X.shape


        # appends to dictionary with key = class and val = probability of class
        for i in range(len(distribution)):
            self.probabilities_[distribution[i][0]] = float(distribution[i][1])/float(n)

        # prints distribution array
        print self.probabilities_
        ### ========== TODO : END ========== ###
        
        return self
    
    def predict(self, X, seed=1234) :
        """
        Predict class values.
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            seed -- integer, random seed
        
        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.probabilities_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")
        np.random.seed(seed)
        
        ### ========== TODO : START ========== ###
        # part b: predict the class for each test example
        # hint: use np.random.choice (be careful of the parameters)

        # gets X parameters
        n,d = X.shape

        # Gets keys and values from probabilities dict
        probabilities_keys = self.probabilities_.keys()
        probabilities_vals = self.probabilities_.values()
        
        # Creates array of estimates
        print("Initializing predictions...")
        y = np.random.choice(probabilities_keys, n, True, probabilities_vals)
        ### ========== TODO : END ========== ###
        
        return y


######################################################################
# functions
######################################################################
# Function to get error of knn classifier
def error_knnclassifier(neighbors, X, y) :
    print("Initializing KNeighborsClassifier with %d neighbors" % neighbors)
    knnClf = KNeighborsClassifier(n_neighbors=neighbors)

    print("Fitting model...")
    knnClf.fit(X, y)

    print("Making array of predictions...")
    y_pred = knnClf.predict(X)

    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)


def plot_histograms(X, y, Xnames, yname) :
    n,d = X.shape  # n = number of examples, d =  number of features
    fig = plt.figure(figsize=(20,15))
    nrow = 3; ncol = 3
    for i in range(d) :
        fig.add_subplot (3,3,i)  
        data, bins, align, labels = plot_histogram(X[:,i], y, Xname=Xnames[i], yname=yname, show = False)
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xnames[i])
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')
 
    plt.savefig ('histograms.pdf')


def plot_histogram(X, y, Xname, yname, show = True) :
    """
    Plots histogram of values in X grouped by y.
    
    Parameters
    --------------------
        X     -- numpy array of shape (n,d), feature values
        y     -- numpy array of shape (n,), target classes
        Xname -- string, name of feature
        yname -- string, name of target
    """
    
    # set up data for plotting
    targets = sorted(set(y))
    data = []; labels = []
    for target in targets :
        features = [X[i] for i in range(len(y)) if y[i] == target]
        data.append(features)
        labels.append('%s = %s' % (yname, target))
    
    # set up histogram bins
    features = set(X)
    nfeatures = len(features)
    test_range = list(range(int(math.floor(min(features))), int(math.ceil(max(features)))+1))
    if nfeatures < 10 and sorted(features) == test_range:
        bins = test_range + [test_range[-1] + 1] # add last bin
        align = 'left'
    else :
        bins = 10
        align = 'mid'
    
    # plot
    if show == True:
        plt.figure()
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xname)
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')
        plt.show()

    return data, bins, align, labels


def error(clf, X, y, ntrials=100, test_size=0.2) :
    """
    Computes the classifier error over a random split of the data,
    averaged over ntrials runs.
    
    Parameters
    --------------------
        clf         -- classifier
        X           -- numpy array of shape (n,d), features values
        y           -- numpy array of shape (n,), target classes
        ntrials     -- integer, number of trials
    
    Returns
    --------------------
        train_error -- float, training error
        test_error  -- float, test error
    """
    
    ### ========== TODO : START ========== ###
    # compute cross-validation error over ntrials
    # hint: use train_test_split (be careful of the parameters)
    
    train_error = 0
    test_error = 0 
    train_error_total = 0
    test_error_total = 0   

    for x in range(0, ntrials):
        
        print("Splitting test and training data for trial %d..." % (x))
    
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = x)
    
        print("Fitting data to model...")

        
        clf.fit(X_train, y_train)

        # Predicting Training Data

        y_pred = clf.predict(X_train)

        train_error = (1 - metrics.accuracy_score(y_train, y_pred, normalize=True))

        # Predicting Test Data

        y_pred = clf.predict(X_test)

        test_error = (1 - metrics.accuracy_score(y_test, y_pred, normalize=True))

        print("Train Error: %.3f\nTest Error: %.3f" % (train_error, test_error))

        train_error_total += train_error
        test_error_total += test_error


        
    ### ========== TODO : END ========== ###
    
    return train_error_total/float(100), test_error_total/float(100)


def write_predictions(y_pred, filename, yname=None) :
    """Write out predictions to csv file."""
    out = open(filename, 'wb')
    f = csv.writer(out)
    if yname :
        f.writerow([yname])
    f.writerows(list(zip(y_pred)))
    out.close()


######################################################################
# main
######################################################################

def main():
    # load Titanic dataset
    titanic = load_data("titanic_train.csv", header=1, predict_col=0)
    X = titanic.X; Xnames = titanic.Xnames
    y = titanic.y; yname = titanic.yname
    n,d = X.shape  # n = number of examples, d =  number of features

    #========================================
    # part a: plot histograms of each feature
    '''
    print('Plotting...')
    for i in range(d) :
        plot_histogram(X[:,i], y, Xname=Xnames[i], yname=yname)
    '''
       
    #========================================
    # train Majority Vote classifier on data
    print('Classifying using Majority Vote...')
    clf = MajorityVoteClassifier() # create MajorityVote classifier, which includes all model parameters
    clf.fit(X, y)                  # fit training data using the classifier
    y_pred = clf.predict(X)        # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)
    
    
    
    ### ========== TODO : START ========== ###
    # part b: evaluate training error of Random classifier
    print('Classifying using Random...')
    ranClf = RandomClassifier()
    ranClf.fit(X,y)
    y_pred = ranClf.predict(X)
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part c: evaluate training error of Decision Tree classifier
    # use criterion of "entropy" for Information gain 
    print('Classifying using Decision Tree...')
    
    print("Initializing DecisionTreeClassifier...")
    decisionClf = DecisionTreeClassifier(criterion="entropy")

    print("Fitting DecisionTreeClassifier...")
    decisionClf.fit(X, y)

    print("Predicting...")
    y_pred = decisionClf.predict(X)

    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)

    ### ========== TODO : END ========== ###

    

    # note: uncomment out the following lines to output the Decision Tree graph
    
    # save the classifier -- requires GraphViz and pydot
    '''
    import StringIO, pydot
    from sklearn import tree
    dot_data = StringIO.StringIO()
    tree.export_graphviz(decisionClf, out_file=dot_data,
                         feature_names=Xnames)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph[0].write_pdf("dtree.pdf") 
    '''

    ### ========== TODO : START ========== ###
    # part d: evaluate training error of k-Nearest Neighbors classifier
    # use k = 3, 5, 7 for n_neighbors 
    print('Classifying using k-Nearest Neighbors...')

    print("Evaluating for k = 3")
    error_knnclassifier(3, X, y)
   
    print("Evaluating for k = 5")
    error_knnclassifier(5, X, y)

    print("Evaluating for k = 7")
    error_knnclassifier(7, X, y)


    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part e: use cross-validation to compute average training and test error of classifiers
    print('Investigating various classifiers...')
    print("Investigating MajorityClassifier...\n====================================\n==================================")
    training_error, test_error = error(clf, X, y)
    print("Training Error Average: %.3f\nTesting Error Average: %.3f" %(training_error, test_error))
    print("=====================================\n=====================================")
    print("Investigating RandomClassifier...\n====================================\n==================================")
    training_error, test_error = error(ranClf, X, y)
    print("Training Error Average: %.3f\nTesting Error Average: %.3f" %(training_error, test_error))
    print("=====================================\n=====================================")
    print("Investigating DecisionTreeClassifier...\n====================================\n==================================")
    training_error, test_error = error(decisionClf, X, y)
    print("Training Error Average: %.3f\nTesting Error Average: %.3f" %(training_error, test_error))
    print("=====================================\n=====================================")
    print("Investigating KNNeighborsClassifier...\n====================================\n==================================")
    knnClf = KNeighborsClassifier(5)
    training_error, test_error = error(knnClf, X, y)
    print("Training Error Average: %.3f\nTesting Error Average: %.3f" %(training_error, test_error))
    ### ========== TODO : END ========== ###



    ### ========== TODO : START ========== ###
    # part f: use 10-fold cross-validation to find the best value of k for k-Nearest Neighbors classifier
    print('Finding the best k for KNeighbors classifier...')

    # Create list of x values signifying neighbors
    xNums = list(range(1, 51))
    yNums = []

    print("Computing 10 fold cross-validation scores...")
    # gets 10 fold cross-validation scores for k = 1 to 50
    for x in range(1, 51):
        knnClf = KNeighborsClassifier(x)
        yNums.append(1-(sum(cross_val_score(knnClf, X, y, cv = 10, scoring="accuracy"))/10))
        
    # Plotting Commands
    print("Plotting Validation Score Error vs. k Neighbors...")
    plt.scatter(xNums, yNums, c='b', marker='x')
    plt.xlabel("k neighbors")
    plt.ylabel("Validation Score Error")
    plt.title("Validation Score Error vs k Neighbors")
    plt.show()
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part g: investigate decision tree classifier with various depths
    print('Investigating depths...')
    print("Computing 10 fold cross-validation scores...")
    # gets 10 fold cross-validation scores for depth = 1 to 20
    
    yCrossVal = []
    yTrainingError = []
    yTestingError = []
    
    for x in range(1, 21):
        decisionClf = DecisionTreeClassifier(criterion="entropy", max_depth=x)
        yCrossVal.append(1-(sum(cross_val_score(decisionClf, X, y, cv = 10, scoring="accuracy"))/float(10)))
        temp_train, temp_test = error(decisionClf, X, y)
        yTrainingError.append(temp_train)
        yTestingError.append(temp_test) 
    
    # plotting Cross Val Score Error vs. max depth
    xNums = list(range(1, 21))
    plt.plot(xNums, yCrossVal, label = "Cross Validation Error")
    plt.plot(xNums, yTrainingError, label = "Training Error")
    plt.plot(xNums, yTestingError, label = "Testing Error")
    plt.xlabel("Max Depth")
    plt.ylabel("Error")
    plt.title("Error Comparison vs. Max Depth")
    plt.legend()
    plt.show()
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part h: investigate Decision Tree and k-Nearest Neighbors classifier with various training set sizes
    print('Investigating training set sizes...')
    print("Splitting Data...")

    # Set up data
    k = 7
    depth = 3
    x_vals = np.arange(0.1, 1.1, 0.1)
    training_error_knn = []
    testing_error_knn = []
    training_error_dec = []
    testing_error_dec = []

    # set up classifiers
    knnClf = KNeighborsClassifier(n_neighbors=k)
    decisionClf = DecisionTreeClassifier(criterion="entropy", max_depth=depth)

    # split data into 0.1 test, 0.9 train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 1)

    # range from 0.1 of training data to 1 times it
    for i in range(1, 11):
        # split by i * .14
        test_percentage = -1
        if i < 10:
            test_percentage = 0.1 * i
        else:
            test_percentage = 1
            
        print ("Running test with %.3f percent of training data" % test_percentage)

        train_error_knn_total = 0
        test_error_knn_total = 0
        train_error_dec_total = 0
        test_error_dec_total = 0

        for x in range(1, 101):
            X_train_split, X_test_dont_use, y_train_split, y_test_dont_use = train_test_split(X_train, y_train, test_size = 1 - test_percentage, random_state = x)
        
            # fit knn classifier
            knnClf.fit(X_train_split, y_train_split)

            # training error with knn classifier
            y_pred = knnClf.predict(X_train_split)

            train_error_knn_total += (1 - metrics.accuracy_score(y_train_split, y_pred, normalize=True))
        
            # testing error with knn classifier
            y_pred = knnClf.predict(X_test)

            test_error_knn_total += (1 - metrics.accuracy_score(y_test, y_pred, normalize=True))

            # fit dec classifier
            decisionClf.fit(X_train_split, y_train_split)

            # training error with knn classifier
            y_pred = decisionClf.predict(X_train_split)

            train_error_dec_total += (1 - metrics.accuracy_score(y_train_split, y_pred, normalize=True))
        
            # testing error with knn classifier
            y_pred = decisionClf.predict(X_test)

            test_error_dec_total += (1 - metrics.accuracy_score(y_test, y_pred, normalize=True))
        
        training_error_knn.append(train_error_knn_total/100)
        testing_error_knn.append(test_error_knn_total/100)
        training_error_dec.append(train_error_dec_total/100)
        testing_error_dec.append(test_error_dec_total/100)

    plt.scatter(x_vals, training_error_knn, label = "Training Error KNN", c = 'r')
    plt.scatter(x_vals, testing_error_knn, label = "Testing Error KNN", c = 'y')
    plt.scatter(x_vals, training_error_dec, label = "Training Error Decision", c = 'g')
    plt.scatter(x_vals, testing_error_dec, label = "Testing Error Decision", c = 'b')
    plt.xlabel("Percentage of Training Data Used")
    plt.ylabel("Error")
    plt.title("Error vs. Percentage of Training Data Used")
    plt.legend()
    plt.show()
    
    ### ========== TODO : END ========== ###
    
       
    print('Done')


if __name__ == "__main__":
    main()
