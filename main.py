from automate_parser import Automate

def main():
    # Chemin vers le fichier .dot
    dot_file_path = "automate.dot"

    automate = Automate()

    automate.traitement_dot_file(dot_file_path)
    print(automate)

    print(automate.successors('q1'))

    print(automate.is_satisfiable('q1','P'))

if __name__ == "__main__":
    main()
