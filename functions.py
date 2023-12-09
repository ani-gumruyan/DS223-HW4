
import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig


def plot_directed_graph(graph):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize = (20, 10))
    nx.draw(graph, pos, with_labels = False, ax = ax, alpha = 0.6,
            node_size = 100, node_color = 'rosybrown')
    plt.show()


def find_bridges(graph):
    bridges = []
    visited = set()
    disc = {}  # Discovery times of vertices
    low = {}   # Earliest visited vertex reachable from the subtree rooted at that vertex

    time = 0 

    def dfs(u, parent):
        nonlocal time
        disc[u] = time
        low[u] = time
        time += 1

        visited.add(u)

        for v in graph.neighbors(u):
            if v not in visited:
                dfs(v, u)
                low[u] = min(low[u], low[v])

                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for node in graph.nodes():
        if node not in visited:
            dfs(node, None)

    return bridges


def plot_graph_with_centrality(graph, sorted_closeness, sorted_betweenness, sorted_eigenvector):
  pos = nx.spring_layout(graph)
  fig, ax = plt.subplots(figsize = (20,10))

  # Draw the graph with rosybrown color for nodes
  nx.draw(graph, pos, with_labels = False, node_color = 'rosybrown', 
          alpha = 0.6, node_size = 100, ax = ax)

  # Highlight nodes with the highest centrality in red
  top_nodes_closeness = [node for node, _ in sorted_closeness[:5]]
  nx.draw_networkx_nodes(graph, pos, nodelist = top_nodes_closeness, alpha = 0.6,
                        node_color = 'sienna', node_size = 200, ax = ax)

  top_nodes_betweenness = [node for node, _ in sorted_betweenness[:5]]
  nx.draw_networkx_nodes(graph, pos, nodelist = top_nodes_betweenness, alpha = 0.6, 
                        node_color = 'cadetblue', node_size = 200, ax = ax)

  top_nodes_eigenvector = [node for node, _ in sorted_eigenvector[:5]]
  nx.draw_networkx_nodes(graph, pos, nodelist = top_nodes_eigenvector, alpha = 0.6, 
                        node_color = 'olive', node_size = 200, ax = ax)

  plt.show()


def plot_three_largest_communities(graph, largest_three_communities):
  pos = nx.spring_layout(graph)
  fig, axes = plt.subplots(1, 3, figsize = (20, 10))

  for i, community in enumerate(largest_three_communities):
      nx.draw(graph.subgraph(community), pos, with_labels = True, alpha = 0.6, 
              node_color = 'rosybrown', node_size = 100, ax = axes[i])
      axes[i].set_title(f"Largest Community {i + 1}")

  plt.tight_layout()
  plt.show()


def remove_top_nodes_community(community_subgraph, centrality_measure, top_k = 3, **kwargs):
    centrality_dict = centrality_measure(community_subgraph, **kwargs)
    sorted_centrality = sorted(centrality_dict.items(), key = lambda x: x[1], reverse = True)
    top_nodes = [node for node, _ in sorted_centrality[:top_k]]
    return top_nodes


def plot_with_removed_nodes(graph, largest_three_communities):
  for i, community in enumerate(largest_three_communities):
      community_subgraph = graph.subgraph(community).copy()

      # Remove top nodes based on centrality measures
      degree_top_nodes = remove_top_nodes_community(community_subgraph, nx.degree_centrality)
      closeness_top_nodes = remove_top_nodes_community(community_subgraph, nx.closeness_centrality)
      betweenness_top_nodes = remove_top_nodes_community(community_subgraph, nx.betweenness_centrality)
      eigenvector_top_nodes = remove_top_nodes_community(community_subgraph, nx.eigenvector_centrality, max_iter = 1000)

      # Remove the top nodes from the community subgraph
      community_subgraph.remove_nodes_from(degree_top_nodes + closeness_top_nodes + betweenness_top_nodes + eigenvector_top_nodes)

      # Visualization after removing top nodes from each community
      pos = nx.spring_layout(graph)
      fig, axes = plt.subplots(1, 4, figsize = (20, 10))

      # Plot the community subgraph after removing top nodes
      nx.draw(community_subgraph, pos, with_labels = True, alpha = 0.6, 
              node_color = 'rosybrown', node_size = 100, ax = axes[0])
      axes[0].set_title(f"Community {i + 1} After Top Node Removal")

      # Plot the community subgraph after removing top nodes based on Degree Centrality
      nx.draw(graph.subgraph(degree_top_nodes), pos, with_labels = True, alpha = 0.6, 
              node_color = 'sienna', node_size = 100, ax = axes[1])
      axes[1].set_title(f"Community {i + 1} After Degree Centrality Removal")

      # Plot the community subgraph after removing top nodes based on Closeness Centrality
      nx.draw(graph.subgraph(closeness_top_nodes), pos, with_labels = True, alpha = 0.6, 
              node_color = 'cadetblue', node_size = 100, ax = axes[2])
      axes[2].set_title(f"Community {i + 1} After Closeness Centrality Removal")

      # Plot the community subgraph after removing top nodes based on Betweenness Centrality
      nx.draw(graph.subgraph(betweenness_top_nodes), pos, with_labels = True, alpha = 0.6, 
              node_color = 'olive', node_size = 100, ax = axes[3])
      axes[3].set_title(f"Community {i + 1} After Betweenness Centrality Removal")

      plt.tight_layout()
      plt.show()


def find_top_nodes_community(community_subgraph, centrality_measure, top_k = 3, **kwargs):
    centrality_dict = centrality_measure(community_subgraph, **kwargs)
    sorted_centrality = sorted(centrality_dict.items(), key = lambda x: x[1], reverse = True)
    top_nodes = [node for node, _ in sorted_centrality[:top_k]]
    return top_nodes   


def plot_with_highlighted_influencers(graph, largest_three_communities):
  for i, community in enumerate(largest_three_communities):
    # Create a subgraph for the current community
    community_subgraph = graph.subgraph(community).copy()

    # Find top nodes based on different centrality measures within each community
    degree_top_nodes = find_top_nodes_community(community_subgraph, nx.degree_centrality)
    closeness_top_nodes = find_top_nodes_community(community_subgraph, nx.closeness_centrality)
    betweenness_top_nodes = find_top_nodes_community(community_subgraph, nx.betweenness_centrality)
    
    # Increase max_iter for eigenvector centrality to 1000
    eigenvector_top_nodes = find_top_nodes_community(community_subgraph, nx.eigenvector_centrality, max_iter = 1000)

    # Combine all top nodes for plotting
    all_top_nodes = set(degree_top_nodes + closeness_top_nodes + betweenness_top_nodes + eigenvector_top_nodes)

    # Visualization of the influencers within each community
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize = (20,10))

    # Plot the community subgraph
    nx.draw(community_subgraph, pos, with_labels = True, alpha = 0.6, 
            node_color = 'rosybrown', node_size = 50, ax = ax)

    # Highlight the top nodes based on different centrality measures
    nx.draw_networkx_nodes(community_subgraph, pos, nodelist = all_top_nodes, 
                           node_size = 500, node_color = 'maroon', ax = ax)

    plt.title(f"Largest Community {i + 1} with Top Influencers")
    plt.show()
    