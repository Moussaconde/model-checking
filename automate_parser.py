import pydot

class Automate:
    def __init__(self):
        self.init_node = ''
        self.transitions = list()
        self.node_names = set()
        self.atomic_propositions = dict()

    def successors(self, state):
        return [dest for orig, dest in self.transitions if orig == state]
    
    def is_satisfiable(self, state:str, atomic_prop:str):
        return state in self.atomic_propositions and atomic_prop in self.atomic_propositions[state]
    
    def traitement_dot_file(self,dot_file_path:str):
        # Lire le fichier .dot
        graph = pydot.graph_from_dot_file(dot_file_path)[0]

        # Parcourir les nœuds du graphe
        for node in graph.get_nodes():
            node_name = node.get_name().strip().strip("\"").strip() # Nom du nœud sans les guillemets
            label = node.get_attributes().get('label', '').strip().strip("\"").strip()  # Label du nœud
            shape = node.get_attributes().get('shape', '').strip().strip("\"").strip()  # Forme du nœud
            
            if node_name != "\\n":        
                self.node_names.add(node_name)

                # Vérifier si le nœud est le nœud initial
                if shape == "box":
                    self.init_node = node_name

                if not (node_name in self.atomic_propositions):
                    self.atomic_propositions[node_name] = label
        
        self.node_names = sorted(self.node_names)
        
        # Parcourir les arêtes (transitions)
        for edge in graph.get_edges():
            source = edge.get_source().strip('"')  # Nœud source
            target = edge.get_destination().strip('"')  # Nœud cible
            self.transitions.append((source,target))
    
    def create_graph_png(self,dot_file_path,image_name="automate.png"):
        graph = pydot.graph_from_dot_file(dot_file_path)[0]
        graph.write_png(image_name)


    def __str__(self) -> str:
        return str({"Noeud initial ": self.init_node,"Noeuds " : self.node_names , "Transitions : " : self.transitions , "Propositions_Atomiques " : self.atomic_propositions })


