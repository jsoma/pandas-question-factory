import pandas as pd
import json

from generator import QuestionBank

countries = pd.read_csv("data/countries.csv")
countries['gdp'] = countries.gdp.round(-6)
countries['population'] = countries.population.round(-3)
countries['life_expectancy'] = countries.life_expectancy.round(1)

loans = pd.read_csv("data/china-loans-to-africa.csv")

cases = pd.read_csv("data/Medical_Examiner_Case_Archive.csv", nrows=10000)
cases['latitude'] = cases['latitude'].round(3)
cases['longitude'] = cases['longitude'].round(3)

datasets = [
    countries,
    loans,
    cases
]
bank = QuestionBank(datasets)
bank.generate_questions(100)
questions = bank.for_export()

with open("docs/questions.json", "w") as fp:
    json.dump(questions, fp)