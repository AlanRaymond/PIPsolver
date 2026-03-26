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
from ConstraintSolver.functions import apply_constraint, exclude_domino, get_edges_for_node, get_nodes_for_edge, restrict_neighbours, update_edge_domain, update_node_domain

from .domino import Domino
from .domain import DomainEdge, DomainNode
from .constraints import Constraint

class Solver:
    def __init__(self, data: Gamedata):
        self.variables = data.variables
        self.domains = data.domains
        self.constraints = data.constraints
        
        self.dominoes = data.dominoes
        
        # Initialise game state
        self.apply_all_constraints()
    
    @property
    def nodes(self) -> iter:
        return [node for node in self.variables 
                if isinstance(self.domains[node], DomainNode)]
        
    @property
    def edges(self) -> iter:
        return [edge for edge in self.variables
                if isinstance(self.domains[edge], DomainEdge)]
    
    @property
    def singleton_edges(self) -> iter:
        return [edge for edge in self.edges
                if self.domains[edge].is_singleton]
    
    # ---------------------------------------------------------------------
    
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
    
    def collapse_neighbourhood(self) -> bool:
        collapsable = True
        while collapsable:
            collapsable = restrict_neighbours(self.nodes, self.domains, self.variables)
        return True
    
    def exclude_dominoes(self) -> None:
        '''
        Checks for edge domains that are singletons and removes domino from all other domains.
        Keeps track of edges that have already been processed.
        '''
        checked_edges = set()
        unchecked_edges = set(self.singleton_edges).difference(checked_edges)
        
        while unchecked_edges:
            edge = unchecked_edges.pop()
            checked_edges.add(edge)
            edges = exclude_domino(edge, self.domains, self.variables)
            for e in edges:
                nodes = set(get_nodes_for_edge(e, self.domains))
                for node in nodes:
                    update_node_domain(node, self.domains)
    
    def update_all_node_domains(self) -> None:
        '''
        Updates all node domains to match the values from their corresponding edges.
        Used to maintain data integrity.
        '''
        if all(node.is_singleton for name, node in self.domains.items()
               if name in self.nodes):
            return
        for node in self.nodes:
            update_node_domain(node, self.domains)
        
    # -----------------------------------------------------------------
    
    def advance(self) -> None:
        self.collapse_neighbourhood()
        self.exclude_dominoes()
        self.update_all_node_domains()
        self.apply_all_constraints()            
                    
    def __str__(self):
        string = "Gamestate:\n"
        for variable, domain in self.domains.items():
            if variable in self.variables:
                string += f"  {variable}: {domain}\n"
        return string