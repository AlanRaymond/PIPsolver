from .constraints import Constraint, Condition, ConstraintAllEqual, ConstraintAllNotEqual
from .domain import Domain, DomainEdge, DomainNode
from .domino import Domino

class Gamedata:
    def __init__(self, data: dict | None):
        if data is None:
            raise ValueError("No data provided")

        self.values = generate_values(data)
        self.dominoes = generate_dominoes(data)
        nodes = generate_nodes(data, self.values)
        edges = generate_edges(data, self.dominoes)
        constraints = generate_constraints(data)
        
        self.variables = Domain(set().union(nodes.keys(), edges.keys()))
        self.domains = {**nodes, **edges}
        self.constraints = constraints
    
    def __str__(self):
        string = "Gamedata:\n"
        
        string += "Variables:\n"
        string += f"{self.variables.values}\n"
            
        string += "Domains:\n"
        for name, domain in self.domains.items():
            string += f"{name}: {domain}\n"
            
        string += "Constraints:\n"
        for constraint in self.constraints:
            string += f"{constraint}\n"
        return string
    
    
    
    
    
def generate_values(game_data) -> dict[int, int]:
    """Used to initialise node domains with only available values"""
    value_dict = {}
    for domino in game_data["dominoes"]:
        for pip in domino:
            value_dict[pip] = value_dict.get(pip, 0) + 1
    return value_dict

def generate_dominoes(game_data) -> set[Domino]:
    dominoes = set()
    for domino in game_data["dominoes"]:
        a, b = domino
        dominoes.add( Domino(a, b) )
        dominoes.add( Domino(b, a) ) # add flipped version as well
    return dominoes

def generate_nodes(game_data, value_dict) -> dict[str, DomainNode]:
    values = set(int(v) for v in value_dict.keys())
    nodes = {}
    for node in game_data["tiles"].keys():
        nodes[node] = DomainNode(values)
    return nodes

def generate_edges(game_data, dominoes: set[Domino]) -> dict[str, DomainEdge]:
    edges = {}
    for node, neighbours in game_data["tiles"].items():
        for neighbour in neighbours:
            edge_name = f"{node}_{neighbour}"
            edges[edge_name] = DomainEdge(
                node_a=node,
                node_b=neighbour,
                values=dominoes)
    return edges

def generate_constraints(game_data) -> list[Constraint]:
    condition_dict = {
        "EQUAL_TO": Condition.EQUAL_TO,
        "GREATER_THAN": Condition.GREATER_THAN,
        "LESSER_THAN": Condition.LESSER_THAN,
        "ALL_EQUAL": Condition.ALL_EQUAL,
        "ALL_NOT_EQUAL": Condition.ALL_NOT_EQUAL
    }

    constraints = []
    for constraint in game_data["constraints"]:
        nodes = tuple(constraint["tiles"])
        condition = condition_dict.get(constraint["condition"])
        target_value = constraint.get("target_value", None)
        
        if condition == Condition.ALL_EQUAL:
            constraints.append(
                ConstraintAllEqual(
                    nodes = nodes,
                    condition=condition,
                    values=generate_values(game_data)
                    )
                )
            continue
        if condition == Condition.ALL_NOT_EQUAL:
            constraints.append(
                ConstraintAllNotEqual(
                    nodes = nodes,
                    condition=condition
                )
            )
        
        constraints.append(Constraint(
            nodes=nodes,
            target_value=target_value,
            condition=condition
        ))
    return constraints