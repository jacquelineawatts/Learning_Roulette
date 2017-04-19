import requests
import time
import random
from nodes import KATree, TopicNode, VideoNode
import cPickle as pickle

def call_api_and_return_tree(kind, slug=None):
    """Makes initial call to topictree endpoint, returns root node.

    Potential values for kind include Topic, Video, and Exercise."""

    print "Beginning API call..."

    if kind == 'Topic':
        response = requests.get("http://www.khanacademy.org/api/v1/topictree?kind=" + kind).json()
    elif kind == 'Video':
        print 'Slug: ', slug
        
    print "Response successfully received!"
    # print 'Reponse: ', response
    print "Building tree:"
    tree = KATree(build_tree(response, kind))

    return tree


def build_tree(response, kind):
    """Builds node relationships to build tree from Khan Academy API.

    Title Nodes include: title, slug, url, and children topic nodes.
    Video Nodes include: title, slug, url, readable_id, and duration.
    """

    # print "Starting new recursive call..."
    if response:
        # print 'RESPONSE KEYS: ', response.keys()
        if kind == 'Topic':
            current_node = TopicNode(response.get('standalone_title'),
                                      response.get('slug'),
                                      response.get('ka_url'))
        elif kind == 'Video':
            current_node = VideoNode(response.get('title'), 
                                      response.get('readable_id'),
                                      response.get('ka_url'),
                                      response.get('slug'),
                                      response.get('duration'))

        # print 'Current node: ', current_node
   
        if response.get('children'):
            for child in response['children']:
                child_node = build_tree(child, kind)
                current_node.children.append(child_node)

        # print 'Current node children: ', current_node.children

        return current_node


def get_video(topic, time, node):
    """Given a topic slug and a time preference, returns a relevant video.

    Time preference provided in seconds."""

    print ""
    print "New API request for videos: "
    response = requests.get('http://www.khanacademy.org/api/v1/topic/' + topic + '/videos').json()

    if response:
        # print 'Found one!'
        for r in response:
            # print 'RESPONSE: ', r
            if r['duration'] < time:
                return r

    elif node.children:
        # print 'None found... but checking children nodes.'
        for node in node.children:
            video = get_video(node.slug, time, node)
            if video:
                return video

    return None


def return_all_nodes(root):
    """Provided with a root node, returns list of all nodes, not including leaves. """

    all_nodes_with_children = []

    def traverse_tree(root):
        """Given root, traverses tree and appends all nodes to external list."""
        if root.children:
            for child in root.children:
                traverse_tree(child)
            all_nodes_with_children.append(root) 
    
    traverse_tree(root)

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


def pickle_topic_tree():
    """Makes API call and pickles response."""

    topic_tree = call_api_and_return_tree('Topic')
    file_object = open('topic_tree_response.p', 'wb')

    pickle.dump(topic_tree, file_object)


if __name__ == '__main__':
    # import doctest
    # if doctest.testmod().failed == 0:
    #     print "\n*** ALL TESTS PASSED.\n"

    pickle_topic_tree()
