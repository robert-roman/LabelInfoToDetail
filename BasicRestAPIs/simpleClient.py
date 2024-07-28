import re
from DataBase.compound_db_client import CompoundDBClient
from deep_translator import GoogleTranslator
translator = GoogleTranslator(source="romanian", target="english")


currentDB = CompoundDBClient(host="localhost",
    user="root",
    password="parola123",
    database="food_ingredients")


def getIngredientsList(ingredientsString):
    ingredientsString = ingredientsString.replace('\n', ' ')
    ingredientsList = re.split(';|,|\.|\(|\)|:|  ', ingredientsString)
    ingredientsList = [ingredient.strip() for ingredient in ingredientsList if ingredient.strip()]
    # translatedIngredientsList = [translator.translate(ingredient.strip()) for ingredient in ingredientsList]
    # return translatedIngredientsList
    return  ingredientsList


# def getIngredientDetails(ingredient):
#     return currentDB.fetch_expanded_compound(ingredient)


def getIngredientsDetails(ingredientsList: list[str]):
    return currentDB.fetch_expanded_compounds(ingredientsList)
