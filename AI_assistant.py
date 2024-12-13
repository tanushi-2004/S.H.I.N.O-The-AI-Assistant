import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime
import subprocess
import google.generativeai as genai
import logging
from config import GENAI_API_KEY
import bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the recognizer once
recognizer = sr.Recognizer()

# Configure the genai API key and model once
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
)
chat_session = model.start_chat(history=[])

# Initialize TTS engine
engine = pyttsx3.init()

def log_message(message):
    logging.info(message)

def ai(prompt):
    log_message(f"AI prompt: {prompt}")
    response = chat_session.send_message(prompt)
    response_text = response.text
    print(response_text)
    save_to_file(response_text, prompt)

def save_to_file(text, prompt):
    if not os.path.exists("AI"):
        os.mkdir('AI')
    filename_suffix = prompt.split("AI")[1].strip() or "NoPromptText"
    filename = f"AI/{filename_suffix}.txt"
    try:
        with open(filename, "w") as f:
            f.write(f"AI response for prompt: {prompt}\n*********************\n\n{text}")
            print(f"Saved to {filename}")
    except Exception as e:
        log_message(f"Error saving file: {e}")

chatstr = ""
current_voice = 'female'

def chat(query):
    global chatstr
    log_message(f"User query: {query}")
    chatstr += f"Chaitanya: {query}\n Shino: "
    response = chat_session.send_message(chatstr)
    response_text = response.text

    # Limit response to 5 lines
    lines = response_text.split('\n')
    limited_response = '\n'.join(lines[:5])
    
    say(limited_response)
    chatstr += f"{response_text}\n"
    return limited_response

def say(text):
    global current_voice
    voices = engine.getProperty('voices')
    if current_voice == 'female':
        engine.setProperty('voice', voices[1].id)  # Female voice
    else:
        engine.setProperty('voice', voices[0].id)  # Male voice
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1)  # Reduce ambient noise adjustment duration
        recognizer.pause_threshold = 0.2  # Reduce pause threshold
        recognizer.non_speaking_duration = 0.1  # Reduce non-speaking duration
        
        try:
            audio = recognizer.listen(source, timeout=5)  # Add timeout to avoid hanging
            print("recognizing")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.WaitTimeoutError:
            log_message("Listening timed out while waiting for phrase to start")
            return "Sorry, I did not hear anything. Please try again."
        except sr.UnknownValueError:
            log_message("Google Speech Recognition could not understand audio")
            return "Sorry, I did not catch that."
        except sr.RequestError as e:
            log_message(f"Error with Google Speech Recognition service: {e}")
            return "Sorry, I'm having trouble connecting to the service."

def open_site(query):
    if "open" in query.lower():
        site_name = query.lower().split("open ")[1]
        url = f"https://{site_name}.com"
        say(f"Opening {site_name}")
        webbrowser.open(url)
        return True
    return False

def launch_application(app_name):
    app_commands = {
        "notepad": "notepad",
        "calculator": "calc",
        "camera": "start microsoft.windows.camera:",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "chrome": "start chrome"
        # Add more applications and their commands here
    }
    
    command = app_commands.get(app_name.lower())
    
    if command:
        try:
            subprocess.run(command, shell=True)
            say(f"Launching {app_name}")
        except Exception as e:
            log_message(f"Error launching {app_name}: {e}")
    else:
        say(f"Sorry, I don't know how to launch {app_name}")

def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open('users.txt', 'a') as file:
        file.write(f"{username}:{hashed_password.decode()}\n")
    print("User registered successfully!")

def authenticate_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split(':')
                if stored_username == username:
                    if bcrypt.checkpw(password.encode(), stored_password.encode()):
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password.")
                        return False
            print("Username not found.")
            return False
    except FileNotFoundError:
        print("No user data found. Please register first.")
        return False

def main():
    global current_voice

    if not os.path.exists('users.txt'):
        print("No user data found.")
        action = input("Would you like to [1] Register a new user or [2] Exit? (Enter 1 or 2): ").strip()
        if action == '1':
            register_user()
        else:
            print("Exiting...")
            exit()
    
    while True:
        action = input("Do you want to [1] Sign In or [2] Register a new user? (Enter 1 or 2): ").strip()
        if action == '1':
            authenticated = authenticate_user()
            if authenticated:
                break
        elif action == '2':
            register_user()
        else:
            print("Invalid option. Please enter 1 or 2.")

    print("Jai Siya Ram")
    say("Naammaastttaaa")
    say("SHINO this side")
    
    while True:
        print("Listening....")
        query = takeCommand()
        
        if 'change voice to female' in query.lower():
            current_voice = 'female'
            say("Voice changed to female.")
            continue
        
        if 'change voice to male' in query.lower():
            current_voice = 'male'
            say("Voice changed to male.")
            continue
        
        if open_site(query):
            continue
        
        if 'open music' in query:
            musicpath = r"C:\Users\chait\Downloads\_Jai Shri Ram_320(PagalWorld.com.sb).mp3"
            say("Playing Music")
            os.startfile(musicpath)
            continue
        
        elif query.lower().startswith('launch'):
            app_name = query.lower().split('launch ')[1]
            launch_application(app_name)
            continue

        elif 'the time' in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")
            continue
        
        elif "using AI".lower() in query.lower():
            ai(prompt=query)
            continue
        
        elif "CLOSE".lower() in query.lower():
            say("Goodbye!")
            exit()
        
        elif "reset chat".lower() in query.lower():
            global chatstr
            chatstr = ""
            say("Chat history reset.")
            continue
        
        elif "tell me about".lower() in query.lower():
            chat(query)
            continue

if __name__ == '__main__':
    main()
