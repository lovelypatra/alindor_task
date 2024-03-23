from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

model_id = 'gpt-3.5-turbo-1106'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Checking if a file was uploaded
    if 'file' not in request.files:
        return render_template('error.html', message='No file uploaded.')

    file = request.files['file']

    # Checking if the file is empty or not
    if file.filename == '':
        return render_template('error.html', message='Empty file uploaded.')

    # Reading the uploaded file
    text = file.read().decode('utf-8')

    #sentiment analysis
    response = openai.Completion.create(
        engine=model_id,
        prompt=text,
        max_tokens=50
    )

    #insights from OpenAI response
    insights = response.choices[0].text.strip()

    return render_template('result.html', insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
