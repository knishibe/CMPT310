import os

class KnowledgeBase:
    def __init__(self):
        self.rules = []
        self.atoms = []

    def runKnowledgeBase(self):
        # Accept input from the screen forever until program is killed off
        while True:
            in_data = input("kb> ")
            in_data = in_data.split()
            if in_data[0].lower() == "load":
                self.load(in_data[1])
            elif in_data[0].lower() == "tell":
                if len(in_data) <= 1:
                    print("Error: tell needs at least one atom\n")
                else:
                    self.tell(in_data[1:])
            elif in_data[0].lower() == "infer_all":
                self.infer_all()
            elif in_data[0].lower() == "clear_atoms":
                self.atoms = []
            else:
                print("Error: unknown command \"%s\"\n" %in_data[0])


    def load(self, fileName):
        self.rules = []
        self.atoms = []
        rules = []
        if os.path.isfile(fileName):
            file = open(fileName)
        else:
            print("Error: unknown file \"%s\"\n" %fileName)
            return

        # Get data from file and remove blank spaces/empty lines
        in_data = [rule for rule in file.readlines() if rule.strip()] 

        for rule in in_data:
            # Split rules into lists
            rule = rule.split() 

            # Remove "<--" and "&" and check if rules contain only atoms.
            # If atoms not valid then not a valid KB
            for atom in rule:
                if atom == "<--" or atom == "&":
                    rule.remove(atom)
                elif not self.is_atom(atom):
                    print("Error: %s is not a valid knowledge base\n" %fileName)
                    return

            # Add rule to temporary list that will be added to KB if all rules are valid
            rules.append(rule)

        # Add rules to KB
        self.rules.extend(rules)

        # Print out rules added to screen
        for rule in rules:
            print("   %s <--" %rule[0], end='')
            for atom in rule[1:-1]:
                print(" %s &" %atom, end='')
            print(" %s\n" %rule[-1], end='')

        print("\n   %d new rule(s) added\n" %len(rules))


        file.close()

    def tell(self, atoms):
        # Check if atoms are valid
        for atom in atoms:
            if not self.is_atom(atom):
                print("Error: \"%s\" is not a valid atom\n" %atom)
                return

        # Check if atoms are already in KB
        # If not then add the atoms to the KB
        for atom in atoms:
            if atom in self.atoms:
                print("   atom \"%s\" already known to be true" %atom)
            else:
                print("   \"%s\" added to KB" %atom)
                self.atoms.append(atom)
        print("")
                
    def infer_all(self):
        newly_inferred = []
        atom_added = True
        if not self.rules:
            print("Error: No rules, must call \"load\"\n")
            return
        if not self.atoms:
            print("Error: No atoms can be infered, must call \"tell\"\n")
            return

        # Loop through to account for newly inferred atoms
        while atom_added:
            atom_added = False
            for rule in self.rules:
                atom_true = True
                for atom in rule[1:]:
                    # If an atom on the RHS of a rule is not true,
                    # then the head can't be inferred
                    if atom not in self.atoms and atom not in newly_inferred:
                        atom_true = False
                        break
                # If all atoms on the RHS of a rule are true and the head is not already known
                # then add the head to the KB
                if atom_true and rule[0] not in self.atoms and rule[0] not in newly_inferred:
                    newly_inferred.append(rule[0])
                    atom_added = True

        # Print message to screen
        print("   Newly inferred atoms:")
        print("   ", end='')
        if not newly_inferred:
            print("<none>\n")
        else:
            for atom in newly_inferred:
                print(atom + " ", end='')
            print("\n")
        print("   Atoms already known to be true:")
        print("   ", end='')
        if not self.atoms:
            print("<none>\n")
        else:
            for atom in self.atoms:
                print(atom + " ", end='')
            print("\n")
        self.atoms.extend(newly_inferred)
        return

    # Returns True if, and only if, string s is a valid variable name
    # Taken from assignment page
    def is_atom(self, s):
        if not isinstance(s, str):
            return False
        if s == "":
            return False
        return self.is_letter(s[0]) and all(self.is_letter(c) or c.isdigit() for c in s[1:])

    def is_letter(self, s):
        return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.runKnowledgeBase()