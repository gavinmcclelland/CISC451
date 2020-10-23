import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve

def plot_roc_curve(y_test, y_pred, title=None, ax=None):
    """
    Calculates and plots the ROC and corresponding AUC

    Args:
        y_test (np.array): Ground truth matrix
        y_pred (np.array): Prediction matrix
        title (string, optional): Title to display above the plot. Defaults to None.
    """
    fpr, tpr, threshold = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)
    if ax:
        if title is not None:
            ax.set_title(title)
        ax.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        ax.legend(loc = 'lower right')
        ax.plot([0, 1], [0, 1],'r--')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_ylabel('True Positive Rate')
        ax.set_xlabel('False Positive Rate')
    else:
        if title is not None:
            plt.title(title)
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()
