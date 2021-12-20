import random
from .. import ColumnManipulator

class GroupBy(ColumnManipulator):

    @staticmethod
    def select_one(df, cols):
        from . import CategoryGroupBy
        
        groupbys = {
            CategoryGroupBy: 80
        }
        groupbys = random.choices(list(groupbys.keys()), weights=list(groupbys.values()), k=len(groupbys))
        for groupby in groupbys:
            options = groupby.column_options(cols)
            if len(options) > 0:
                return groupby(df, random.choice(options), cols=cols)