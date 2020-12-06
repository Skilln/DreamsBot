import config
import telebot
import scenario
from telebot import types

from node.answer.answer import Answer, ArgumentAnswer
from node.game_handler import process_arg
from node.node import Node, GameNode

bot = telebot.TeleBot(config.TOKEN)

scenario.load("scenario.xml")
node_index: int = 0
current_node: Node = scenario.nodes[0]

@bot.message_handler(commands=['start'])
def start(message):
    global current_node

    current_node = scenario.nodes[0]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for answer in current_node.answers:
        item = types.KeyboardButton(answer.text)
        markup.add(item)

    bot.send_message(message.chat.id, current_node.text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    global node_index
    global current_node

    answers: Answer = current_node.answers

    for answer in answers:
        if answer.text == message.text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            if type(answer) is ArgumentAnswer:
                process_arg(answer.argument)

            if current_node.check_condition(answer):

                node_index = answer.next_node_id
                current_node = scenario.get_node_by_id(node_index)

            for nextAnswer in current_node.answers:
                item = types.KeyboardButton(nextAnswer.text)
                markup.add(item)

            bot.send_message(message.chat.id, current_node.get_text(), reply_markup=markup)


bot.polling(none_stop=True)
