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

# @app.route("/")
# def home():
#     return "haida varule"


@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data), 201


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
        image.show()
        image_text = imageToText(image)
        print({"message": f"image text is: {image_text}"}), 200
        ingredientsList = simpleClient.getIngredientsList(image_text)
        ingredientsDetails = simpleClient.getIngredientsDetails(ingredientsList)
        return jsonify({"message": f"Ingredients details:\n{ingredientsDetails}"}), 303


if __name__ == "__main__":
    app.run(debug=True)
