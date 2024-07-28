from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Specify the URL
url = "https://www.compositesworld.com/news/azl-collaborative-project-to-redefine-hydrogen-tank-development"

# Set up the Chrome webdriver with Selenium
chrome_driver_path = "/path/to/chromedriver"  # Replace with the path to your chromedriver executable
chrome_service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service)

# Navigate to the URL
driver.get(url)

# Wait for the page to load (you may need to adjust the waiting time)
driver.implicitly_wait(10)

# Find the main content element by inspecting the HTML structure of the page
main_content = driver.find_element(By.CLASS_NAME, "article-content")

if main_content:
    # Extract and print the text
    article_text = main_content.text
    print(article_text)
else:
    print("Main content not found on the page.")

# Close the browser window
driver.quit()
