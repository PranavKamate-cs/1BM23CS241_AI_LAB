# -------------------------------------------------------
# Forward Reasoning in First Order Logic (FOL)
# with simple Unification
# -------------------------------------------------------

class KnowledgeBase:
    def __init__(self):
        self.facts = []   # list of ground facts
        self.rules = []   # list of (antecedents, consequent)

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, antecedents, consequent):
        """
        antecedents: list of premise strings like ["Human(x)"]
        consequent: conclusion string like "Mortal(x)"
        """
        self.rules.append((antecedents, consequent))

    def unify(self, var_map, fact, pattern):
        """
        Unify a fact with a pattern (like Human(Socrates) and Human(x))
        Returns substitution map if match is possible, else None.
        """
        if fact.split("(")[0] != pattern.split("(")[0]:
            return None

        fact_args = fact[fact.find("(")+1:fact.find(")")].split(",")
        patt_args = pattern[pattern.find("(")+1:pattern.find(")")].split(",")

        local_map = var_map.copy()
        for f, p in zip(fact_args, patt_args):
            f, p = f.strip(), p.strip()
            if p.islower():  # variable
                if p in local_map and local_map[p] != f:
                    return None
                local_map[p] = f
            elif f != p:
                return None
        return local_map

    def substitute(self, expr, mapping):
        """Replace variables in expr using mapping"""
        result = expr
        for var, val in mapping.items():
            result = result.replace(var, val)
        return result

    def forward_chain(self, query):
        print("Initial Facts:", self.facts)
        new_inferred = True

        while new_inferred:
            new_inferred = False

            for antecedents, consequent in self.rules:
                # Try to find substitutions that make all antecedents true
                for fact in self.facts:
                    mapping = self.unify({}, fact, antecedents[0])
                    if mapping is not None:
                        # Check other antecedents
                        all_match = True
                        for ant in antecedents[1:]:
                            matched = any(
                                self.unify(mapping, f, ant) for f in self.facts
                            )
                            if not matched:
                                all_match = False
                                break

                        if all_match:
                            new_fact = self.substitute(consequent, mapping)
                            if new_fact not in self.facts:
                                print(f"Inferred: {new_fact} from {antecedents}")
                                self.facts.append(new_fact)
                                new_inferred = True
                                if new_fact == query:
                                    print("\n✅ Query proven true!")
                                    return True

        print("\n❌ Query cannot be proven.")
        return False


# -------------------------------------------------------
# Example Usage
# -------------------------------------------------------
if __name__ == "__main__":
    kb = KnowledgeBase()

    # Facts
    kb.add_fact("Human(Socrates)")
    kb.add_fact("Human(Plato)")

    # Rules
    kb.add_rule(["Human(x)"], "Mortal(x)")
    kb.add_rule(["Mortal(x)"], "Dies(x)")

    # Query
    query = "Dies(Socrates)"

    print("Applying Forward Reasoning...\n")
    kb.forward_chain(query)
