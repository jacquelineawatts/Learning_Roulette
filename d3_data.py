from ka_api import KA_Node, KA_Tree


def return_all_nodes(root):

    all_nodes_with_children = []

    def traverse_tree(root):
        if root.children:
            for child in root.children:
                traverse_tree(child)
            all_nodes_with_children.append(root) 
    
    return all_nodes_with_children


def find_nodes_and_paths(root):
    """Given a root node for a tree, returns all nodes and paths.

    Leaf nodes are not included, as selecting a leaf node on the graph would not 
    have an additional videos other than itself associated with it. To maintain a
    bit of randomness with the video selected, only included nodes with children.
    """

    all_nodes = return_all_nodes(root)

    nodes = [{'title': node.title,
              'slug': node.slug,
              'url': node.url,
              'num_children': len(node.children)}
              for node in all_nodes]

    index_nodes = {}
    for i, node in enumerate(nodes):
        index_nodes[node['slug']] = i

    
    paths = [{'source': index_nodes[node.slug],
              'target': index_nodes[child.slug]} 
              for node in all_nodes for child in node.children if child.children]

    print "NODES: ", nodes
    print "PATHS: ", paths

    return nodes, paths
