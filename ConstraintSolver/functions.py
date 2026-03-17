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
        allowed_sets = constraint.relation(nodes)
        
        changed_nodes = set()
        for node, allowed_values in zip(constraint.nodes, allowed_sets):
            node_has_changed = domains[node].restrict_to(allowed_values)
            if node_has_changed:
                changed_nodes.add(node)
        return changed_nodes

def get_edges_for_node(node: str, domains: dict[str, Domain]) -> set[str]:
    # Get the edges associated with a node.
    edges = {edge for edge, domain in domains.items()
                    if isinstance(domain, DomainEdge) and 
                    node in {domain.node_a, domain.node_b}}
    return edges

def get_nodes_for_edge(edge: str, domains: dict[str, Domain]) -> tuple[str, str]:
    # Get the nodes associated with an edge.
    domain = domains[edge]
    if not isinstance(domain, DomainEdge):
        raise ValueError(f"{edge} is not an edge domain")
    return domain.node_a, domain.node_b

def update_edge_domain(edge: str, domains: dict[str, Domain]) -> bool:
    # Update the domain of an edge based on the domains of its associated nodes.
    node_a, node_b = get_nodes_for_edge(edge, domains)
    domain_a = domains[node_a]
    domain_b = domains[node_b]

    allowed_dominoes = set()
    for value_a in domain_a:
        for value_b in domain_b:
            domino = Domino(value_a, value_b)
            if domino in domains[edge]:
                allowed_dominoes.add(domino)
    
    return domains[edge].restrict_to(allowed_dominoes)

def update_node_domain(node: str, domains: dict[str, Domain]) -> bool:
    # Update the domain of a node based on the domains of its associated edges.
    edges = get_edges_for_node(node, domains)
    
    allowed_values = set()
    for edge in edges:
        edge_domain = domains[edge]
        if not isinstance(edge_domain, DomainEdge):
            raise ValueError(f"{edge} is not an edge domain")
        
        position = 0 if edge_domain.node_a == node else 1
        for domino in edge_domain:
            allowed_values.add(domino.values[position])
    
    return domains[node].restrict_to(allowed_values)

def get_neighbours(node: str, domains: dict[str, Domain], variables: list[str]) -> Domain:
    # Get the neighbours of a node based on the edges in the domains.
    #  The variables list indicates domains that are still active, and not null.
    # Returns a domain to enable properties like is_empty and is_singleton.
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

def remove_null_edges(domains: dict[str, Domain], variables: list[str]) -> list[str]:
    # Remove edges with empty domains from the variables list.
    null_edges = [edge for edge, domain in domains.items()
                    if edge in variables and isinstance(domain, DomainEdge) and domain.is_empty]
    for edge in null_edges:
        variables.remove(edge)
    return null_edges
    
def exclude_domino(edge: str, domain: dict[str, Domain]) -> set[str]:
    # if a edge domain becomes a singleton, that domino may exist in other domains
    if not domain[edge].is_singleton:
        raise ValueError(f"Domain {edge} is not a singleton.")
    
    value = domain[edge].values
    
    changed_edges = set()
    for v, d in domain:
        if not isinstance(d, DomainEdge) or v == edge:
            continue
        changed_edge = d[v].remove(value)
        if changed_edge:
            changed_edges.add(v)
    
    return changed_edges

            
