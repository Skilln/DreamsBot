from xml.etree.ElementTree import Element

from node.answer import answer_factory
from node.answer.answer import Answer, GameAnswer
from node.game_handler import process_arg, get_final


class Node:
    node_type: str = ""
    node_index: int = -1
    text: str = ""
    answers: Answer

    def __init__(self, node_type: str, node_index: int):
        self.node_type = node_type
        self.node_index = node_index

    def initialize(self, xml_node: Element):
        text_node: Element = xml_node.find("text")
        answers_node: Element = xml_node.find("answers")

        if text_node is None:
            print("Error reading xml!  \'text\' node doesn't exist!")
            return
        else:
            self.text = text_node.text

        if answers_node is None:
            print("Error reading xml!  \'answers\' node doesn't exist!")
            return
        else:
            answers_elements = answers_node.findall("answer")
            temp_answer = []

            for answer in answers_elements:
                temp_answer.append(answer_factory.get_answer(answer))

            self.answers = temp_answer

    def check_condition(self, answer: Answer) -> bool:
        return True

    def check_answer(self, message: str) -> bool:
        for answer in self.answers:
            if answer.text == message:
                return True
        return False

    def get_text(self) -> str:
        return self.text


class GameNode(Node):
    success_points: int = 0
    fail_points: int = 0

    goal_success_point: int = 0
    goal_fail_points: int = 0

    success_node_id: int = -1
    fail_node_id: int = -1

    success_text: str = ""
    fail_text: str = ""

    success_arg: str = ""
    fail_arg: str = ""

    status: str = ""

    def __init__(self, node_type: str, node_index: int):
        super().__init__(node_type, node_index)

    def initialize(self, xml_node: Element):
        super().initialize(xml_node)

        self.status = self.text;

        self.goal_success_point = int(xml_node.find("goal").text)
        self.goal_fail_points = int(xml_node.find("fail").text)
        self.success_node_id = int(xml_node.find("success_id").text)
        self.fail_node_id = int(xml_node.find("fail_id").text)

        self.success_text = xml_node.find("success_text").text
        self.fail_text = xml_node.find("fail_text").text

        self.success_arg = xml_node.find("success_arg").text
        self.fail_arg = xml_node.find("fail_arg").text

    def check_condition(self, answer: GameAnswer) -> bool:
        if answer.check_chance():
            self.success_points += 1
            self.status = self.success_text
        else:
            self.fail_points += 1
            self.status = self.fail_text

        if self.success_points >= self.goal_success_point:
            answer.next_node_id = self.success_node_id
            process_arg(self.success_arg)
            return True
        elif self.fail_points >= self.goal_fail_points:
            answer.next_node_id = self.fail_node_id
            process_arg(self.fail_arg)
            return True
        return False

    def check_answer(self, message: str) -> bool:
        is_game_message: bool = message == self.success_text | message == self.fail_text

        return is_game_message | super().check_answer(message)

    def get_text(self) -> str:
        return self.status


class FinalNode(Node):

    finales = []

    def __init__(self, node_type: str, node_index: int):
        super().__init__(node_type, node_index)

    def initialize(self, xml_node: Element):
        super().initialize(xml_node)

        finale_node: Element = xml_node.find("finales")
        finale_nodes = finale_node.findall("final")
        temp = []
        for node in finale_nodes:
           temp.append(node.text)

        self.finales = temp

    def  get_text(self) -> str:
        return self.text + "\n" + self.finales[get_final()]
