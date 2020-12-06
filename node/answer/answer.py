import random
from xml.etree.ElementTree import Element


class Answer:
    answer_type: str = ""
    text: str = ""
    next_node_id: int = -1

    def __init__(self, answer_type: str):
        self.answer_type = answer_type

    def initialize(self, xml_node: Element):
        text_node: Element = xml_node.find("text")
        next_node: Element = xml_node.find("next")

        if text_node is not None:
            self.text = text_node.text
        else:
            print("Error reading xml! \'text\' node doesn't exist!")
            return

        if next_node is not None:
            self.next_node_id = int(next_node.text)
        else:
            print("Error reading xml! \'next\' node doesn't exist!")


class ArgumentAnswer(Answer):
    argument: str = ""

    def __init__(self, answer_type: str):
        super().__init__(answer_type)

    def initialize(self, xml_node: Element):
        super().initialize(xml_node)

        self.argument = xml_node.get("arg")


class GameAnswer(Answer):
    chance: float = 0.0

    def __init__(self, answer_type: str):
        super().__init__(answer_type)

    def initialize(self, xml_node: Element):
        super().initialize(xml_node)

        self.chance = float(xml_node.get("chance"))

    def check_chance(self) -> bool:
        rand: float = random.uniform(0, 1)
        return rand <= self.chance

