from ..globals import *
from .filter import Filter
import random

class IsinFilter(Filter):

    def set_desc(self):
        words_as_list = "\n* ".join(self.words)

        if self.not_in:
            self.desc = f"{self.colname} is not one of:\n* {words_as_list}\n"
        else:
            self.desc = f"{self.colname} is one of:\n* {words_as_list}\n"
    
    def set_code(self):
        words_as_list = ', '.join([f"\"{word}\"" for word in self.words])
        self.code = f"{DF_COLUMN}.isin([{words_as_list}])"
        if self.not_in:
            self.code = "~" + self.code

    def populate(self):
        max_unique = self.df[self.colname].nunique()
        min_list_size = 3
        max_list_size = min(max_unique - 2, 5)
        n = random.randint(min_list_size, max_list_size)

        self.words = random.sample(list(self.df[self.colname].dropna().unique()), n)
        if random.random() > 0.9:
            self.not_in = True
        else:
            self.not_in = False

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols['unique'] > 5) & 
            (cols['avg_spaces'] < 2)
        ].index)