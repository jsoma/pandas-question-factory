from collections import Counter
import numpy as np
from math import log, e
import random
from .filter import Filter
from .aggregation import Aggregation
from .groupby import GroupBy

class Question:
    
    def __init__(self, df, df_name='df'):
        if df.shape[0] > 1000:
            self.df = df.sample(1000)
        else:
            self.df = df
        self.filters = []
        self.aggregation = None
        self.groupby = None
        self.desc = None
        if df_name == 'random':
            names = {
                'df': 80,
                'merged': 20,
                'df2': 30
            }
            self.df_name = random.choices(names.keys(), weights=names.values())[0]
        else:
            self.df_name = df_name
        self.populate()
    
    def get_col_details(self):
        def _get_avg_str_len(col):
            try:
                col.str.len().mean()
            except:
                return
        
        def _get_avg_spaces(col):
            try:
                col.astype(str).str.split(" ").str.len().mean() - 1
            except:
                return
            
        def _str_contains_options(col):
            combined = col.astype(str).str.lower().str.replace("[^a-z]", " ", regex=True).str.split("\s+").sum()
            longer = [word for word in combined if len(word) > 3]
            words = [w[0] for w in Counter(longer).most_common(20)]
            if not words:
                return
            else:
                return words

        def _calc_entropy(col, base=None):
            labels = list(col.values)
            n_labels = len(labels)
            
            if n_labels <= 1:
                return 0

            value,counts = np.unique(labels, return_counts=True)
            probs = counts / n_labels

            n_classes = np.count_nonzero(probs)

            if n_classes <= 1:
                return 0

            ent = 0.

            # Compute entropy
            base = e if base is None else base
            for i in probs:
                ent -= i * log(i, base)

            return ent

        cols = self.df.describe(include='all').T
        cols['pct_missing'] = (self.df.shape[0] - cols['count']) / self.df.shape[0]
        cols['pct_unique'] = cols['unique'] / cols['count']
        cols['data_type'] = self.df.dtypes.apply(lambda t: str(t))
        cols['entropy'] = self.df.apply(_calc_entropy).dropna()
        cols['avg_str_len'] = self.df.select_dtypes('object').apply(_get_avg_str_len).dropna()
        cols['avg_spaces'] = self.df.select_dtypes('object').apply(_get_avg_spaces).dropna()
        cols['most_common_words'] = self.df.select_dtypes('object').apply(_str_contains_options).dropna()
        return cols
    
    def generate_filters(self):
        self.filters = []
        filter_count = random.choices([0, 1, 2, 3], weights=[20, 70, 30, 10])[0]
        for i in range(filter_count):
            self.add_filter()

    def get_used_colnames(self):
        cols = [f.colname for f in self.filters]
        
        if self.aggregation:
            cols.append(self.aggregation.colname)

        if self.groupby:
            cols.append(self.groupby.colname)
        
        return cols

    def add_filter(self):
        cols = self.get_col_details().drop(index=self.get_used_colnames())
        f = Filter.select_one(self.df, cols)
        if f:
            self.filters.append(f)
    
    def add_aggregate(self):
        self.aggregation = None
        cols = self.get_col_details().drop(index=self.get_used_colnames())
        a = Aggregation.select_one(self.df, cols)
        if a:
            self.aggregation = a
    
    def add_groupby(self):
        self.groupby = None
        cols = self.get_col_details().drop(index=self.get_used_colnames())
        g = GroupBy.select_one(self.df, cols)
        if g:
            if not self.aggregation:
                self.add_aggregate()
            if self.aggregation:
                self.groupby = g 
    
    def populate(self):
        self.generate_filters()
        if random.random() > 0.5:
            self.add_aggregate()
        if random.random() > 0.75:
            self.add_groupby()
        self.set_desc()
        self.set_code()
    
    def get_difficulty(self):
        return len(self.filters) + int(self.aggregation is not None) + int(self.groupby is not None)

    def set_desc(self):
        if self.df_name == 'df':
            self.desc = ""
        else:
            self.desc = f"for a dataframe named {self.df_name}, "

        if self.aggregation:
            self.desc += f" {self.aggregation.get_desc()}"
        else:
            self.desc = f"display all rows {self.desc}"

        if self.filters:
            self.desc += " where "
            wheres = [f.get_desc() for f in self.filters]
            self.desc += ' and '.join(wheres)

        if self.groupby:
            self.desc += f" {self.groupby.get_desc()}, "

        self.desc = self.desc.strip()

    def set_code(self):
        self.code = f"{self.df_name}"
        if self.filters and len(self.filters) == 1:
            self.code += "[" + self.filters[0].get_code() + "]"
        elif len(self.filters) > 1:
            filter_code = []
            for f in self.filters:
                code = f.get_code()
                if f.NEEDS_WRAP:
                    code = f"({code})"
                filter_code.append(code)
            self.code += f"[{' & '.join(filter_code)}]"
        if self.groupby:
            self.code += f"{self.groupby.get_code()}"
        if self.aggregation:
            self.code += f"{self.aggregation.get_code()}"

        self.code = self.code.format(df_name=self.df_name)

    def for_export(self):
        return {
            'desc': self.desc,
            'code': self.code,
            'difficulty': self.get_difficulty()
        }