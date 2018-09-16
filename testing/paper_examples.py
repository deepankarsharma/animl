import graphviz
from statsmodels.graphics.boxplots import _show_legend

from animl.trees import *
from gen_samples import *
import tempfile
from sklearn.tree import export_graphviz

parrt_article = "/Users/parrt/github/ml-articles/decision-tree-viz/images"

def viz_boston_one_feature(orientation="TD", max_depth=3, random_state=666, fancy=True):
    regr = tree.DecisionTreeRegressor(max_depth=max_depth, random_state=random_state)
    boston = load_boston()

    i = 6
    X_train = boston.data[:, i].reshape(-1, 1)
    y_train = boston.target
    regr = regr.fit(X_train, y_train)

    st = dtreeviz(regr, X_train, y_train, target_name='price',
                  feature_names=[boston.feature_names[i]], orientation=orientation,
                  fancy=fancy,
                  show_node_labels = True,
                  X=None)

    g = graphviz.Source(st)
    g.render(filename='boston-TD-AGE', directory=parrt_article, view=False, cleanup=True)
    return g

def viz_knowledge_one_feature(orientation="TD", max_depth=3, random_state=666, fancy=True):
    # data from https://archive.ics.uci.edu/ml/datasets/User+Knowledge+Modeling
    clf = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    know = pd.read_csv("data/knowledge.csv")
    target_names = ['very_low', 'Low', 'Middle', 'High']
    know['UNS'] = know['UNS'].map({n: i for i, n in enumerate(target_names)})

    the_feature = "PEG"
    X_train, y_train = know[[the_feature]], know['UNS']
    clf = clf.fit(X_train, y_train)

    X = X_train.iloc[np.random.randint(0, len(X_train))]
    X = None

    st = dtreeviz(clf, X_train, y_train, target_name='UNS',
                  feature_names=[the_feature], orientation=orientation,
                  class_names=target_names,
                  show_node_labels = True,
                  fancy=fancy,
                  X=X)
    g = graphviz.Source(st)
    g.render(filename='knowledge-TD-PEG', directory=parrt_article, view=False, cleanup=True)
    return g

g = viz_boston_one_feature(fancy=True, max_depth=3, orientation='TD')

#g = viz_knowledge_one_feature(fancy=True, orientation='TD', max_depth=3)

g.view()
