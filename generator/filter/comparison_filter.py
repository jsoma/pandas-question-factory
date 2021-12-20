from ..column_manipulator import ColumnManipulator
from ..globals import *
from .filter import Filter
import random

class ComparisonFilter(Filter):
    
    NEEDS_WRAP = True

    COMPARISONS = {
        'less than': '<',
        'greater than': '>',
        'greater than or equal to': '>=',
        'less than or equal to': '<=',
        'equal to': '=='
    }
    
    def set_desc(self):
        self.desc = f"{self.colname} is {self.comparison} {self.target}"

    def set_code(self):
        self.code = f"{DF_COLUMN} {self.COMPARISONS[self.comparison]} {self.target}"

    def populate(self):
        self.comparison = random.choice(list(self.COMPARISONS.keys()))
        
        if self.comparison.endswith('equal to'):
            self.target = random.choice(self.df[self.colname].dropna().unique())
        else:
            anchor = random.randint(25, 75) / 100
            self.target = self.df[self.colname].quantile(anchor).round(2)

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols['data_type'].isin(['int64', 'float64']))
        ].index)