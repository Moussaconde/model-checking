import ply.lex as lex
import ply.yacc as yacc

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

# Exemple d'utilisation du parseur
for input_formula in [
    "AX (not Q) U (P v Q)",
    "E X (P) ",
    "E X (P ^ Q) ",
    "E ( not Q ) U ( P v Q ) ",
    "E ( P v Q ) U ( Q ^ not P ) ",
    "A ( E ( P ) ) U ( A ( P ) U ( not Q ))"]:
    parsed_tree = parser.parse(input_formula, lexer=lexer)
    print(parsed_tree)

