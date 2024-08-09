from pysat.formula import CNF
from pysat.solvers import Solver


class KnowledgeBase:
    def __init__(self):
        self.formula = CNF()

    @staticmethod
    def standardize_clause(clause):
        return sorted(list(set(clause)))

    def add_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.formula:
            self.formula.append(clause)

    def del_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause in self.formula:
            self.formula.remove(clause)

    def infer(self, not_alpha):
        with Solver(bootstrap_with=self.formula) as solver:
            for clause in not_alpha:
                if not isinstance(clause, list):
                    clause = [clause]
                solver.add_clause(clause)
            return not solver.solve()


# Example usage:

# # Create a new knowledge base
# kb = KnowledgeBase()

# # Add some clauses to the knowledge base
# kb.add_clause([1, -2])  # Clause: x1 ∨ ¬x2
# kb.add_clause([-1, 2])  # Clause: ¬x1 ∨ x2

# # Define some clauses to infer
# not_alpha = [
#     [-1, -2]
# ]  # Clauses to check if they are implied by the knowledge base (¬x1 ∨ ¬x2)

# # Perform inference
# is_implied = kb.infer(not_alpha)

# # Output result
# print(
#     f"Is the clause {not_alpha} implied by the knowledge base? {'Yes' if is_implied else 'No'}"
# )
