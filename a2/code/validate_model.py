from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from plot_roc_curve import plot_roc_curve
from make_confusion_matrix import make_confusion_matrix

def validate_model(model, x_train, y_train, model_name, cv=10, group_names=None, categories='auto', roc=True):
    """
    Trains and validates, using k-fold cross validation, the given model using the supplied data sets.
    Creates and displays confusion matrix with calculated metrics, as well as a plot of the ROC.

    Args:
        model (sklearn.model): A scikit learn model object
        x_train (np.array): feature matrix to use for training/validation
        y_train (np.array): label matrix to use for training/validation
        model_name (string): the name of the model for use in plot titles
        cv (int, optional): Number of folds for cross validation. Defaults to 10.
        group_names:   List of strings that represent the labels row by row to be shown in each square.
        categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    """
    if cv:
        y_pred = cross_val_predict(model, x_train, y_train, n_jobs=-1, cv=cv)
    else:
        y_pred = model.fit(x_train, y_train)
    conf_matrix = confusion_matrix(y_train, y_pred)
    if roc:
        fig, (ax1, ax2) =  plt.subplots(1, 2, figsize=(13, 5))
        make_confusion_matrix(conf_matrix, group_names, categories, title=f'{model_name} Confusion Matrix', ax=ax1)
        plot_roc_curve(y_train, y_pred, title=f'{model_name} ROC', ax=ax2)
    else:
        fig, (ax1) =  plt.subplots(1, 1, figsize=(6, 5))
        make_confusion_matrix(conf_matrix, group_names, categories, title=f'{model_name} Confusion Matrix', ax=ax1)
