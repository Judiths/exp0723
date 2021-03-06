# coding=utf-8


class Graph(object):
    # 构造图
    def __init__(self,*args,**kwargs):
        self.node_neighbors = {}
        self.visited = {}

    def add_nodes(self, nodelist):
        # 添加节点
        for node in nodelist:
            self.add_node(node)

    def add_node(self,node):
        # 添加单个节点
        if not node in self.nodes():
            self.node_neighbors[node] = []

    def add_edge(self,edge):
        # 添加边
        u,v = edge
        if(v not in self.node_neighbors[u]) and (u not in self.node_neighbors[v]):
            self.node_neighbors[u].append(v)
            if(u!=v):
                self.node_neighbors[v].append(u)

    def nodes(self):
        # 返回节点
        return list(self.node_neighbors.keys())


    def breadth_first_search(self,root=None):
        # 广度优先遍历
        queue = []
        order = []
        def bfs():
            while len(queue)> 0:
                node = queue.pop(0)
                self.visited[node] = True
                for n in self.node_neighbors[node]:
                    if (not n in self.visited) and (not n in queue):
                        queue.append(n)
                        order.append(n)
        if root:
            queue.append(root)
            order.append(root)
            bfs()
        for node in self.nodes():
            if not node in self.visited:
                queue.append(node)
                order.append(node)
                bfs()
        # print('广度优先遍历', order)

        return order


# if __name__ == '__main__':
#     g = Graph()
#     set = ['a', 'b', 'c','d','e','f','g','h']
#     g.add_nodes(set)
#
#     g.add_edge(('a', 'c'))
#     g.add_edge(('a', 'b'))
#     g.add_edge(('b', 'd'))
#     g.add_edge(('b', 'e'))
#     g.add_edge(('d', 'h'))
#     g.add_edge(('e', 'h'))
#     g.add_edge(('c', 'f'))
#     g.add_edge(('c', 'g'))
#     g.add_edge(('f', 'g'))
#     print("nodes:", g.nodes())
#
#     order = g.breadth_first_search('a')
