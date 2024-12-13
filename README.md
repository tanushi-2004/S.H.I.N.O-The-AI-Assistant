# S.H.I.N.O - Smart Human-Interactive Neural Operator

S.H.I.N.O (Smart Human-Interactive Neural Operator) is a Python-based AI assistant powered by speech recognition and Google Gemini APIs. It can perform various tasks such as launching applications, browsing the web, responding to user queries, and more. S.H.I.N.O. also includes user authentication for personalized experiences.

## Features

- **Voice Commands**: S.H.I.N.O can recognize and execute voice commands using Google's Speech Recognition API.
- **AI Interaction**: Utilizes Google's Generative AI (Gemini) for generating responses to user queries.
- **Text-to-Speech**: Provides audio feedback using `pyttsx3` with customizable voice options (male/female).
- **User Authentication**: Secure user authentication using bcrypt for password hashing.
- **Web Browsing**: Opens websites directly via voice commands.
- **Application Launching**: Launches various applications like Notepad, Calculator, Camera, etc., based on user commands.
- **Time Inquiry**: Tells the current time.
- **Customizable AI Responses**: Responses are generated based on the user's queries, with AI-generated content saved to text files.
- **Music Playback**: Plays music stored on your system via voice command.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ChaitanyaNarang28/S.H.I.N.O-the-ai-assistant.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd S.H.I.N.O-the-ai-assistant
   ```
3. **Install Required Dependencies**:
   Make sure you have Python installed (preferably Python 3.7+).
   Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
   Required libraries include:
   - `speechrecognition`
   - `pyttsx3`
   - `bcrypt`
   - `google-generativeai`
   - `webbrowser`
   - `subprocess`
   - `os`
   - `datetime`

4. **Set Up Your API Key**:
   - Obtain a Google Gemini API key.
   - Create a file named `config.py` in the project directory and add your API key:
     ```python
     GENAI_API_KEY = 'your_google_gemini_api_key'
     ```

## Usage

1. **Run the AI Assistant**:
   ```bash
   python shino.py
   ```
   Follow the prompts to either register or sign in as a user.

2. **Interact with S.H.I.N.O.**:
   - Give voice commands to perform tasks.
   - Example commands:
     - "Open YouTube"
     - "Launch Notepad"
     - "What's the time?"
     - "Tell me about Python using AI"

3. **Customization**:
   - Change the AI voice by saying "Change voice to male" or "Change voice to female."
   - Reset the chat history by saying "Reset chat."

## Folder Structure

```
S.H.I.N.O-the-ai-assistant/
│
├── AI/                          # Directory where AI-generated responses are stored
├── users.txt                    # File for storing user credentials
├── shino.py                     # Main script for running the AI assistant
├── config.py                    # Configuration file for API keys
├── requirements.txt             # List of required Python packages
├── README.md                    # Project documentation (this file)
```

## Future Enhancements

- **Enhanced AI Capabilities**: Integrate more advanced AI models and features.
- **Voice-Activated Applications**: Expand the list of supported applications.
- **GUI Integration**: Provide a graphical user interface for easier interaction.
- **Cloud Support**: Store user data and chat history in the cloud for seamless cross-device experiences.

## Contributing

Contributions are welcome! Feel free to submit issues, request features, or create pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Gemini AI**: For providing the AI capabilities.
- **Python Community**: For the various libraries that made this project possible.

