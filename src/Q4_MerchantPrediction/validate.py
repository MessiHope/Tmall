import sys
import xgboost
import scipy
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_svmlight_file
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn import metrics


def xgboost_model(X_train, X_valid, y_train):
    dtrain = xgboost.DMatrix(X_train, y_train)
    dvalid = xgboost.DMatrix(X_valid)
    param = {
        'silent': 1,
        'eta': 0.03,
        'max_depth': 3,
        'gamma': 0.3,
        'subsample': 0.1,
        'objective': 'binary:logistic',
    }
    model = xgboost.train(param, dtrain, 1000)
    y_pred_prob = model.predict(dvalid)
    return model, y_pred_prob

def LR_model(X_train, X_valid, y_train):
    scaler = StandardScaler(with_mean=False)
    X_full = scipy.sparse.vstack((X_train, X_valid))
    Z_full = scaler.fit_transform(X_full)
    Z_train, Z_valid = Z_full[:X_train.shape[0], :], Z_full[X_train.shape[0]:, :]
    model = LogisticRegression(class_weight='balanced')
    model.fit(Z_train, y_train)
    y_pred_prob = model.predict_proba(Z_valid)[:, 1]
    return model, y_pred_prob

def RF_model(X_train, X_valid, y_train):
    model = RandomForestClassifier(n_estimators=1000, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred_prob = model.predict_proba(X_valid)[:, 1]
    return model, y_pred_prob

def print_fimportance(model):
    with open(in_path.split(".csv")[0] + "_column_names") as name_file:
        feature_names = [line.strip() for line in name_file]
    if type(model) is xgboost.Booster:
        l = sorted(model.get_score(importance_type='weight').items(), key=lambda x: -x[1])
        l = [(feature_names[int(item[0][1:])], item[1]) for item in l]
        print 'Weight:', l
        l = sorted(model.get_score(importance_type='gain').items(), key=lambda x: -x[1])
        l = [(feature_names[int(item[0][1:])], item[1]) for item in l]
        print 'Gain:', l
        l = sorted(model.get_score(importance_type='cover').items(), key=lambda x: -x[1])
        l = [(feature_names[int(item[0][1:])], item[1]) for item in l]
        print 'Cover:', l
    elif type(model) is LogisticRegression:
        weight = model.coef_[0, :]
        l = zip(feature_names, weight)
        l = sorted(l, key=lambda x: -x[1])
        print l
    elif type(model) is RandomForestClassifier():
        print "No feature importance in Random Forest"

def ensemble_model(y_pred_prob_xg,y_pred_prob_LR,y_pred_prob_RF):
    y_pred_prob = []
    for a,b,c in zip(y_pred_prob_xg,y_pred_prob_LR,y_pred_prob_RF):
        y_pred_prob.append((a+b+c)/3.0)
    return y_pred_prob

def choose_best_threshold(y_valid,y_pred_prob):
    print "choose best threshold ..."
    best_F, best_P, best_R, best_threshold = 0, 0, 0, 0
    print "threshold\tPrecision\tRecall\tACC"
    for threshold in np.linspace(.1, .9, 20):
        y_pred = np.zeros(len(y_valid))
        y_pred[y_pred_prob > threshold] = 1

        y_valid_change = np.absolute(y_valid - 1)
        y_pred = np.absolute(y_pred - 1)
        ACC = accuracy_score(y_valid_change, y_pred)
        P = precision_score(y_valid_change, y_pred)
        R = recall_score(y_valid_change, y_pred)
        F = 5 * P * R / (2 * P + 3 * R)
        print "%f\t%f\t%f\t%f" % (threshold, P, R, ACC)
        if F > best_F:
            best_F = F
            best_P = P
            best_R = R
            best_threshold = threshold
    print "best threshold %f, P %f, R %f, ACC %f" % (best_threshold, best_P, best_R, ACC)
    return best_threshold
import os
if __name__ == "__main__":
    # in_path = sys.argv[1]
    pre_path = os.path.dirname(os.getcwd())
    ##  prepare data
    in_path = pre_path + "/../data/features.csv"
    print "Training model using features file %s..." % in_path

    print "Loading feature file ..."
    X, y = load_svmlight_file(in_path)
    id_list = np.arange(len(y)) + 1

    print "Random split validation data ..."
    X_train, X_valid, y_train, y_valid, id_train, id_valid = \
            train_test_split(X, y, id_list, test_size=.6)

    print "Training model ..."
    # Model 1: xgboost
    model_xg, y_pred_prob_xg = xgboost_model(X_train, X_valid, y_train)

    # Model 2: Logistic Regression
    model_LR, y_pred_prob_LR = LR_model(X_train, X_valid, y_train)

    # Model 3: Random Forest
    model_RF, y_pred_prob_RF = RF_model(X_train, X_valid, y_train)

    ##  ensemble models
    y_pred_prob = ensemble_model(y_pred_prob_xg, y_pred_prob_LR, y_pred_prob_RF)

    best_threshold_xg =  choose_best_threshold(y_valid, y_pred_prob_xg)
    best_threshold_LR =  choose_best_threshold(y_valid, y_pred_prob_LR)
    best_threshold_RF =  choose_best_threshold(y_valid, y_pred_prob_RF)
    best_threshold =  choose_best_threshold(y_valid, y_pred_prob)

    print "Wrong result:"
    N_test = len(id_valid)
    y_pred = np.zeros(len(y_pred_prob))
    y_pred[y_pred_prob > best_threshold] = 1
    wr = [(id_valid[i], y_valid[i], y_pred_prob[i])
        for i in range(N_test) if y_valid[i] != y_pred[i]]
    wr = sorted(wr, key=lambda x: x[0])
    for x in wr:
        print "\t id %d, label %d, P[y=1] %f" % (x[0], x[1], x[2])
    num_correct = np.sum(y_valid == y_pred)
    acc = 1.0 * num_correct / len(y_valid)

    print "acc: %f, num_wrong: %d" % (acc, len(y_valid) - num_correct)

    print "Feature importance xgboost:"
    print_fimportance(model_xg)

    print "Feature importance LR:"
    print_fimportance(model_LR)

    print "Feature importance RF:"
    print_fimportance(model_RF)

    test_auc_xg = metrics.roc_auc_score(y_valid, y_pred_prob_xg)
    print "test accuracy xgboost: ",test_auc_xg

    test_auc_LR = metrics.roc_auc_score(y_valid, y_pred_prob_LR)
    print "test accuracy Logistic Regression: ", test_auc_LR

    test_auc_RF = metrics.roc_auc_score(y_valid, y_pred_prob_RF)
    print "test accuracy Random Forest: ", test_auc_RF

    test_auc = metrics.roc_auc_score(y_valid, y_pred_prob)
    print "test accuracy ensemble: ", test_auc

