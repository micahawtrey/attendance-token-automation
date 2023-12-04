from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

# Start a Firefox window in the Headless mode.
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
# Access the Galvanize single-sign-on page.
driver.get("https://auth.galvanize.com/sign_in")

# Wait until the elements to input user email and password are located,
# create variable that contains the path to those two elements,
# then input user email and password and press enter.
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "user[email]"))
)
email = driver.find_element(By.NAME, "user[email]")
email.send_keys("micah.a.awtrey@gmail.com")

password = driver.find_element(By.NAME, "user[password]")
password.send_keys("@DcIf4103842644@")
password.send_keys(Keys.RETURN)

# Makes the code wait one second to allow the login information to load.
time.sleep(1)

# Access the SIS
driver.get("https://sis.galvanize.com/cohorts/105/attendance/mine/")

# Clicks on the single-sign-on button, utilizing the login information
# that the session is using.
driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[3]/form/div/div/button").click()

# Clicks on the button leading to the attendance token page.
driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/ul[1]/li[1]/a").click()

# Creates a variable to allow a while loop.
x = 0

while x != 1:
    try:
        # Looks for the token element for 1 second. If it is not found,
        # a TimeoutException error is thrown, sending it to the except.
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/form/div/div/div[1]/p[2]/span"))
        )
        # Creates a variable that holds the token location from the HTML.
        token_location = driver.find_element(By.XPATH, "/html/body/main/div/div/form/div/div/div[1]/p[2]/span")
        # Gets the innerHTML attribute that holds the token.
        token = token_location.get_attribute('innerHTML')
        # Creates a variable that holds the code input.
        token_input = driver.find_element(By.XPATH, "/html/body/main/div/div/form/div/div/div[2]/div[2]/input")
        # Sends the token to the code input then presses enter.
        token_input.send_keys(token)
        token_input.send_keys(Keys.RETURN)
    except:
        # Indicates that the token is not present yet, then refreshes the page.
        print("It's not here yet!")
        driver.refresh()
    else:
        # Runs if the TimeoutException is not thrown after the try.
        # Declares me the winner and changes x to 1, exiting the while loop.
        print("I win!")
        x = 1

# Waits 2 seconds to ensure that everything has time to work.
time.sleep(2)
# Closes the window.
driver.quit
