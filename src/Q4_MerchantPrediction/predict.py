
import sys
import os
import xgboost
import scipy
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def load_pred_file(pred_path):
    with open(pred_path) as in_file, \
         open(pred_path + ".tmp", 'w') as out_file:
        for line in in_file:
            out_file.write("0 ")
            out_file.write(line)

    X_test, y_test = load_svmlight_file(pred_path + ".tmp")
    os.remove(pred_path + ".tmp")
    return X_test


def train_lr(train_path, pred_path):
    print "Loading feature file ..."
    X_train, y_train = load_svmlight_file(train_path)
    X_test = load_pred_file(pred_path)

    print "Transforming data ..."
    scaler = StandardScaler(with_mean=False)
    X_full = scipy.sparse.vstack((X_train, X_test))
    Z_full = scaler.fit_transform(X_full)
    Z_train, Z_test = Z_full[:X_train.shape[0], :], Z_full[X_train.shape[0]:, :]

    print "Training model ..."
    model = LogisticRegression()
    model.fit(Z_train, y_train)

    print "Predicting..."
    y_pred_prob = model.predict_proba(Z_test)[:, 1]
    return y_pred_prob


def train_rf(train_path, pred_path):
    print "Loading feature file ..."
    X_train, y_train = load_svmlight_file(train_path)
    X_test = load_pred_file(pred_path)

    print "Training model ..."
    model = RandomForestClassifier(n_estimators=1000, n_jobs=-1)
    model.fit(X_train, y_train)

    print "Predicting..."
    y_pred = model.predict_proba(X_test)[:, 1]
    return y_pred


def train_xgboost(train_path, pred_path):
    print "Loading feature file ..."
    dtrain = xgboost.DMatrix(train_path)
    dtest = xgboost.DMatrix(pred_path)

    print "Training model ..."
    param = {
        'silent': 1,
        'eta': 0.03,
        'gamma': 0.3,
        'max_depth': 3,
        'subsample': 0.5,
        'objective': 'binary:logistic',
    }
    model = xgboost.train(param, dtrain, 1000)

    print "Predicting..."
    y_pred_prob = model.predict(dtest)
    return y_pred_prob

if __name__ == "__main__":
    train_path = sys.argv[1]
    pred_path = sys.argv[2]
    algo_type = sys.argv[3]
    print "Training model using features %s..." % train_path

    if algo_type == "xgboost":
        y_pred_prob = train_xgboost(train_path, pred_path)
    elif algo_type == "random_forest":
        y_pred_prob = train_rf(train_path, pred_path)
    else:
        print "unsupported algorithm type"
        sys.exit(-1)

    with open('predict', 'w') as out_file:
        for idx, prob in enumerate(y_pred_prob):
            out_file.write('%d %f\n' % (idx + 1, 1 - prob))
