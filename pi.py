import pathlib
import warnings
import speech_recognition as sr
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options  # Import Edge Options
from selenium.webdriver.edge.service import Service  # Import Edge Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # Correct EdgeDriverManager import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global variables
VoiceIsOnOrOff = False

# Disable warnings
warnings.simplefilter('ignore')

# Import the Clap module, make sure it's in the correct path
from Clap import MainClapExe
MainClapExe()

# Speech recognition function
def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language="en")
            print(f"==> Me : {query}")
            return query.lower()
        except Exception as e:
            print(f"Error: {e}")
            return ""


# Selenium setup
ScriptDir = pathlib.Path().absolute()
url = "https://pi.ai/talk"
edge_option = Options()

# Define a user-agent
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
edge_option.add_argument(f"user-agent={user_agent}")
edge_option.add_argument('--profile-directory=Default')
edge_option.add_argument(f'user-data-dir={ScriptDir}\\edgedata')

# Automatically install the compatible version of EdgeDriver
driver_path = EdgeChromiumDriverManager().install()

# Debugging: Print the EdgeDriver path
print(f"Using EdgeDriver: {driver_path}")

service = Service(driver_path)

# Initialize the driver with the correct options
driver = webdriver.Edge(service=service, options=edge_option)

# Maximize window for visibility
driver.maximize_window()
driver.get(url=url)
sleep(5)

# Functions to interact with the web page
def VoiceOnButton():
    global VoiceIsOnOrOff
    try:
        Xpath = '/html/body/div/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button/div/svg[1]'
        driver.find_element(by=By.XPATH, value=Xpath).click()
        VoiceIsOnOrOff = True
    except Exception as e:
        print(f"Error clicking voice button: {e}")

def QuerySender(Query):
    try:
        XpathInput = '/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/div/textarea'
        XpathSenderButton = '/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/button'
        driver.find_element(by=By.XPATH, value=XpathInput).send_keys(Query)
        sleep(1)
        driver.find_element(by=By.XPATH, value=XpathSenderButton).click()
        sleep(1)
    except Exception as e:
        print(f"Error sending query: {e}")

def Wait_for_result():
    try:
        XpathInput = '/html/body/div/main/div/div/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div'
        driver.find_element(by=By.XPATH, value=XpathInput).send_keys("Testing...")
        sleep(1)

        # Wait for the send button to become enabled
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/button/svg/path"))
        )
    except Exception as e:
        print(f"Error waiting for result: {e}")

def Result():
    try:
        Text = driver.find_element(by=By.XPATH, value="/html/body/div/main/div/div/div[3]/div[1]/div[2]/div/div/div/div[3]").text
        return Text
    except Exception as e:
        print(f"Error getting result: {e}")
        return "Error getting result"

# Main execution function
def MainExecution():
    global VoiceIsOnOrOff
    Query = speechrecognition()

    if Query:
        QuerySender(Query=Query)

        if VoiceIsOnOrOff == False:
            VoiceOnButton()
        Wait_for_result()
        print(f"==> Zara AI: {Result()}")

# Infinite loop to keep running
while True:
    MainExecution()
