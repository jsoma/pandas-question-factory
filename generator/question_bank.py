from .question import Question
from tqdm import tqdm
import numpy as np

class QuestionBank:

    def __init__(self, dfs):
        self.dfs = dfs
    
    def generate_questions(self, n=10):
        self.questions = []
        for id, df in enumerate(self.dfs):
            print(f"Processing dataset {id+1} of {len(self.dfs)}")
            for _ in tqdm(range(n), smoothing=0):
                q = Question(df).for_export()
                q['dataset_id'] = id
                self.questions.append(q)

    def for_export(self):
        return {
            'datasets': [df.sample(5).replace([np.nan], [None]).to_dict(orient='records') for df in self.dfs],
            'questions': self.questions
        }