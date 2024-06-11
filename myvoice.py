from time import sleep
import webbrowser
import cv2
import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import subprocess

# Specify the path to your ChromeDriver executable
chrome_driver_path = r"ja"  # Replace with the actual path

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Adjust the speaking rate (you can experiment with different values)
engine.setProperty('rate', 150)  # Adjust the rate as needed

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to pause listening
def pause_listening():
    global listening
    listening = False


# Function to recognize voice command
def listen_for_command(recognizer):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except sr.UnknownValueError:
        return ""

# Function to open applications
def open_application(application_name):
    try:
        if "chrome" in application_name:
            webbrowser.open("https://www.google.com")
        elif "notepad" in application_name:
            subprocess.Popen("notepad.exe")
        elif "calculator" in application_name:
            subprocess.Popen("calc.exe")
        elif "camera" in application_name:
            # Open the camera using opencv-python
            camera = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this if needed)

            # Check if the camera opened successfully
            if camera.isOpened():
                speak("Camera is now open. You can view the camera feed.")
                
                # Continuously capture frames from the camera (you can add more camera-related functionality)
                while True:
                    ret, frame = camera.read()
                    if not ret:
                        break
                    cv2.imshow("Camera Feed", frame)

                    # Press the 'q' key to exit the camera feed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # Release the camera and destroy the OpenCV windows when done
                camera.release()
                cv2.destroyAllWindows()
            else:
                speak("Unable to open the camera.")
        # Add more application-specific commands and actions here
        else:
            speak("Sorry, I don't know how to open that application.")
    except Exception as e:
        print(f"Error: {e}")

# Function to perform a Google search
def perform_google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Searching for {query} on Google.")

# Function to play a YouTube video based on a query
def play_youtube_video(query):
    # Create ChromeOptions and specify the executable path
    chrome_options = Options()
    chrome_options.binary_location = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"  # Replace with the actual path

    # Initialize the Chrome WebDriver with ChromeOptions
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

    try:
        # Construct the YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query}"

        # Open the YouTube search results page in Chrome
        driver.get(search_url)

        # Locate and click on the first video link (adjust the XPath as needed)
        video_link = driver.find_element_by_xpath('//*[@id="video-title"]')
        video_link.click()

        speak(f"Searching and playing '{query}' on YouTube.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the WebDriver when done
        driver.quit()

# Welcome message
speak("Welcome")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Main loop
while True:
    command = listen_for_command(recognizer)

    if "search" in command:
        # Extract the search query and perform the Google search
        query = command.split("search", 1)[1].strip()
        perform_google_search(query)
    elif "open" in command:
        app_name = command.split("open")[1].strip()
        open_application(app_name)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_date = datetime.date.today().strftime("%A, %B %d, %Y")
        speak(f"The current time is {current_time}. Today is {current_date}.")
    elif "stop" in command:
        speak("Goodbye!")
        break
    elif "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "break" in command:
        speak("Listening stopped.")
        # Pause listening
        pause_listening()
    elif "play" in command:
        # Extract the query to play from the command
        query = command.split("play", 1)[1].strip()
        play_youtube_video(query)
    else:
        speak("I could not understand your command")
