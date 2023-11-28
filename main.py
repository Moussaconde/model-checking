#!/usr/bin/env python3

from automate_parser import Automate
from ctl_parser import CTL_Evaluateur
import sys

 
def main():
    
    print()
    # Vérification du nombre correct d'arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py ctl_file_path dot_file_path")
        return
    else:
        ctl_file_path = sys.argv[1]
        dot_file_path = sys.argv[2]

    

    automate:Automate = Automate()

    automate.traitement_dot_file(dot_file_path)

    automate.create_graph_png(dot_file_path)
    
    formules_a_verifier = CTL_Evaluateur.parse_file(ctl_file_path)
        
    
    count_formule=1

    for formule in formules_a_verifier:

        CTL_e = CTL_Evaluateur(automate)
        
        print(f'Formule ' , count_formule ,' : ' , formule)
        
        CTL_e.mark_formula(formule)


        if CTL_e.verified_formulas[formule]:
            print(f'Formule ' , count_formule ,' : Vrai 🤩', "\n\n")
        else:
            print(f'Formule ' , count_formule ,' : Faux 🥺',"\n\n")
        count_formule += 1

if __name__ == "__main__":
    main()





