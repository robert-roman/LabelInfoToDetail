from DataBase.compound_db_client import CompoundDBClient
from ImageToText import imageToText
from PIL import Image
from BasicRestAPIs import simpleClient, simpleServer
import requests

currentDB = CompoundDBClient(host="localhost",
                             user="root",
                             password="parola123",
                             database="food_ingredients")

image_path = Image.open("Images/onlyText.png")
# image.show()
# image_text = imageToText(image)
# print(image_text)

BASE = "http://127.0.0.1:5000/"

with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    response = requests.post(BASE, files=files)
    response = requests.post(url= BASE + "upload", files=files)
print(response.json())

# ingredientsList = simpleClient.getIngredientsList(image_text)
# print(ingredientsList)
# # for ingredient in ingredientsList:
# #     print(ingredient)
#
# databaseResults = currentDB.fetch_expanded_compounds(ingredientsList)
# print(databaseResults)
# for result in databaseResults:
#     print("INGREDIENT:")
#     print(databaseResults[result]['compound'])
#     print(len(databaseResults[result]['health_effects']))
#     for he in databaseResults[result]['health_effects']:
#         print(databaseResults[result]['health_effects'][he])


###verify database queries
# print("fetch expanded compounds test")
# x = (currentDB.fetch_expanded_compounds(["Bornyl acetate", "Betaine", "Butadiene-styrene rubber", "Cyanidin 3-(6''-acetyl-galactoside)"]))
# print(x.keys())
# print(x)
# for k in x:
#     print("new line \n")
#     print(x[k]["compound"]["name"])
#     print(len(x[k]["health_effects"]))
#     print(x[k]["health_effects"])
#     for effect in x[k]["health_effects"]:
#         print(x[k]["health_effects"][effect]["name"], x[k]["health_effects"][effect]["id"])
#     # print(x[k]["health_effects"])
#     # print(x[k]["name"])

