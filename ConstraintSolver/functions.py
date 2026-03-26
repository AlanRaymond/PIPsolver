'''
Helper functions for the constraint solver.
Assumes the solver class has the following attributes:
- self.variables: a set of variable names (strings)
- self.domains: a dictionary mapping variable names to their domains (sets of allowed values)
- self.constraints: a list of constraints, where each constraint is a function
    that takes in the current state of the domains and restricts the domains.
'''

from .constraints import Constraint
from .domain import Domain, DomainEdge
from .domino import Domino


def apply_constraint(domains: dict[str, Domain], constraint: Constraint) -> set[str]:
    nodes = tuple(domains[node] for node in constraint.nodes)
    allowed_sets = constraint.relation()(nodes)
        
    changed_nodes = set()
    for node, allowed_values in zip(constraint.nodes, allowed_sets):
        node_has_changed = domains[node].restrict_to(allowed_values)
        if node_has_changed:
            changed_nodes.add(node)
    return changed_nodes

def get_edges_for_node(node: str, domains: dict[str, Domain]) -> set[str]:
    '''Returns all edges associated with the input node'''
    edges = {edge for edge, domain in domains.items()
                    if isinstance(domain, DomainEdge) and 
                    node in {domain.node_a, domain.node_b}}
    return edges

def get_nodes_for_edge(edge: str, domains: dict[str, Domain]) -> tuple[str, str]:
    '''Returns node_a and node_b from the input edge'''
    domain = domains[edge]
    if not isinstance(domain, DomainEdge):
        raise ValueError(f"{edge} is not an edge domain")
    return domain.node_a, domain.node_b

def update_edge_domain(edge: str, domains: dict[str, Domain]) -> str:
    '''
    Update the domain of an edge using the values of its associated nodes.
    Returns the edge name for propagation.
    '''
    node_a, node_b = get_nodes_for_edge(edge, domains)
    domain_a = domains[node_a]
    domain_b = domains[node_b]

    allowed_dominoes = set()
    for value_a in domain_a:
        for value_b in domain_b:
            domino = Domino(value_a, value_b)
            if domino in domains[edge]:
                allowed_dominoes.add(domino)
    
    has_changed = domains[edge].restrict_to(allowed_dominoes)
    
    return edge if has_changed else ""

def update_node_domain(node: str, domains: dict[str, Domain]) -> bool:
    '''
    Update the domain of a node based on the domains of its associated edges.
    Return a boolean whether the domain has changed.
    Function used for data integrity, not propagation.
    '''
    edges = get_edges_for_node(node, domains)
    
    allowed_values = set()
    for edge in edges:
        edge_domain = domains[edge]
        if not isinstance(edge_domain, DomainEdge):
            raise ValueError(f"{edge} is not an edge domain")
        
        position = 0 if edge_domain.node_a == node else 1
        for domino in edge_domain:
            allowed_values.add(domino.values[position])
            
    has_changed = domains[node].restrict_to(allowed_values)
    
    return has_changed

def get_neighbours(node: str, domains: dict[str, Domain], variables: list[str]) -> Domain:
    '''
    Get the neighbours of a node based on the edges in the domains.
     The variables list indicates domains that are still active, and not null.
    Returns a domain to enable properties like is_empty and is_singleton.
    '''
    neighbours = set()
    for edge, domain in domains.items():
        if edge not in variables:
            continue
        if not isinstance(domain, DomainEdge):
            continue
        if node == domain.node_a:
            neighbour = domain.node_b
            neighbours.add(neighbour)
    return Domain(neighbours)


def exclude_domino(edge: str, domain: dict[str, Domain], variables) -> set[str]:
    '''
    Extracts the domino from the input edge and removes the domino from
    all other domain.
    Checks that the edge is a singleton.
    Returns all edges that have been changed for further propagation. 
    '''
    
    if not domain[edge].is_singleton:
        raise ValueError(f"Domain {edge} is not a singleton.")
    
    domino = list(domain[edge].values)[0]
    
    double = domino == domino.flipped()
    
    # if there are two singletons containing a double, then remove all other instances
    singletons_containing_domino = len(list(v for v, d in domain.items()
                                       if isinstance(d, DomainEdge) and
                                       domino in d and
                                       d.is_singleton))   
    
    changed_edges = set()
    
    for v, d in domain.items():      
        if v not in variables:
            continue
        if not isinstance(d, DomainEdge) or v == edge:
            continue
        if double and singletons_containing_domino == 2 and d.is_singleton:
            continue
        changed_edge = d.remove(domino)
        if changed_edge:
            changed_edges.add(v)
    
    return changed_edges

def collapse_neighbour(edge, domains, variables) -> bool:
    has_changed = domains[edge].restrict_to(set())
    if has_changed:
        variables.remove(edge)
    return has_changed

def restrict_neighbours(nodes, domains, variables) -> bool:
    '''
    
    '''
    changed = False
    for node in nodes:
        neighbours_a = get_neighbours(node, domains, variables)
        if neighbours_a.is_singleton:
            neighbour_a = neighbours_a.values.pop()
            neighbours_b = get_neighbours(neighbour_a, domains, variables)
            if not neighbours_b.is_singleton:
                collapsed_edges = [edge for edge in get_edges_for_node(neighbour_a, domains)
                                   if edge not in {f"{neighbour_a}_{node}", f"{node}_{neighbour_a}"}]
                for collapsed_edge in collapsed_edges:
                    changed |= collapse_neighbour(collapsed_edge, domains, variables)
    return changed

            