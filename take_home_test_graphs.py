import pydot

binomial_tree_prices_x = pydot.Dot(graph_type="digraph", rankdir="LR")
# Level zero
binomial_tree_prices_x.add_node(pydot.Node("X_Y(0)", label="<X<SUB>Y</SUB>(0) = 4>"))

# Level one
binomial_tree_prices_x.add_node(
    pydot.Node("X_Y(1,H)", label="<X<SUB>Y</SUB>(1,H) = 8>")
)
binomial_tree_prices_x.add_node(
    pydot.Node("X_Y(1,T)", label="<X<SUB>Y</SUB>(1,H) = 2>")
)
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(0)", "X_Y(1,H)",label = "1/3"))
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(0)", "X_Y(1,T)",label = "2/3"))

# Level two
binomial_tree_prices_x.add_node(
    pydot.Node("X_Y(2,HH)", label="<X<SUB>Y</SUB>(2,HH) = 16>")
)
binomial_tree_prices_x.add_node(
    pydot.Node("X_Y(2,HT)", label="<X<SUB>Y</SUB>(2,TH) = 4>")
)
binomial_tree_prices_x.add_node(
    pydot.Node("X_Y(2,TT)", label="<X<SUB>Y</SUB>(2,TT) = 1>")
)
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(1,H)", "X_Y(2,HH)",label = "1/3"))
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(1,H)", "X_Y(2,HT)",label = "2/3"))
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(1,T)", "X_Y(2,HT)",label = "1/3"))
binomial_tree_prices_x.add_edge(pydot.Edge("X_Y(1,T)", "X_Y(2,TT)",label = "2/3"))


binomial_tree_prices_v = pydot.Dot(graph_type="digraph", rankdir="LR")
# Level zero
binomial_tree_prices_v.add_node(pydot.Node("V_Y(0)", label="<V<SUB>Y</SUB>(0) = 5/9>"))

# Level one
binomial_tree_prices_v.add_node(
    pydot.Node("V_Y(1,H)", label="<V<SUB>Y</SUB>(1,H) = 1/3>")
)
binomial_tree_prices_v.add_node(
    pydot.Node("V_Y(1,T)", label="<V<SUB>Y</SUB>(1,H) = 2/3>")
)
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(0)", "V_Y(1,H)",label = "1/3"))
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(0)", "V_Y(1,T)",label = "2/3"))

# Level two
binomial_tree_prices_v.add_node(
    pydot.Node("V_Y(2,HH)", label="<V<SUB>Y</SUB>(2,HH) = 1>")
)
binomial_tree_prices_v.add_node(
    pydot.Node("V_Y(2,HT)", label="<V<SUB>Y</SUB>(2,TH) = 0>")
)
binomial_tree_prices_v.add_node(
    pydot.Node("V_Y(2,TT)", label="<V<SUB>Y</SUB>(2,TT) = 1>")
)
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(1,H)", "V_Y(2,HH)",label = "1/3"))
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(1,H)", "V_Y(2,HT)",label = "2/3"))
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(1,T)", "V_Y(2,HT)",label = "1/3"))
binomial_tree_prices_v.add_edge(pydot.Edge("V_Y(1,T)", "V_Y(2,TT)",label = "1/3"))
