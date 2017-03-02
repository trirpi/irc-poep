import random
import requests
import sys

import settings

from controllers.karma import KarmaController

control_karma = KarmaController(settings.karma_file)

insulting_sentences = [
    "you triggered bro!?",
    "Je hebt minder stijl dan een krultang",
    "zoek een leven (http://zoekeenleven.be)",
    "meeloper!",
    "oliebol!",
    "dommerik!",
    "stout kind!",
    "je bent net een baby.",
    "je lijkt op een blobvis"
]

eightball_sentences = [
    "ja",
    "nee",
    "natuurlijk",
    "de tijd zal het uitwijzen",
    "je mama weet het antwoord",
    "vraag het aan Sling",
    "hoe moet ik dat weten, verdomme"
]



def dis(arg, user):
    if user in settings.admin:
        return arg + ": " + random.choice(insulting_sentences)
    else:
        return "Jij bent geen admin!"


def bedank(arg, person):
    return person + ": graag gedaan"


def quit(arg, person):
    if person in settings.admin:
        sys.exit()
    else:
        return "Jij bent geen admin!"


def urban_dict(arg, person):
    urb_url = 'http://api.urbandictionary.com/v0/define?term='
    json_data = requests.get(urb_url + arg).json()
    return json_data["list"][0]["definition"]


def increment_karma(arg, person):
        control_karma.add_karma_item(arg)
        return control_karma.increment_karma(arg)


def decrement_karma(arg, person):
    control_karma.add_karma_item(arg)
    return control_karma.decrement_karma(arg)


def get_karma(arg, person):
    control_karma.add_karma_item(arg)
    return control_karma.get_karma(arg)


def love(arg, person):
    return "there is " + str(random.randint(0, 100)) + "% love between " + person + " and " + arg + "."


def eightball(arg, person):
    if arg != '' and len(arg) > 5:
        return random.choice(eightball_sentences)
    else:
        return "Ben je lang ofzo? Stel me een ja/nee-vraag"


def fortune(arg, person):
    with open(settings.fortune_file, 'r') as f:
        fortunes = f.readlines()
    return random.choice(fortunes)


def ban(arg, person):
    if person in settings.admin:
        settings.banned.append(arg)
        return "user " + arg + " is gebanned van " + settings.nickname + " voor deze sessie"


def oke(arg, person):
    return "is goed"


def sorry(arg, person):
    return person + ": sorry, m'love"


def help(arg, person):
    return "https://github.com/trirpi/irc-poep/blob/master/README.md"


callbacks = [
    (["dis", "naai", "vermorzel"], dis),
    (["dankjewel", "tnx", "dankje", "dankuwel", "danku", "thanks", "thnx"], bedank),
    (["flikker", "rot", "optyfen", "optiefen"], quit),
    (["urban", "ud"], urban_dict),
    (["plus", "++"], increment_karma),
    (["min", "minus", "--", "verminder"], decrement_karma),
    (["karma", "get"], get_karma),
    (["liefde", "love"], love),
    (["eight", "eightball", "yesorno", "jaofnee"], eightball),
    (["fortune", "oh-fortuna", "meester", "oke-is-goed"], fortune),
    (["ban", "verwijder", "tering", "stommerik", "gaweg"], ban),
    (["oke"], oke),
    (["sorry", "ikdeedietsverkeerd", "ikbeneenoliebol", "iklijkzelfookopeenblobvis"], sorry),
    (["help"], help)
]


def handle_message(command, arg, user):
    """
    function handles message when input starts with control_char or ends with nick
    then it gives an answer
    :param command: the command that needs to be executed
    :param arg: the argument (all the text after the command)
    :param user: the user who sended the text
    :return: string with answer
    """

    for (options, func) in callbacks:
        if command in options:
            return func(arg, user)
