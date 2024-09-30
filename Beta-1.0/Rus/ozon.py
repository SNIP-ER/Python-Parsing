from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from function import collect_product_info, page_down
import pandas as pd


# Loading data from text file
file = open("setin.txt", "r")
content = file.read()
lines = content.split("\n")

variables = {}

for line in lines:
    key, value = line.split("=")
    key = key.strip().replace('"', '')
    value = value.strip().replace('"', '')
    variables[key] = value

file.close()
globals().update(variables)

links = links
request = request
sort = sort
indexis = indexis
brouther = brouther
itog = int(kolichestvo)


# Parsing
def get_product_links(item_name=request):
	# Automatic software for sensor operation
	if brouther == 'chrome_old':
		# < 79.0.3945.16
		options = webdriver.ChromeOptions()
		options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option("useAutomationExtension", False)

		driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) 
	elif brouther == 'chrome':
		# New chrome (79.0.3945.16 <=)
		options = webdriver.ChromeOptions()
		options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

		options.add_argument("--disable-blink-features=AutomationControlled")

		driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) 
	elif brouther == 'fire_fox':
		options = webdriver.FirefoxOptions()
		options.set_preference("general.useragent.override", "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

		options.set_preference("dom.webdriver.enabled", False)

		driver = webdriver.Firefox(options=options)

	
	driver.implicitly_wait(5)

	# Getting a link to the site
	driver.get(url=links)
	time.sleep(3)

	# Request introduction
	find_input = driver.find_element(By.NAME, 'text')
	find_input.clear()
	find_input.send_keys(item_name)
	time.sleep(2)

	find_input.send_keys(Keys.ENTER)
	time.sleep(2)

	# Sorting
	current_url = f'{driver.current_url}&sorting={sort}'
	driver.get(url=current_url)
	time.sleep(2)

	# Scrolling
	if itog > 11:
		page_down(driver=driver)
		time.sleep(2)

	# Getting links
	try:
		find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
		products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))

		print('[*] Ссылки получены!')
	except:
		print('[*] Что-то не так!')

	# Write links to file
	products_urls_dict = {}

	for k, v in enumerate(products_urls):
		products_urls_dict.update({k: v})

	with open('products_urls_dict.json', 'w', encoding='utf-8') as file:
		json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)
	
	time.sleep(2)

	products_data = []

	# Recording results in a file
	suma = 0

	for url in products_urls:
		if suma < itog:
			data = collect_product_info(driver=driver, url=url)
			print('[+] Данные со страницы собраны')
			time.sleep(2)
			products_data.append(data)
			suma += 1
		elif itog == -1:
			data = collect_product_info(driver=driver, url=url)
			print('[+] Данные со страницы собраны')
			time.sleep(2)
			products_data.append(data)

	pdi = pd.DataFrame(products_data)
	pdi.to_excel('./products_data.xlsx', index=indexis)

	# Finalization
	driver.close()
	driver.quit()


# Main function
def main():
	print("[INFO] Сбор начался!")
	get_product_links()
	print("[INFO] Сбор закончен!")


if __name__ == '__main__':
	main()
