from ..globals import *
from .. import ColumnManipulator
import random

class Aggregation(ColumnManipulator):

    @staticmethod
    def select_one(df, cols):
        from . import NumericAgg, TopNAgg, ValueCountsAgg

        aggs = {
            NumericAgg: 80,
            TopNAgg: 40,
            ValueCountsAgg: 40
        }
        aggs = random.choices(list(aggs.keys()), weights=list(aggs.values()), k=len(aggs))
        for agg in aggs:
            options = agg.column_options(cols)
            if len(options) > 0:
                return agg(df, random.choice(options), cols=cols)




