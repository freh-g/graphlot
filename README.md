# Graphlot


Graphlot is a library that allows to simply visualize networks. It is built upon matplotlib, and plotly and exploits network layouts from networkx, igraph and graphviz.

For this reason the first step is to install graphviz by running

```
sudo apt install graphviz

```

The library takes as input a networx graph and can plot the degree distribution and the network itself with different layouts.

To demonstrate it we will generate a random network with the function CreateNetworkFromRandomClasses(). This function takes as input a list and an integer. The list is of length n_classes and in which every value is the number of nodes of that specific classes. The integer is the number of random edges of the graph.

The function stores the information of the node belonging to a specific class in "type" node attribute and node name in "name" node attribute.

```

import graphlot as gv
import random


random.seed(123127844)

grafo = gv.CreateNetworkFromRandomClasses([10,20,30,40,50],500)
g.plot_degree_distribution_nx(grafo)

```

![Degree Distribution](https://github.com/freh-g/graphlot/images/degree_distribution.png?raw=true)



```

random.seed(123127844)
gv.visualize_network(grafo,mode = '2d',node_color_attribute='Type',legend = 'Type',cmap='viridis',annotate = 'Name')

```



![Network Visualization](https://github.com/freh-g/graphlot/images/network.png?raw=true)










