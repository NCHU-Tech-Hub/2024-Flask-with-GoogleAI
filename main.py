import os

from flask import Flask, render_template, request
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
api_key = os.environ.get("api_key")

genai.configure(api_key=api_key)
generation_config = {
    "temperature": .7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 256,
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

@app.route('/', methods=['GET', 'POST'])
def chat():
    chat_history = []
    # Start a chat session with the history
    chat_session = model.start_chat(
        history=[
        ]
    )
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Get previous chat history from hidden form field
        previous_history = request.form.get('chat_history', '[]')
        chat_history = json.loads(previous_history)
        # Append the user's message to the chat history
        chat_history.append({'role': 'user', 'content': user_input})
        # Get the AI's response
        response_text = get_ai_response(user_input, chat_session)
        # Append the AI's response to the chat history
        chat_history.append({'role': 'assistant', 'content': response_text})
        # Render the template with the updated chat history
        return render_template(
            'chat.html',
            chat_history=chat_history,
            chat_history_json=chat_history  # Pass the list directly
        )

    # For GET requests, render the template with an empty chat history
    return render_template(
        'chat.html',
        chat_history=chat_history,
        chat_history_json=chat_history
    )

def get_ai_response(message, chat_session):
    # Prepare the messages for the chat session


    response = chat_session.send_message(message)

    return response.text
def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
