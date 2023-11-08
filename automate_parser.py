import pydot
# import graphviz


# Chemin vers le fichier .dot
dot_file_path = "automate.dot"

# Lire le fichier .dot
graph = pydot.graph_from_dot_file(dot_file_path)[0]

# Créer un dictionnaire pour stocker les informations extraites
automate_info = {
    "Noeuds": {},
    "Transitions": [],
    "Propositions_Atomiques": {}
}

# Parcourir les nœuds du graphe
for node in graph.get_nodes():

    node_name = node.get_name().strip().strip("\"").strip() # Nom du nœud sans les guillemets
    label = node.get_attributes().get('label', '').strip().strip("\"").strip()  # Label du nœud
    shape = node.get_attributes().get('shape', '').strip().strip("\"").strip()  # Forme du nœud
    
    if node_name != "\\n":        
        print("Noeud Avant", node_name, "Label ", label, "shape ", shape)

        # Vérifier si le nœud est le nœud initial
        if shape == "box":
            automate_info["Noeuds"][node_name] = "initial"
        else:
            automate_info["Noeuds"][node_name] = ""

        if not (node_name in automate_info["Propositions_Atomiques"]):
            # Extraire les propositions atomiques du label
            print("LABEL",label)
            automate_info["Propositions_Atomiques"][node_name] = label



# Parcourir les arêtes (transitions)
for edge in graph.get_edges():

    source = edge.get_source().strip('"')  # Nœud source
    target = edge.get_destination().strip('"')  # Nœud cible
    automate_info["Transitions"].append(f"{source} -> {target}")

# Afficher les informations extraites
print("Noeuds:", automate_info["Noeuds"])
print("Transitions:", automate_info["Transitions"])
print("Propositions Atomiques:", automate_info["Propositions_Atomiques"])




# Partie experimentale

# Chemin vers le fichier .dot
dot_file_path = "automate.dot"

# Lire le fichier .dot
graph = pydot.graph_from_dot_file(dot_file_path)[0]
print(graph.get_nodes())
# Générer l'image du graphe
graph_image_path = "automate.png"  # Chemin de l'image de sortie
graph.write_png(graph_image_path)

print(f"Image du graphe générée : {graph_image_path}")



class CTL_Evaluateur:
    def __init__(self, automate_info):
        self.automate_info = automate_info

    def E(self, state, proposition):
        return state in self.automate_info["Noeuds"] and self.automate_info["Noeuds"][state] == proposition

    def A(self, state, proposition):
        return state not in self.automate_info["Noeuds"] or self.automate_info["Noeuds"][state] != proposition

    def AX(self, state, subformula):
        return all(self.X(s, subformula) for s in self.automate_info["Transitions"].get(state, []))

    def EX(self, state, subformula):
        return any(self.X(s, subformula) for s in self.automate_info["Transitions"].get(state, []))

    def AG(self, state, subformula):
        return all(self.G(s, subformula) for s in self.automate_info["Noeuds"])

    def EG(self, state, subformula):
        return any(self.G(s, subformula) for s in self.automate_info["Noeuds"])

    def AF(self, state, subformula):
        return any(self.F(s, subformula) for s in self.automate_info["Noeuds"])

    def EF(self, state, subformula):
        return all(self.F(s, subformula) for s in self.automate_info["Noeuds"])

    def X(self, state, subformula):
        return subformula(state)

    def F(self, state, subformula):
        return subformula(state) or any(self.X(s, self.F(state, subformula)) for s in self.automate_info["Transitions"].get(state, []))

    def G(self, state, subformula):
        return subformula(state) and all(self.X(s, self.G(state, subformula)) for s in self.automate_info["Transitions"].get(state, []))

    def evaluer_formule(self,formule):
        # Analyser la formule pour extraire les sous-formules entre parenthèses
        stack = []
        current = ""
        for char in formule:
            if char == '(':
                if current:
                    stack.append(current)
                    current = ""
                stack.append(char)
            elif char == ')':
                if current:
                    stack.append(current)
                    current = ""
                subformula = stack.pop()  # Extraire la sous-formule
                if subformula == '(':
                    current = ""
                else:
                    # Évaluer la sous-formule et ajouter le résultat à la pile
                    subresult = self.evaluer_formule(subformula)
                    stack.append(subresult)
            else:
                current += char

        if current:
            stack.append(current)

        # Évaluer la formule finale en évaluant les sous-formules de gauche à droite
        result = self.evaluer_formule(stack[0])

        return result

def main():
    automate_info = {
        "Noeuds": {"q1": "P"},
        "Transitions": {"q1": []}
    }

    formule = "EX (P)"

    CTL_e = CTL_Evaluateur(automate_info)

    resultat = CTL_e.evaluer_formule(automate_info, formule)

    if resultat:
        print("Vrai : -)")
    else:
        print("Faux : -)")

if __name__ == "__main__":
    main()
