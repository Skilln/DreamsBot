from xml.etree.ElementTree import Element

from node.node import Node, GameNode, FinalNode

TEXT: str = "text"
GAME: str = "game"
FINAL: str = "final"


def get_node(xml_node: Element) -> Node:
    node: Node
    node_type: str = xml_node.get("type")
    node_index: int = int(xml_node.get("id"))

    if node_type == GAME:
        node = GameNode(node_type, node_index)
    elif node_type == FINAL:
        node = FinalNode(node_type, node_index)
    else:
        node = Node(node_type, node_index)

    node.initialize(xml_node)

    return node
