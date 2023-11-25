
import copy
import ply.lex as lex
import ply.yacc as yacc
from automate_parser import Automate


# Liste des noms des tokens
tokens = (
    'TRUE',
    'FALSE',
    'ID',
    'AND',
    'OR',
    'NOT',
    'X',
    'G',
    'F',
    'E',
    'A',
    'U',
    'LPAREN',
    'RPAREN',
)

# Expressions régulières pour les tokens
t_TRUE = r'true'
t_G = r'G'
t_F = r'F'
t_FALSE = r'false'
t_AND = r'\^'
t_OR = r'v'
t_NOT = r'not'
t_E = r'E'
t_U = r'U'
t_X = r'X'
t_A = r'A'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ID = r'[B-DH-MP-SWY-Zb-dh-mp-swy-z0-9]+'

# Ignorer les espaces et les tabulations
t_ignore = ' \t'


# Operator precedence and associativity
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'U'),
    ('left', 'F'),
    ('left', 'G'),
    ('left', 'X'),
)

# Règles de grammaire
def p_formula(p):

    """
    formula : atomic_formula
            | TRUE
            | FALSE
            | NOT formula
            | A formula
            | E formula
            | formula AND formula
            | formula OR formula
            | formula U formula
            | LPAREN formula RPAREN
            | E X formula
            | E G formula
            | E F formula
            | A X formula
            | A G formula
            | A F formula
    """
 
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        elif p[1] in ('A', 'E') and p[2] in ('X', 'G', 'F'):
            p[0] = (p[1] + p[2], p[3])
        elif p[1] in ('A', 'E') and p[3] == 'U':
            p[0] = (p[1] + p[2], p[3])
        else:
            p[0] = (p[2], p[1], p[3])
     

def p_atomic_formula(p):
    """
    atomic_formula : ID
    """
    # Gérer la construction de l'arbre syntaxique ici
    p[0] = ('ID', p[1])

def p_error(p):
    """
    Fonction de gestion des erreurs de syntaxe
    """
    if p:
        print(f"Erreur de syntaxe à la position {p.lexpos}: Caractère non valide : '{p.value}'")
    else:
        print("Erreur de syntaxe : fin de fichier inattendue")

def t_error(t):
    print("Caractère non valide : '%s'" % t.value[0])
    t.lexer.skip(1)

# Création de l'analyseur lexical et du parseur
lexer = lex.lex()
parser = yacc.yacc()


