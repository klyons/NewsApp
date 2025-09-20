import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D


#heatmap plot - needs similarity matrix & header labels
def plot_similarity_heatmap(similarity_matrix, labels, name):
    plt.figure(figsize=(8,6))
    sns.heatmap(similarity_matrix, xticklabels=labels, yticklabels=labels, annot=True, cmap="coolwarm")
    plt.title(f"Headline {name} Similarity Heatmap")
    plt.show()
    
# needs similarity matrix & header labels
def plot_similarity_network(similarity_matrix, labels, name, threshold=0.2):
    G = nx.Graph()
    for h in labels:
        G.add_node(h)
    
    # Add edges with weight above threshold
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            if similarity_matrix[i,j] > threshold:
                G.add_edge(labels[i], labels[j], weight=similarity_matrix[i,j])
    
    pos = nx.spring_layout(G, seed=42)
    weights = [G[u][v]['weight']*5 for u,v in G.edges()]  # scale thickness
    
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, width=weights)
    plt.title(f"Headline {name} Similarity Network")
    plt.show()

#scatter plot 
def plot_headline_3d_scatter(cosine_matrix, semantic_matrix, labels, sources):
    """
    Plots a 3D scatter where:
      - X = cosine similarity (flattened pairs)
      - Y = semantic similarity (flattened pairs)
      - Z = categorical source encoding
    """
    
    n = len(labels)
    
    # Collect pairwise similarities (upper triangle only to avoid duplicates)
    x_vals, y_vals, z_vals, pair_labels = [], [], [], []
    
    # Map sources to numeric values for Z-axis
    unique_sources = list(set(sources))
    source_map = {src: i for i, src in enumerate(unique_sources)}
    
    for i in range(n):
        for j in range(i+1, n):  # only upper triangle
            x_vals.append(cosine_matrix[i, j])
            y_vals.append(semantic_matrix[i, j])
            # Encode source pair as average of numeric codes
            z_vals.append((source_map[sources[i]] + source_map[sources[j]]) / 2)
            pair_labels.append(f"{labels[i]} ↔ {labels[j]}")
    
    # Convert to numpy arrays
    x_vals, y_vals, z_vals = np.array(x_vals), np.array(y_vals), np.array(z_vals)
    
    # Plot
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='tab10', s=80)
    
    # Add labels for some points
    for i, txt in enumerate(pair_labels):
        ax.text(x_vals[i], y_vals[i], z_vals[i], txt, fontsize=8)
    
    ax.set_xlabel("Cosine Similarity")
    ax.set_ylabel("Semantic Similarity")
    ax.set_zlabel("Source Category")
    ax.set_title("Cosine vs Semantic Similarity by Source")
    
    # Legend for sources
    handles = [plt.Line2D([0], [0], marker='o', color='w',
                          label=src, markerfacecolor=plt.cm.tab10(source_map[src]),
                          markersize=10) for src in unique_sources]
    ax.legend(handles=handles, title="Sources")
    
    plt.show()


def plot_headline_3d_scatter_list(cosine_list, semantic_list, sentiment_list, labels):
    """
    Plots a 3D scatter where:
      - X = cosine similarity (list of values)
      - Y = semantic similarity (list of values)
      - Z = sentiment score (list of values, e.g. -1 = negative, 0 = neutral, 1 = positive)
    
    Arguments:
      cosine_list: list of cosine similarity values (flattened pairs)
      semantic_list: list of semantic similarity values (flattened pairs)
      sentiment_list: list of sentiment scores for each pair (same length as cosine_list)
      labels: list of label pairs, e.g. ["A ↔ B", "A ↔ C", ...]
    """
    
    # Convert to numpy
    x_vals = np.array(cosine_list)
    y_vals = np.array(semantic_list)
    z_vals = np.array(sentiment_list)

    # Plot
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='coolwarm', s=80)
    
    # Add labels for each point
    for i, txt in enumerate(labels):
        ax.text(x_vals[i], y_vals[i], z_vals[i], txt, fontsize=8)
    
    ax.set_xlabel("Cosine Similarity")
    ax.set_ylabel("Semantic Similarity")
    ax.set_zlabel("Sentiment Score")
    ax.set_title("Cosine vs Semantic Similarity vs Sentiment")
    
    # Add colorbar for sentiment interpretation
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.6)
    cbar.set_label("Sentiment Score")
    
    plt.show()