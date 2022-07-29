from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"

print(style.GREEN)
print(" [+]-{Python}-[+] ")
print(style.RESET)

f = open("message.txt", "r")
message = f.read()
f.close()

print(style.GREEN + '\nThis is your message :-')
print(style.WHITE + message)
print("\n" + style.RESET)
message = quote(message)

numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
	if line.strip() != "":
		numbers.append(line.strip())
f.close()
total_number=len(numbers)
print(style.RED + 'Found ' + str(total_number) + ' numbers in the file.!' + style.RESET)
delay = 30

if (total_number==0):
	print(style.RED+"Programme Terminated..!")
	exit()


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
print('\nSign into WhatsApp Web...')
driver.get('https://web.whatsapp.com')
input(style.RED + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER..." + style.RESET)
for idx, number in enumerate(numbers):
	number = number.strip()
	if number == "":
		continue
	print(style.BLUE + '{}/{} => Sending message to {}.'.format((idx+1), total_number, number) + style.RESET)
	try:
		url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
		sent = False
		for i in range(1):
			if not sent:
				driver.get(url)
				try:
					click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_4sWnG']")))
				except Exception as e:
					print(style.GREEN + f"\nMessage sent to: {number}, retry ({i+1}/1)")
					print("Complete.\n" + style.RESET)
				else:
					click_btn.click()
					sent=True
					print(style.GREEN + 'Message sent to: ' + number + style.RESET)
	except Exception as e:
		print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)
		lines = [str(number)]
		file_create = open("Faild_Numbers.txt","w")
		for line in lines:
			file_create.write(line)
			file_create.write("\n")
		file_create.close()
		printfile = open("Faild_Numbers.txt","r")	
		print("\n"+printfile.read())
driver.close()
