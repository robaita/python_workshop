from flask import Flask, render_template, jsonify, request
from datetime import datetime
from lib import text_to_image_generation_api

# Example usage
prompt = "A futuristic cityscape at night with neon lights"


app = Flask(__name__)
task_status = {"completed": False, "file_path":""}
prompt = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image',methods=['POST'])
def generate_image():
   
    prompt = ""
    try:
        prompt = request.form['prompt']
    except:
        prompt = ""
        pass

    print("prompt")
    print(prompt)

    print("Calling API...")
    image_data = text_to_image_generation_api(prompt)
    file_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+".png"
    file_path = "static/images/"+file_name
    print(file_path)
    print("Received Responce... Saving File...")
    if image_data:
        with open(file_path, "wb") as f:
            f.write(image_data)
        print(f"Image generated and saved as {file_name}")
    else:
        print("Failed to generate image.")

    return jsonify({"status": "completed", "file_path": file_path})

if __name__ == '__main__':
    app.run(debug=True)
