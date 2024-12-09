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

plants = pd.read_csv("data/powerplants.csv", usecols=[
    'plant_name', 'utility_name', 'sector_name', 'city', 'primary_source',	'total_mw',	'coal_mw', 'hydro_mw'
])

datasets = [
    countries,
    loans,
    cases,
    plants,
]
names = {
    'df': 100,
    'merged': 20,
    'df2': 20
}
bank = QuestionBank(datasets, df_names=names)
bank.generate_questions(100)
questions = bank.for_export()

with open("docs/questions.json", "w") as fp:
    json.dump(questions, fp)