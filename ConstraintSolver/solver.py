# A constraint solver:
#  X - A set of variables.
#       Implemented using a list. Will contain the names for each domain.
#  D - A set of domains, one for each variable.
#       Implemented using a dictionary where keys are variable names and
#       values are lists of allowed values.
#  C - A set of constraints that restrict the values the variables can take.
#       Implemented using a list of functions that take in the current state
#       of the domains and restrict the domains.

from ConstraintSolver.constructor import Gamedata
from ConstraintSolver.functions import apply_constraint, get_edges_for_node, update_edge_domain

from .domino import Domino
from .domain import Domain, DomainEdge
from .constraints import Constraint

class Solver:
    def __init__(self, data: Gamedata):
        self.variables = data.variables
        self.domains = data.domains
        self.constraints = data.constraints
        
        self.dominoes = data.dominoes
        
    def apply_all_constraints(self) -> set[str]: # O(n_constraints * n_changed_nodes * n_edges_per_node)
        # Constraints are applied to the node domains.
        # If a node domain changes, then the edges need to be updated as well.
        for constraint in self.constraints:
            changed_nodes = apply_constraint(self.domains, constraint)
            changed_edges = set()
            for changed_node in changed_nodes:
                for edge in get_edges_for_node(changed_node, self.domains):
                    changed_edge = update_edge_domain(edge, self.domains)
                    changed_edges.add(changed_edge)
        return changed_edges

                    
                                      
    def is_solved(self) -> bool:
        solved = all(domain.is_singleton for variable, domain in self.domains
                     if variable in self.variables)

        return solved
                    
                    
    def __str__(self):
        string = "Gamestate:\n"
        for variable, domain in self.domains.items():
            if variable in self.variables:
                string += f"  {variable}: {domain}\n"
        return string