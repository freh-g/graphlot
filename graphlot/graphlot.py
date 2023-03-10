import networkx as nx
from collections import Counter
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import random 
import textalloc as ta
import plotly.graph_objs as go



def CreateNetworkFromRandomClasses(n_of_class_nodes, n_edges):
    Net=nx.Graph()
    net_data=list(zip([f'Class{i}' for i in range(len(n_of_class_nodes))],[n for n in n_of_class_nodes]))
    i=0
    for d in net_data:
        for step in range(d[1]):
            Net.add_node(i,Type=d[0],Name='node_'+str(i))
            i+=1
    nod=list(Net.nodes())
    edges=[random.sample(nod,2) for _ in range(n_edges)]


    Net.add_edges_from(edges)
    
    return Net








def visualize_network(G,layout='auto',figure_size=(15,10),figure_title='',mode='2d',
                      node_color_attribute=False, cmap = "viridis" ,edge_color_attribute=False,annotate = False,
                      node_shape = 'o', node_size=100, node_alpha=1,node_outline='black',
                      edge_linewidth=0.5,edge_alpha=0.5,edge_color='black',
                      annotation_arrows = False, text_size = 10, text_color = 'black', text_margin = 0.01, 
                      text_min_distance = 0.015, text_max_distance = 0.07,
                      save=False,legend=False):
    
    #UPGRADE THE DICTIONARIES ===============================================================================================================

    if mode=='2d':
        #LAYOUTS ========================================================================================================================
        
        if layout == 'auto':
            iG=ig.Graph.from_networkx(G)
            my_layout=iG.layout_auto()
            sources = iG.get_edge_dataframe()['source'].map(iG.get_vertex_dataframe()._nx_name)
            targets = iG.get_edge_dataframe()['target'].map(iG.get_vertex_dataframe()._nx_name)
            node_coordinates=dict(enumerate(my_layout.coords))
        elif layout == 'spring':
            node_coordinates=nx.spring_layout(G)
        elif layout == 'circular':
            node_coordinates=nx.circular_layout(G)
        elif layout== 'spectral':
            node_coordinates=nx.spectral_layout(G)
        elif layout == 'hierarchical':
            node_coordinates = nx.drawing.nx_agraph.graphviz_layout(G, prog = 'dot')

        
        sources = [s[0] for s in G.edges()]
        targets = [s[1] for s in G.edges()]
        
        edges_coordinates=[]
        for edge in list(zip(sources,targets)):
            edges_coordinates.append(list(map(node_coordinates.get,edge)))


        # BUILD THE FIGURE ========================================================================================================================
        fig,ax=plt.subplots(figsize=figure_size) 
        
        # EDGES ========================================================================================================================
        
        for point in edges_coordinates:
            ax.plot((point[0][0],point[1][0]),(point[0][1],point[1][1]),
                    color=edge_color,
                    linewidth=edge_linewidth,
                    alpha=edge_alpha,
                    zorder=0)

        
        #NODES ========================================================================================================================
        
        if node_color_attribute:
            
            NodeClasses=[n[1][node_color_attribute] for n in G.nodes(data=True)]
            N = len(set(NodeClasses))
            Cdict=dict(zip(set(NodeClasses),[n for n in range(N)]))
            NodeColors = list(map(Cdict.get,NodeClasses))

            colors  = [f"C{i}" for i in np.arange(1, max(NodeColors)+1)]
#             cmap, norm = matplotlib.colors.from_levels_and_colors(np.arange(1, max(NodeColors)+2), colors)

        else:
            N = len(G.nodes)
            NodeColors = [0 for n in range(N)]
            colors  = [f"C{i}" for i in np.arange(1, max(NodeColors)+1)]
