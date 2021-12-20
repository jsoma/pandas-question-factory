from ..globals import *
from .filter import Filter
import random

class MatchFilter(Filter):
    
    NEEDS_WRAP = True

    def set_desc(self):
        if self.equality:
            self.desc = f"{self.colname} is {self.selection}"
        else:
            self.desc = f"{self.colname} is not {self.selection}"

    def set_code(self):
        if self.equality:
            self.code = f"{DF_COLUMN} == '{self.selection}'"
        else:
            self.code = f"{DF_COLUMN} != '{self.selection}'"
        
    def populate(self):
        self.selection = random.choice(self.df[self.colname].dropna().unique())
        self.equality = True if random.random() < 0.5 else False

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols.data_type == 'object') &
            (cols.pct_unique < 0.5) &
            (cols.avg_spaces < 2)
        ].index)
