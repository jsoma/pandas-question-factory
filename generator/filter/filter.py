from .. import ColumnManipulator
import random

class Filter(ColumnManipulator):

    NEEDS_WRAP = False
    
    @staticmethod
    def select_one(df, cols):
        from . import StrContainsFilter, MatchFilter, NaFilter, IsinFilter, ComparisonFilter

        filters = [StrContainsFilter, MatchFilter, NaFilter, IsinFilter, ComparisonFilter]
        random.shuffle(filters)
        for f in filters:
            options = f.column_options(cols)
            if len(options) > 0:
                return f(df, random.choice(options), cols=cols)
