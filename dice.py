from collections import Counter
import random
import re

from .base import MessageHandler
from ..util import parse_int

class DiceHandler(MessageHandler):

  TRIGGERS = ['dice', 'roll']
  HELP = 'roll the given number of dice; default 1'

  def handle_message(self, event, triggers, query):
    # Convert query into this format {number_of_dice}D{number_of_sides} {modifier}
    number_of_dice = re.search('[0-9]*\s*(?=d)', query, flags=re.IGNORECASE)
    if number_of_dice != None:
        number_of_dice = number_of_dice.group()
    if number_of_dice == '':
        number_of_dice = 1
    try:
        number_of_dice = int(number_of_dice)
    except:
        return 'Unable to determine number of dice to roll from input of "%s"' %(query)
    
    number_of_sides = re.search('(?<=d)\s*[1-9][0-9]*', query, flags=re.IGNORECASE)
    if number_of_sides != None:
        number_of_sides = number_of_sides.group()
    if number_of_sides == '':
        number_of_sides = 20
    try:
        number_of_sides = int(number_of_sides)
    except:
        return 'Unable to determine the number of sides for the dice to roll from input of "%s"' %(query)
    
    modifiers = re.search('[\+\-\*\/]+\s*[0-9]+', query)
    if modifiers != None:
        modifiers = modifiers.group()
    
    results = 0
    for result in (random.randrange(1, number_of_sides + 1) for _ in xrange(number_of_dice)):
        results += result
    if modifiers != '' and modifiers != None:
        results = eval('%s%s' %(results, modifiers))

    return str(results)
