from xml.etree.ElementTree import Element

from node.answer.answer import Answer, GameAnswer, ArgumentAnswer

DEFAULT: str = "default"
ARGUMENT: str = "argument"
GAME: str = "game"


def get_answer(xml_node: Element) -> Answer:
    answer: Answer
    answer_type: str = xml_node.get("type")

    if answer_type == GAME:
        answer = GameAnswer(answer_type)
    elif answer_type == ARGUMENT:
        answer = ArgumentAnswer(answer_type)
    else:
        answer = Answer(answer_type)

    answer.initialize(xml_node)

    return answer
