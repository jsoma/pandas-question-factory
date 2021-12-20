from ..globals import *
import random
from . import Aggregation

class TopNAgg(Aggregation):
    
    def set_desc(self):
        self.desc = f"display the top {self.top_n} most common values in {self.colname}"
        if self.include_na:
            self.desc += ", including missing values"

    def set_code(self):
        options = []
        if self.include_na:
            options.append("dropna=False")
        self.code = f"{COLUMN}.value_counts({', '.join(options)}).head({self.top_n})"
    
    def populate(self):
        min_n = min(self.df[self.colname].nunique(), 3)
        max_n = min(self.df[self.colname].nunique(), 10)
        self.top_n = random.randint(min_n, max_n)
        self.targets = random.choices(self.df[self.colname].dropna().unique(), k=self.top_n)
        self.include_na = random.random() > 0.8

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols.data_type == 'object') &
            (cols.pct_unique > 0.3) &
            (cols.pct_unique < 0.8)
        ].index)