#             cmap, norm = None,None

        
        
        
        xses=[x[0] for x in node_coordinates.values()]
        yses=[y[1] for y in node_coordinates.values()]
        
        
        
        
        scatter=ax.scatter(xses,
                yses, 
                alpha=node_alpha ,
                edgecolors=node_outline,
                marker = node_shape,
                c=NodeColors,
                zorder=1,
                s=node_size,
                cmap=cmap)
        lab=[]
        if annotate:
            
            lab=[n[1][annotate] for n in G.nodes(data=True)]
            ta.allocate_text(fig,
                            ax,
                            xses,
                            yses,
                            lab,
                            draw_lines=annotation_arrows,
                            textsize = text_size,
                            textcolor = text_color,
                            margin = text_margin,
                            min_distance = text_min_distance,
                            max_distance = text_max_distance
                            )
        if legend:
            
            lab=[n[1][legend] for n in G.nodes(data=True)]
            handles,labels=scatter.legend_elements()[0],set(lab)
            ax.legend(handles=handles,labels=labels, loc="best")
            
        
        
        
        ax.axis('off')
        plt.tight_layout()
        if save:
            plt.savefig(save,dpi=300)

        plt.show()
    elif mode=='3d':
        #LAYOUTS ========================================================================================================================
        if layout=='auto':
            iG=ig.Graph.from_networkx(G)
            my_layout=iG.layout_auto(dim=3)
            sources = iG.get_edge_dataframe()['source'].map(iG.get_vertex_dataframe()._nx_name)
            targets = iG.get_edge_dataframe()['target'].map(iG.get_vertex_dataframe()._nx_name)
            node_coordinates=dict(enumerate(my_layout.coords))
        if layout == 'kk':
            node_coordinates=nx.kamada_kawai_layout(G,dim=3)
        elif layout == 'spring':
            node_coordinates=nx.spring_layout(G,dim=3)
        elif layout== 'spectral':
            node_coordinates=nx.spectral_layout(G,dim=3)
        
        
        #==================================================DEFINE XYZ OF THE SCATTERS AND EDGES========================================
        
        Xn=[coords[0] for coords in node_coordinates.values()]# x-coordinates of nodes
        Yn=[coords[1] for coords in node_coordinates.values()]# y-coordinates
        Zn=[coords[2] for coords in node_coordinates.values()]# z-coordinates
        
        Xe=sum([(node_coordinates[e[0]][0], node_coordinates[e[1]][0],None) for e in G.edges()],())# x-coordinates of edge ends
        Ye=sum([(node_coordinates[e[0]][1], node_coordinates[e[1]][1],None) for e in G.edges()],())
        Ze=sum([(node_coordinates[e[0]][2], node_coordinates[e[1]][2],None) for e in G.edges()],())
                
        traces = []
     
            
        #==================================================    LABELS    ============================================

        if annotate:
            lab=[n[1][annotate] for n in G.nodes(data=True)]
            labdict = dict(zip(list(G.nodes()),lab))
        else:
            lab = []
        
        
        
        #==================================================     COLORS    ========================================

        if node_color_attribute:
            
            NodeClasses=[n[1][node_color_attribute] for n in G.nodes(data=True)]
            N = len(set(NodeClasses))
            Cdict=dict(zip(set(NodeClasses),[n for n in range(N)]))
            NodeColors = list(map(Cdict.get,NodeClasses))
            
            
            class_color_dict = dict(zip(NodeClasses,NodeColors))


            trace1=go.Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=dict(color='rgb(125,125,125)', width=1),
                   hoverinfo='none',
                   showlegend=False
                   )

            traces.append(trace1)

            for Class in set(NodeClasses):
                ClassNodes = [n[0] for n in G.nodes(data = True) if n[1][node_color_attribute] == Class]
                ClassLabels = [labdict[n] for n in ClassNodes]
                Xc = [node_coordinates[n][0] for n in ClassNodes]
                Yc = [node_coordinates[n][1] for n in ClassNodes]
                Zc = [node_coordinates[n][2] for n in ClassNodes]

                traces.append(go.Scatter3d(x=Xc,
                            y=Yc,
                            z=Zc,
                            mode='markers',
                            name=Class,
                            marker=dict(symbol='circle',
                                            size=node_size/10,
                                            color=class_color_dict[Class],
                                            colorscale=cmap,
                                            line=dict(color='rgb(50,50,50)', width=0.5)
                                            ),
                            hovertext=ClassLabels,
                            hoverinfo='text',
                            showlegend = True
                            ))

            axis=dict(showbackground=False,
                    showline=False,
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    title=''
                    )

            fig_layout = go.Layout(
                    title=figure_title,
                    width=1000,
                    height=1000,
                    showlegend=True,
                    scene=dict(
                        xaxis=dict(axis),
                        yaxis=dict(axis),
                        zaxis=dict(axis),
                    ))

        else:
            N = len(G.nodes)
            NodeColors = [0 for n in range(N)]
            colors  = [f"C{i}" for i in np.arange(1, max(NodeColors)+1)]
        
        
        
            traces = []
        
        

            traces.append(go.Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=dict(color='rgb(125,125,125)', width=1),
                   hoverinfo='none',
                   showlegend=False
                   ))



            traces.append(go.Scatter3d(x=Xn,
                            y=Yn,
                            z=Zn,
                            mode='markers',
                            name='Nodes',
                            marker=dict(symbol='circle',
                                            size=node_size/10,
                                            line=dict(color='rgb(50,50,50)', width=0.5)
                                            ),
                            hovertext=lab,
                            hoverinfo='text',
                            showlegend = False
                            ))

        axis=dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

        fig_layout = go.Layout(
                title=figure_title,
                width=1000,
                height=1000,
                showlegend=True,
                scene=dict(
                    xaxis=dict(axis),
                    yaxis=dict(axis),
                    zaxis=dict(axis),
                ))
        data=traces
        fig=go.Figure(data=data, 
                      layout=fig_layout
                      )
        
        fig.show()
        if save:
            fig.write_html(save)
    
    elif mode == 'cytoscape':
        
        pass # STILL TO BE IMPLEMENTED






















