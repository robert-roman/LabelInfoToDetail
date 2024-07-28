from flask import Flask, request, jsonify
from PIL import Image
from ImageToText import imageToText
from DataBase.compound_db_client import CompoundDBClient
from BasicRestAPIs import simpleClient

currentDB = CompoundDBClient(host="localhost",
                             user="root",
                             password="parola123",
                             database="food_ingredients")
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Read and display the image
        image = Image.open(file)
        image_text = imageToText(image)
        print({"message": f"image text is: {image_text}"}), 200
        ingredientsList = simpleClient.getIngredientsList(image_text)
        ingredientsDetails = simpleClient.getIngredientsDetails(ingredientsList)
        return jsonify({"message": f"Ingredients details:\n{ingredientsDetails}"}), 200


if __name__ == "__main__":
    app.run(debug=True)
