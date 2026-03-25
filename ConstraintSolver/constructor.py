from .constraints import Constraint, Condition, relation
from .domain import Domain, DomainEdge, DomainNode
from .domino import Domino

class Gamedata:
    def __init__(self, data: dict | None):
        if data is None:
            raise ValueError("No data provided")

        self.dominoes = self.generate_dominoes(data)
        nodes = self.generate_nodes(data)
        edges = self.generate_edges(data, self.dominoes)
        constraints = self.generate_constraints(data)
        
        self.values = self.generate_values(data)
        
        self.variables = Domain(set().union(nodes.keys(), edges.keys()))
        self.domains = {**nodes, **edges}
        self.constraints = constraints
        
    def generate_values(self, game_data) -> dict[int, int]:
        """Used to initialise node domains with only available values"""
        value_dict = {}
        for domino in game_data["dominoes"]:
            for pip in domino:
                value_dict[pip] = value_dict.get(pip, 0) + 1
        return value_dict

    def generate_dominoes(self, game_data) -> set[Domino]:
        dominoes = set()
        for domino in game_data["dominoes"]:
            a, b = domino
            dominoes.add( Domino(a, b) )
            dominoes.add( Domino(b, a) ) # add flipped version as well
        return dominoes

    def generate_nodes(self, game_data) -> dict[str, DomainNode]:
        values = set(int(v) for v in self.generate_values(game_data).keys())
        nodes = {}
        for node in game_data["tiles"].keys():
            nodes[node] = DomainNode(values)
        return nodes

    def generate_edges(self, game_data, dominoes: set[Domino]) -> dict[str, DomainEdge]:
        edges = {}
        for node, neighbours in game_data["tiles"].items():
            for neighbour in neighbours:
                edge_name = f"{node}_{neighbour}"
                edges[edge_name] = DomainEdge(
                    node_a=node,
                    node_b=neighbour,
                    values=dominoes)
        return edges

    def generate_constraints(self, game_data) -> list[Constraint]:
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
            constraints.append(Constraint(
                nodes=nodes,
                target_value=target_value,
                condition=condition
            ))
        return constraints
    
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