from ..globals import *
import random
from . import Aggregation

class NumericAgg(Aggregation):
        
    OPTIONS = [
        'sum', 'median', 'mean'
    ]

    def set_desc(self):
        self.desc = f"calculate the {self.aggfunc} of {self.colname}"

    def set_code(self):
        self.code = f"{COLUMN}.{self.aggfunc}()"

    def populate(self):
        self.aggfunc = random.choices(self.OPTIONS)[0]

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols['data_type'].isin(['int64', 'float64'])) &
            (cols['entropy'] > 3)
        ].index)