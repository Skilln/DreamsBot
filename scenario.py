import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from node import node_factory
from node.node import Node

nodes = []


def load(file):
    data = ET.parse(file)
    root: Element = data.getroot()
    xml_nodes = root.findall("node")

    for xml_node in xml_nodes:
        nodes.append(node_factory.get_node(xml_node))


def get_node_by_id(index: int) -> Node:
    for node in nodes:
        if node.node_index == index:
            return node
    return None