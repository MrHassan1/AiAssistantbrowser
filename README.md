# AI Assistant Browser Extension

A powerful browser extension that uses autonomous AI agents to perform tasks on web pages. It supports multiple AI providers including Groq, OpenAI, and Google Gemini.

## Features

- **Autonomous Actions**: The agent can click, type, and navigate to complete complex tasks.
- **Multi-Provider Support**: Choose between Groq (Llama 3.3), OpenAI (GPT-4o), or Google Gemini.
- **Privacy-Focused**: Your API keys are stored locally and requests are proxied through your own local server.

## Installation

### 1. Backend Setup

Prerequisites: Python 3.8+

1.  Navigate to the project directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure environment variables:
    - Rename `.env.example` to `.env`.
    - Open `.env` and add your API keys for the providers you wish to use.

### 2. Extension Setup (How to Load in Browser)

The extension must be loaded manually as it is a developer version.

1.  **Open Extensions Page**:
    - **Chrome**: Type `chrome://extensions` in the address bar.
    - **Edge**: Type `edge://extensions` in the address bar.
2.  **Enable Developer Mode**:
    - Look for the toggle switch named **"Developer mode"** (usually in the top right corner) and turn it **ON**.
3.  **Load the Extension**:
    - Click the button that says **"Load unpacked"**.
    - A file picker will open. Navigate to this `github` folder and select the `extension` subdirectory (e.g., `.../github/extension`).
4.  **Pin the Extension**:
    - Click the puzzle piece icon in your browser toolbar.
    - Find "AI Assistant" and click the pin icon to make it visible.

## Usage

### 1. Start the Server

You can run a server for the specific AI provider you want to use:

- **For Groq (Fast & Free Tier):**
  ```bash
  python groq_server.py
  ```

- **For OpenAI (GPT-4o):**
  ```bash
  python chatgp_server.py
  ```

- **For Google Gemini:**
  ```bash
  python gemini_server.py
  ```

The server will start on `http://localhost:5000`.

### 2. Use the Extension

1.  Open the browser side panel.
2.  Select "AI Assistant" from the dropdown.
3.  Enter a task (e.g., "Go to amazon.com and find a red stapler").
4.  Watch the agent perform the task autonomously!

## Troubleshooting

- **Quota Errors (429)**: If the agent stops working, check your API quota limits on the provider's website.
- **Server Errors**: Ensure the server is running and the `.env` file is correctly configured.


## Architecture

![System Architecture](https://github.com/MrHassan1/AiAssistantbrowser/blob/main/architecture_diagram.png)

## Workflow

![User Workflow](https://github.com/MrHassan1/AiAssistantbrowser/blob/main/workflow_diagram.png)

## Credits




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

** by Waatmani**

- Facebook: [Facebook.com/waatmani](https://facebook.com/waatmani)
- Instagram: [Instagram.com/waatmanii](https://instagram.com/waatmanii)




