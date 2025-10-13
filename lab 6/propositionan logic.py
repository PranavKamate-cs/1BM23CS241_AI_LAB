from sympy import symbols
from sympy.logic.boolalg import And, Implies, simplify_logic

def check_entailment(kb, query):
    """
    Checks if a knowledge base (kb) entails a query.
    
    Entailment holds if (kb => query) is a tautology.
    We use sympy's simplify_logic, which will return True if the
    expression is a tautology (i.e., logically valid).
    """
    print(f"Checking if KB entails {query}...")
    # The expression for entailment is KB => Query
    implication = Implies(kb, query)
    
    print(f"  - Formulating the implication: {implication}")
    
    # simplify_logic will return `True` if the implication is a tautology
    result = simplify_logic(implication)
    
    print(f"  - Simplified result: {result}")
    return result == True


# --- 1. Define Propositions ---
# P: The student passed the final exam.
# Q: The student completed all assignments.
# R: The student is eligible for a certificate.
# S: The student is on the Dean's List (for a non-entailed example).
P, Q, R, S = symbols('P, Q, R, S')


# --- 2. Create the Knowledge Base (KB) ---
# Rule 1: If the student passed the exam AND completed assignments, they are eligible for a certificate.
rule1 = Implies(And(P, Q), R)
# Fact 2: The student passed the exam.
fact1 = P
# Fact 3: The student completed the assignments.
fact2 = Q

# The KB is the conjunction (AND) of all its sentences
knowledge_base = And(rule1, fact1, fact2)

print("="*40)
print("🧠 KNOWLEDGE BASE AND QUERIES")
print("="*40)
print(f"Propositions:")
print(f"  P: Student passed the exam")
print(f"  Q: Student completed assignments")
print(f"  R: Student is eligible for a certificate")
print(f"  S: Student is on the Dean's List")
print("-" * 20)
print(f"Knowledge Base (KB): {knowledge_base}\n")


# --- 3. Test an Entailed Query ---
# Query alpha: Is the student eligible for a certificate? (R)
query_R = R
is_entailed_R = check_entailment(knowledge_base, query_R)

print("\n**RESULT 1**")
if is_entailed_R:
    print(f"✅ YES, the Knowledge Base entails '{query_R}'.")
    print("This means the query is logically guaranteed to be true given the KB.")
else:
    print(f"❌ NO, the Knowledge Base does not entail '{query_R}'.")


# --- 4. Test a Non-Entailed Query ---
# Query beta: Is the student on the Dean's list? (S)
query_S = S
is_entailed_S = check_entailment(knowledge_base, query_S)

print("\n**RESULT 2**")
if is_entailed_S:
    print(f"✅ YES, the Knowledge Base entails '{query_S}'.")
else:
    print(f"❌ NO, the Knowledge Base does not entail '{query_S}'.")
    print("The KB contains no information about 'S', so it cannot be proven true.")
print("="*40)
