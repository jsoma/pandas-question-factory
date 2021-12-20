from .groupby import GroupBy

class CategoryGroupBy(GroupBy):

    def set_desc(self):
        self.desc = f"for each value of {self.colname}"

    def set_code(self):
        self.code = f".groupby('{self.colname}')"

    def populate(self):
        pass

    @staticmethod
    def column_options(cols):
        return list(cols[
            (cols.data_type == 'object') &
            (cols.pct_unique > 0.3) &
            (cols.pct_unique < 0.8)
        ].index)