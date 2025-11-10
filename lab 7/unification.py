from typing import Dict, List, Optional, Union, Any

# =========================
# Term classes
# =========================
class Term:
    def occurs(self, var: "Var", subst: Dict["Var", "Term"]) -> bool:
        raise NotImplementedError

    def apply(self, subst: Dict["Var", "Term"]) -> "Term":
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError


class Var(Term):
    def __init__(self, name: str):
        self.name = name

    def occurs(self, var: "Var", subst: Dict["Var", Term]) -> bool:
        # Apply current substitution to this variable then check
        applied = self.apply(subst)
        if isinstance(applied, Var):
            return applied.name == var.name
        return applied.occurs(var, subst)

    def apply(self, subst: Dict["Var", "Term"]) -> "Term":
        # If variable in substitution dictionary, return substituted term (apply recursively)
        for v in subst:
            if isinstance(v, Var) and v.name == self.name:
                return subst[v].apply(subst)
        return self  # unchanged

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("Var", self.name))


class Const(Term):
    def __init__(self, name: str):
        self.name = name

    def occurs(self, var: "Var", subst: Dict["Var", "Term"]) -> bool:
        return False

    def apply(self, subst: Dict["Var", "Term"]) -> "Term":
        return self

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Const) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("Const", self.name))


class Func(Term):
    def __init__(self, name: str, args: List[Term]):
        self.name = name
        self.args = args

    def occurs(self, var: "Var", subst: Dict["Var", "Term"]) -> bool:
        # occurs if var occurs in any argument after applying substitution
        return any(arg.apply(subst).occurs(var, subst) for arg in self.args)

    def apply(self, subst: Dict["Var", "Term"]) -> "Term":
        applied_args = [arg.apply(subst) for arg in self.args]
        return Func(self.name, applied_args)

    def __repr__(self) -> str:
        return f"{self.name}({', '.join(repr(a) for a in self.args)})"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Func)
            and self.name == other.name
            and len(self.args) == len(other.args)
            and all(a == b for a, b in zip(self.args, other.args))
        )

    def __hash__(self) -> int:
        return hash(("Func", self.name, tuple(self.args)))


TermLike = Union[Var, Const, Func]


# =========================
# Utility helpers
# =========================
def apply_subst_to_term(subst: Dict[Var, Term], term: TermLike) -> TermLike:
    return term.apply(subst)


def occurs_check(var: Var, term: TermLike, subst: Dict[Var, Term]) -> bool:
    """Return True if var occurs in term (considering current substitution)."""
    return term.apply(subst).occurs(var, subst)


def extend_subst(subst: Dict[Var, Term], var: Var, term: TermLike) -> Dict[Var, Term]:
    """Return a new substitution extended with var -> term, applying existing subst to term."""
    # Ensure we copy substitution to avoid mutation surprises
    new_subst = dict(subst)
    new_subst[var] = term.apply(new_subst)
    # Also apply new_subst to all existing substitution values (to keep normalized form)
    for v in list(new_subst.keys()):
        new_subst[v] = new_subst[v].apply(new_subst)
    return new_subst


# Pretty print substitution
def subst_to_str(subst: Optional[Dict[Var, Term]]) -> str:
    if subst is None:
        return "Failure (No Unifier)"
    if not subst:
        return "{}"
    pairs = [f"{v} -> {repr(t)}" for v, t in subst.items()]
    return "{ " + ", ".join(pairs) + " }"


# =========================
# The Unification Algorithm
# =========================
def unify(x: TermLike, y: TermLike, theta: Optional[Dict[Var, Term]] = None) -> Optional[Dict[Var, Term]]:
    """
    Unify terms x and y under substitution theta.
    Returns a substitution (dict Var->Term) or None if fails.
    """
    if theta is None:
        theta = {}

    # Apply current substitution to both terms
    x = x.apply(theta)
    y = y.apply(theta)

    # If identical after applying substitution -> success, return theta
    if x == y:
        return theta

    # If x is variable
    if isinstance(x, Var):
        return unify_var(x, y, theta)

    # If y is variable
    if isinstance(y, Var):
        return unify_var(y, x, theta)

    # If both are functions, check names and arity and unify arguments pairwise
    if isinstance(x, Func) and isinstance(y, Func):
        if x.name != y.name or len(x.args) != len(y.args):
            return None  # different functor or arity -> failure
        # unify arguments left-to-right, threading the substitution
        for a, b in zip(x.args, y.args):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta

    # If both are constants but not equal -> fail (caught earlier by x==y)
    return None


def unify_var(var: Var, x: TermLike, theta: Dict[Var, Term]) -> Optional[Dict[Var, Term]]:
    # If var already has a binding, unify its binding with x
    for v in theta:
        if v == var:
            return unify(theta[v], x, theta)

    # If x is variable and has binding, unify var with that binding
    if isinstance(x, Var):
        for v in theta:
            if v == x:
                return unify(var, theta[v], theta)

    # Occurs check: prevent var -> ...var...
    if occurs_check(var, x, theta):
        return None

    # Extend substitution
    new_theta = extend_subst(theta, var, x)
    return new_theta


# =========================
# Helper constructors for ease of examples
# =========================
def V(name: str) -> Var:
    return Var(name)


def C(name: str) -> Const:
    return Const(name)


def F(name: str, *args: TermLike) -> Func:
    # accept either list or multiple args
    flat_args = []
    for a in args:
        if isinstance(a, (list, tuple)):
            flat_args.extend(a)
        else:
            flat_args.append(a)
    return Func(name, flat_args)


# =========================
# Examples / Tests
# =========================
if __name__ == "__main__":
    examples = []

    # Example 1: unify X and a -> {X -> a}
    examples.append((V("X"), C("a")))

    # Example 2: unify f(X,g(Y)) and f(g(Z), g(a))
    examples.append((F("f", V("X"), F("g", V("Y"))), F("f", F("g", V("Z")), F("g", C("a")))))

    # Example 3: unify f(X) and g(X) -> fail
    examples.append((F("f", V("X")), F("g", V("X"))))

    # Example 4: occurs check: unify X and f(X) -> fail
    examples.append((V("X"), F("f", V("X"))))

    # Example 5: unify f(X,X) and f(a,b) -> fail (X would need to be both a and b)
    examples.append((F("f", V("X"), V("X")), F("f", C("a"), C("b"))))

    # Run examples
    for i, (t1, t2) in enumerate(examples, 1):
        theta = unify(t1, t2, {})
        print(f"Example {i}: unify({t1}, {t2})")
        print("  =>", subst_to_str(theta))
        print()
