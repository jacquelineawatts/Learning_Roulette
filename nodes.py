class KATree(object):
    """Khan Academy API topic tree."""

    def __init__(self, head):
        self.head = head

    def __repr__(self):
        return "<TREE HEAD: {}>".format(self.head.slug)


class AbstractNode(object):
    """Inheritance class for methods used by Topic and Video node classes."""

    def find_node(self, slug):

        print "Starting new node: ", self
        print '...with slug: ', self.slug
        if self.slug == slug:
            return self
        elif self.children:
            for child in self.children:
                node = child.find_node(slug)
                if node:
                    return node
        else:
            return None



class TopicNode(AbstractNode):
    """A topic node from the KA Tree.

    >>> parent = KA_Node('title1', 'slug1', 'url1')
    >>> child = KA_Node('title2', 'slug2', 'url2')
    >>> child2 = KA_Node('title3', 'slug3', 'url3')

    >>> parent.children.append(child)
    >>> parent.children.append(child2)
    >>> parent.children
    [<NODE: slug2>, <NODE: slug3>]

    """

    def __init__(self, title, slug, url):
        self.title = title
        self.slug = slug
        self.url = url
        self.children = []

    def __repr__(self):
        return "<NODE: {}>".format(self.slug)


class VideoNode(AbstractNode):
    """A video node from the KA Tree. """

    def __init__(self, title, readable_id, url, slug, duration):
        self.title = title
        self.readable_id = readable_id
        self.url = url
        self.slug = slug
        self.duration = duration
        self.children = []

    def __repr__(self):
        return "<NODE: {} {}>".format(self.slug, self.url)
    
