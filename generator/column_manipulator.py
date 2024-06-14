from .globals import *

class ColumnManipulator:
    
    def __init__(self, df, colname, cols=None):
        self.df = df
        self.colname = colname
        self.cols = cols
        self.populate()
        self.set_code()
        self.set_desc()

    def __str__(self):
        return f"{type(self).__name__}: \033[1mDescription:\033[0m {self.get_desc()}, \033[1mCode:\033[0m {self.get_code()}"
    
    def __repr__(self):
        return f"{type(self).__name__}({self.colname})"

    def get_code(self):
        return self.code.format(df_column=self.col_accessor(True), column=self.col_accessor())

    def get_desc(self):
        return self.desc.format(df_column=self.col_accessor(True), column=self.col_accessor())

    def col_accessor(self, include_df=False):
        # if ' ' in self.colname:
        col = f"['{self.colname}']"
        # else:
        #     col = f".{self.colname}"
        if include_df:
            return f"{DF}{col}"
        else:
            return col

    @staticmethod
    def select_one(df, cols):
        raise NotImplementedError   
    
    @staticmethod
    def column_options(cols):
        raise NotImplementedError   