def plot_degree_distribution(graph,save_fig=False):
    degree=[val for (node, val) in graph.degree()]
    freqdict=Counter(degree)
    frequency=[]
    frequency0=[]
    degree0=[]
    for x in degree:
        if x==0:
            degree0.append(0)
            frequency0.append(freqdict[x])
        else:
            frequency.append(freqdict[x])

    fig, ax= plt.subplots(figsize=(20,10))
    datax=np.log10([elem for elem in degree if elem!=0])
    datay=np.log10(frequency)

    #PLOT DEGREE == 0  NODES  IF THERE ARE ANY
    if len(frequency0)>0:
        ax.scatter(datax,datay, alpha=0.5,s=300,edgecolor='b')
        ax.scatter(-0.1,np.log10(freqdict[0]),alpha=0.5,s=300,edgecolor='red')
    else:
        ax.scatter(datax,datay, alpha=0.5,s=300,edgecolor='b')

    ##CHOOSE THE DEGREES TICKS TO DISPLAY                    
    ax.set_yticks(np.log10(np.geomspace(1,max(frequency),20,dtype=int)))
    ax.set_yticklabels(np.geomspace(1,max(frequency),20,dtype=int),fontsize=12)


    ##CHOOSE THE DEGREES TICKS TO DISPLAY
    ax.set_xticks(np.log10(np.geomspace(1,max(degree),20,dtype=int)))
    ax.set_xticklabels(np.geomspace(1,max(degree),20,dtype=int),fontsize=12)


    ax.grid()
    ax.set_xlabel('Degree',fontsize=20)
    ax.set_ylabel('Frequency',fontsize=20)
    ax.set_xlim(-0.150)
    
    if save_fig:
        plt.savefig(save_fig,dpi=300)
    plt.show()