from ..globals import *
import random
from . import Aggregation

class ValueCountsAgg(Aggregation):
    
    def set_desc(self):
        self.desc = f"count the frequency of each value of {self.colname}"
        options = []
        if self.as_pct:
            options.append("as a percent")
        if self.include_na:
            options.append("including missing values")
        if options:
            self.desc += " (" + ", ".join(options) + ") "
            
    def set_code(self):
        options = []
        if self.as_pct:
            options.append("normalize=True")
        if self.include_na:
            options.append("dropna=False")
        self.code = f"{COLUMN}.value_counts({', '.join(options)})"
    
    def populate(self):
        self.as_pct = random.random() > 0.75
        self.include_na = random.random() > 0.8

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols.data_type == 'object') &
            (cols.pct_unique < 0.3)
        ].index)