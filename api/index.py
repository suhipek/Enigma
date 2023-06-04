from flask import Flask, send_file, request
import anthropic
import prompt as prm
import re
import os
from sdai import insert_img
import traceback

app = Flask(__name__)
client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.post('/play')
def response_message():
    try:
        # print(request.json)
        preset = request.json['preset']
        prompt = prm.prompt.format(prm.puzzles[preset][0], prm.puzzles[preset][1])
        for message in request.json['messages']:
            if "bot" in message:
                prompt += f"{anthropic.AI_PROMPT} {message['bot']}"
            if "user" in message:
                prompt += f"{anthropic.HUMAN_PROMPT} {message['user']}"
        prompt += f"{anthropic.AI_PROMPT}"
        prompt = re.sub(r'<img[^>]*>', '[An image]', prompt)

        print(prompt)
        response = client.completion(
            prompt=prompt,
            stop_sequences = [anthropic.HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=100,
        )
        print(response['completion'])
        completion = insert_img(response['completion'])
        return {'message': completion}
    except:
        return {'message': traceback.format_exc()}



# @app.get('/play/<preset>')
# def play_page(preset):
#     return send_file('play.html')

# @app.get('/')
# def index_page():
#     return send_file('list.html')

# if __name__ == '__main__':
#     app.run(debug=True)