class CTL_Evaluateur:
    """ Classe qui permettant """


    def __init__(self, automate:Automate):
        self.automate = copy.deepcopy(automate)

        # Contient le marquage de chaque formule
        # Par exemple markings = {formule1 : { q1 : False, q2: True, q3: False} }
        # Ainsi nous pourrons les réutilisé pour la formule parente
        self.markings = dict()

        # Contient la vérification de chaque formule sur l'automate
        # Par exemple verified_formulas = {formule1 : True, formule2: False, ...} }
        self.verified_formulas = dict()

    def mark_states_to_false(self,formula):
        self.markings[formula] = {}
        for state in self.automate.node_names:
            self.markings[formula][state] = False 


    def parse_file(file_path):
        """Lecture du fichier .ctl et mise en tableau"""
        
        formules = []
        try:
            with open(file_path, 'r') as file:
                count = 1
                for formule in file.readlines():
                    formules.append(formule.strip())
                    count += 1
                    
            parsed_formulas = []
            for input_formula in formules:
                parsed_formulas.append(parser.parse(input_formula, lexer=lexer))
            return parsed_formulas
        
        except FileNotFoundError:
            print("Le fichier spécifié est introuvable.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")


    def mark_formula(self,formula):

        if isinstance(formula, str):

            return self.mark_atomic(formula)
        
        if isinstance(formula, tuple):

            operator, *_ = formula

            if operator == 'EX':
                return self.EX(formula)
            if operator == 'EF':
                return self.EF(formula)
            if operator == 'EG':
                return self.EG(formula)
            elif operator == 'E':
                innerFormuleOperator = formula[1][0]
                if innerFormuleOperator == 'U':
                    return self.EU(formula)
            
            elif operator == 'AX':
                return self.AX(formula)
            elif operator == 'AF':
                return self.AF(formula)
            elif operator == 'AG':
                return self.AG(formula)
            
            elif operator == 'A':
                innerFormuleOperator = formula[1][0]
                if innerFormuleOperator == 'U':
                    return self.AU(formula)
            # elif operator == 'U':
            #     return self.U(formula)
            elif operator == '^':
                return self.AND(formula)
            elif operator == 'v':
                return self.OR(formula)
            elif operator == 'not':
                return self.NOT(formula)
            elif operator == 'ID':
                return self.ID(formula)
            
    def mark_atomic(self,formula):
        
        self.mark_states_to_false(formula)
        
        mark = {}
        
        for state in self.automate.node_names:
            if formula == 'true':
                mark[state] = True
            elif formula == 'false':
                mark[state] = False
            else : 
                mark[state] = formula in self.automate.atomic_propositions[state] 
        
        # Ajout du marquage de la proposition atomique
        self.markings[formula] = mark
        

        
    def EX(self, formula):
        # Check if the formula is true for at least one successor of the current state
        """
        Marque les états de l'automate pour la formule CTL EX(psi).
        Utilise l'algorithme de marquage fourni.
        """

        print("Appel à EX ---------> ")
        
        self.verified_formulas[formula] = False
        
        # Recuperer la sous formule de EX 
        _, innerformula = formula 
        
        self.mark_states_to_false(formula)

        self.mark_formula(innerformula)


        # Pour chaque place dans les transitions on verifie si la place suivante vérifie est vraie si oui on met son précédent à True.
        for transition in self.automate.transitions:
            if self.markings[innerformula][transition[1]]==True:
                self.markings[formula][transition[0]] = True
                self.verified_formulas[formula] = True

    
    def EU(self,formula):

        print("Appel à EU ---------> ")

        # self.mark_states_to_false(formula)

        _, *operands = formula

        leftFormula = operands[0][1]

        print("operands ", operands[0][2])

        rightFormula = operands[0][2]

        self.mark_formula(leftFormula)
        self.mark_formula(rightFormula)

        degreeS = dict()

        
        self.mark_states_to_false(formula)

        for state in self.automate.node_names:
            degreeS[state] = {}
            degreeS[state]['degree'] = False

        L = set()

        # marking(ψ2)
        for state in self.automate.node_names:
            if self.markings[rightFormula][state]:  # Vérifie si q.ψ2 est True
                L.add(state)  # Ajoute q à l'ensemble L

        while L:  # Tant que L n'est pas vide
            state = L.pop()  # Prend un élément q de L et le supprime de L
            self.markings[formula][state] = True  # Met à jour q.φ à True

            # parcours de toutes les transitions (q', _, q) dans T
            for from_state, _ in self.automate.transitions:
                if not degreeS[from_state]['degree']:  # Vérifie si q'.degree est False
                    degreeS[from_state]['degree'] = True  # Met q'.degree à True
                    if self.markings[leftFormula][from_state]:  # Vérifie si q'.ψ1 est True
                        L.add(from_state)  # Ajoute q' à l'ensemble L

        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]
    

    def EF(self,formula):
        
        print("Appel à EF ---------> ")

        self.mark_states_to_false(formula)

        _, innerformula = formula

        equivalent_formula = ('E', ('U', 'true', innerformula))

        self.mark_formula(equivalent_formula)

        self.markings[formula] = self.markings[equivalent_formula]

        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]


    def EG(self,formula):
        
        print("Appel à EG ---------> ")

        self.mark_states_to_false(formula)

        _, innerformula = formula

        # not (true U not  phi)
        equivalent_formula = ('not',('A',('U','true',('not',innerformula))))

        self.mark_formula(equivalent_formula)

        self.markings[formula] = self.markings[equivalent_formula]

        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]


    def AF(self,formula):

        print("Appel à AF ---------> ")
        print(formula)

        self.mark_states_to_false(formula)

        _, innerformula = formula

        equivalent_formula = ('A', ('U', 'true', innerformula))

        self.mark_formula(equivalent_formula)

        self.markings[formula] = self.markings[equivalent_formula]

        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]



    def AU(self,formula):

        print("Appel à AU ---------> ")

        _, *operands = formula

        print("AU fromule operands", operands)

        leftFormula = operands[0][1]
        rightFormula = operands[0][2]

        print("leftFormula ",leftFormula)
        print("rightFormula ",rightFormula)

        self.mark_formula(leftFormula)
        self.mark_formula(rightFormula)

        degreeS = dict()
        L = set()
        
        self.mark_states_to_false(formula)

        for state in self.automate.node_names:
            for from_state,_ in self.automate.transitions:
                if from_state == state:
                    degreeS[state] = degreeS.get(state,0) + 1
         
        for state in self.automate.node_names:
            if not state in degreeS.keys():
                degreeS[state] = 0

        # We retrieve all the states q that satisfies the UNTIL(rightFormula) condition 
        for state in self.automate.node_names:
            if self.markings[rightFormula][state]:
                L.add(state)

        #We go through the list and verify the predecessors of q that verify the left formula
        while L:  
            state = L.pop()
            self.markings[formula][state] = True  # Met à jour q.φ à True

            for from_state, _ in self.automate.transitions:
                
                degreeS[from_state] = degreeS[from_state] - 1
                
                from_degree = degreeS.get(from_state)

                if from_degree == 0 and self.markings[leftFormula][from_state] and (not self.markings[formula][from_state]):
                    L.add(from_state)
        
        # self.verified_formulas[formula] = all([val for _,val in self.markings[formula].items()])
        # print("Fromule :AND", formula ,self.markings[formula].items())
        self.verified_formulas[formula] = [val for _,val in self.markings[formula].items()][0]



    def AX(self,formula):

        print("Appel à AX ---------> ")

        self.mark_states_to_false(formula)

        _, innerformula = formula

        equivalent_formula = ('not',('EX',('not',innerformula )))

        self.mark_formula(equivalent_formula)

        self.markings[formula] = self.markings[equivalent_formula]

        self.verified_formulas[formula] = self.verified_formulas[equivalent_formula]



    def AG(self,formula):

        print("Appel à AG ---------> ")

        self.mark_states_to_false(formula)

        _, innerformula = formula

        
        print("inerformula ",innerformula)

        equivalent_formula = ('not',('E',('U','true',('not',innerformula))))

        self.mark_formula(equivalent_formula)

        self.markings[formula] = self.markings[equivalent_formula]

        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]




    def AND(self, formula):

        print("Appel à AND ---------> ")
        _, *operands = formula

        leftFormula = operands[0]
        rightFormula = operands[1]
        
        self.mark_states_to_false(formula)

        self.mark_formula(leftFormula)
        self.mark_formula(rightFormula)

        for noeud in self.automate.node_names:
            self.markings[formula][noeud] = self.markings[leftFormula][noeud] and self.markings[rightFormula][noeud]
        
        self.verified_formulas[formula] = (self.verified_formulas[leftFormula] and self.verified_formulas[rightFormula]) if rightFormula in self.verified_formulas and leftFormula in self.verified_formulas else False

    # def U(self,formula):
    #     self.EU(formula)

    def OR(self, formula):

        print("Appel à OR ---------> ")
        _, *operands = formula

        leftFormula = operands[0]
        rightFormula = operands[1]
        
        self.mark_states_to_false(formula)

        self.mark_formula(leftFormula)
        self.mark_formula(rightFormula)

        for noeud in self.automate.node_names:
            self.markings[formula][noeud] = self.markings[leftFormula][noeud] or self.markings[rightFormula][noeud]
        
        self.verified_formulas[formula] = (self.verified_formulas[leftFormula] or self.verified_formulas[rightFormula]) if rightFormula in self.verified_formulas or leftFormula in self.verified_formulas else False
        

    def NOT(self,formula):

        print("Appel à NOT ---------> ")

        _,innerformule = formula

        self.mark_states_to_false(formula)

        self.mark_formula(innerformule)

        for noeud in self.automate.node_names:
            self.markings[formula][noeud] = not (self.markings[innerformule][noeud])
            
        
        if isinstance(formula, tuple) and innerformule[0] != 'ID' and innerformule[0] != 'not':
            self.verified_formulas[formula] = not self.verified_formulas[innerformule]
        else:
            self.verified_formulas[formula] = not self.verified_formulas[innerformule]


    def ID(self,formula):
        print("Appel à ID (proposition atomique) ---------> ")

        _,innerformule = formula
        self.mark_states_to_false(formula)

        self.mark_formula(innerformule)

        self.markings[formula] = copy.deepcopy(self.markings[innerformule])
        
        self.verified_formulas[formula] = self.markings[formula][self.automate.init_node]

