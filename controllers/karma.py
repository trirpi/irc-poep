import pickle


class KarmaController(object):

    def __init__(self, karma_file):
        self.karma_file = karma_file
        self.karma_dict = pickle.load(open(karma_file, 'rb'))

    def save_karma(self):
        pickle.dump(self.karma_dict, open(self.karma_file, 'wb'))

    def get_karma(self, word):
        return "karma van " + word + " is " + str(self.karma_dict[word])

    def add_karma_item(self, word):
        if word not in self.karma_dict:  # if the word does not exist
            self.karma_dict[word] = 0
            self.save_karma()
            return word + " added"
        else:
            return word + "allready in dict"

    def increment_karma(self, word):
        old_karma = self.karma_dict[word]
        self.karma_dict[word] = old_karma + 1
        self.save_karma()
        return "karma van " + word + " is nu " + str(old_karma + 1)

    def decrement_karma(self, word):
        old_karma = self.karma_dict[word]
        self.karma_dict[word] = old_karma - 1
        self.save_karma()
        return "karma van " + word + " is nu " + str(old_karma - 1)
