from ..globals import *
from .filter import Filter
import random

class NaFilter(Filter):

    def set_desc(self):
        if self.missing:
            self.desc = f"{self.colname} is missing"
        else:
            self.desc = f"{self.colname} is not missing"

    def set_code(self):
        if self.missing:
            self.code = f"{DF_COLUMN}.isna()"
        else:
            self.code = f"{DF_COLUMN}.notna()"
    
    def populate(self):
        self.missing = random.random() > 0.75

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols.pct_missing > 0.1) & 
            (cols.pct_missing < 0.9)
        ].index)
