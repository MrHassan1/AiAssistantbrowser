# Developed by Waatmani
# Facebook: Facebook.com/waatmani
# Instagram: Instagram.com/waatmanii

import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_handler import AgentHandler
import atexit

app = Flask(__name__)
# Enable CORS to allow requests from the extension
CORS(app)

print("Initializing agent handler (Gemini)...")
agent_handler = AgentHandler(provider='gemini')
print("Agent handler (Gemini) initialized.")

@app.route('/')
def index():
    return "Gemini Agent server is running!"

@app.route('/decide-action', methods=['POST'])
def decide_action_route():
    data = request.get_json()
    if not data or 'task' not in data or 'page_info' not in data:
        return jsonify({'error': 'Task or page_info not provided'}), 400

    task = data['task']
    page_info = data['page_info']
    print(f"Received task: {task}")
    # print(f"Received page_info: {page_info}") # Too verbose for regular logging

    try:
        # Call the agent handler to decide the next action
        ai_decision = agent_handler.decide_action(task, page_info)
        print(f"AI decision: {ai_decision}")
        return jsonify(ai_decision)
    except Exception as e:
        print(f"Error making AI decision: {e}")
        return jsonify({'action': {'type': 'error'}, 'result': str(e)}), 500

if __name__ == '__main__':
    # Running on port 5000 as expected by the extension
    app.run(host='0.0.0.0', port=5000)
