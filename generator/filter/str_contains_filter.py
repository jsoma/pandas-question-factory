from ..globals import *
from .filter import Filter
import random

class StrContainsFilter(Filter):
    
    def set_desc(self):
        self.desc = f"{self.colname} contains the text '{self.word}'"

    def set_code(self):
        self.code = f"{DF_COLUMN}.str.contains('{self.word}')"

    def populate(self):
        self.word = random.choice(self.cols.loc[self.colname].most_common_words)
        
    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols['avg_spaces'] > 2)
        ].index)