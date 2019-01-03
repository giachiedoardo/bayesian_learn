class Graph(object):
    def __init__(self, graph=None):
         if graph == None:
             graph = {}
         self.__graph = graph

    def add_node(self, node):
        if node not in self.__graph:
            self.__graph[node] = []

    def add_edge(self, node1,node2):
        #edge = set(edge)
        #(node1, node2) = tuple(edge)
        if node1 in self.__graph:
            for i in range(len(self.__graph[node1])):
                if self.__graph[node1][i]==node2:
                    return
            self.__graph[node1].append(node2)
        else:
            self.__graph[node1] = [node2]

    def nodes(self):
        return list(self.__graph.keys())

    def delete_edge(self, node1, node2):
        #edge = set(edge)
        #(node1, node2) = tuple(edge)
        if node2 not in self.__graph[node1]:
            return
        for i in range(len(self.__graph[node1])):
            if self.__graph[node1][i]==node2:
                del self.__graph[node1][i]
                return

    def stampa(self):
        n={}

        for node in self.__graph:
            e=[]
            for neighbour in self.__graph[node]:
                e.append(neighbour)
            n[node]=e
        print n

    def find_all_paths_mod(self, start_vertex, end_vertex, new_vertex=None, path=[]):
        graph = self.__graph
        if new_vertex==None:
            path = path + [start_vertex]
        else:
            path = path + [new_vertex]
        if new_vertex == end_vertex:
            return [path]
        if new_vertex==None:
            if start_vertex not in graph:
                return []
        else:
            if new_vertex not in graph:
                return []
        paths=[]
        if new_vertex==None:
            for vertex in graph[start_vertex]:
                if vertex not in path:
                    extended_paths = self.find_all_paths_mod(start_vertex, end_vertex, vertex, path)
                    for p in extended_paths:
                        paths.append(p)
        else:
            for vertex in graph[new_vertex]:
                if vertex==end_vertex:
                    extended_paths = self.find_all_paths_mod(start_vertex, end_vertex, vertex, path)
                    for p in extended_paths:
                        paths.append(p)
                if vertex not in path:
                    extended_paths = self.find_all_paths_mod(start_vertex, end_vertex, vertex, path)
                    for p in extended_paths:
                        paths.append(p)
        return paths

    def find_cicle(self):
        for node in self.nodes():
            percorso=self.find_all_paths_mod(node, node)
            if percorso!=[]:
                return "ciclo"
        return "DAG"

    def find_isolated_nodes(self):
        n={}
        no_isolated=[]
        isolated=[]
        for node in self.__graph:
            e=[]
            for neighbour in self.__graph[node]:
                e.append(neighbour)
            n[node]=e
        for node in self.__graph:
            if n[node].__len__()!=0:
                no_isolated.append(node)
                for i in range(n[node].__len__()):
                    no_isolated.append(n[node][i])
        for node in self.__graph:
            presente="no"
            for i in range(no_isolated.__len__()):
                if no_isolated[i]==node:
                    presente="ok"
            if presente=="no":
                isolated.append(node)
        return isolated


