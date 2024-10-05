import time as tm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import os


# Information collection function
def collect_product_info(driver, url=''):
	# Opening a new window
	driver.switch_to.new_window('tab')
	tm.sleep(2)

	# Following the link
	driver.get(url=url)
	tm.sleep(3)

	# Copy page to file
	product_id = driver.find_element(By.XPATH, '//div[contains(text(), "Артикул: ")]').text.split('Артикул: ')[1]

	page_source = str(driver.page_source)
	soup = BeautifulSoup(page_source, 'lxml')

	with open(f'product_{product_id}.html', 'w', encoding="utf-8") as file:
		file.write(page_source)

	product_name = soup.find('div', attrs={"data-widget": 'webProductHeading'}).find('h1').text.strip().replace('\t', '').replace('\n', ' ')

	# Collect feedback
	try:
		product_statistic = soup.find('div', attrs={"data-widget": 'webSingleProductScore'}).text.strip()

		if " • " in product_statistic:
			product_stars = product_statistic.split(' • ')[0].strip()
			product_reviews = product_statistic.split(' • ')[1].strip()
		else:
			product_statistic = product_statistic
			product_statistic = None
			product_stars = None
			product_reviews = None
	except:
		product_statistic = None
		product_stars = None
		product_reviews = None

	
	# Collect price
	try:
		ozon_card_price_element = soup.find('span', string="c Ozon Картой").parent.find('div').find('span')
		product_ozon_card_price = ozon_card_price_element.text.strip() if ozon_card_price_element else ''

		price_element = soup.find('span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

		product_discount_price = price_element[0].text.strip() if price_element[0] else ''
		product_base_price = price_element[1].text.strip() if price_element[1] is not None else ''
	except AttributeError:
		card_price_div = soup.find('div', attrs={"data-widget": "webPrice"}).find('span')

		product_base_price = card_price_div.text.strip()
		product_discount_price = None
		product_ozon_card_price = None
	except IndexError:
		ozon_card_price_element = soup.find('span', string="c Ozon Картой").parent.find('div').find('span')
		product_ozon_card_price = ozon_card_price_element.text.strip() if ozon_card_price_element else ''

		price_element = soup.find('span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

		product_discount_price = None
		product_base_price = price_element[0].text.strip() if price_element[0] is not None else ''

	
	# Recording of data obtained
	product_data = (
		{
		'ID': product_id,
		'Name': product_name,
		'Price (ozon card)': product_ozon_card_price,
		'Price (discount)': product_discount_price,
		'Price (base)': product_base_price,
		'Statistic': product_statistic,
		'Stars': product_stars,
		'Reviews': product_reviews,
		}
	)

	# Finalization
	driver.close()
	driver.switch_to.window(driver.window_handles[0])

	# Deletion of created file
	os.remove(f"./product_{product_id}.html")

	return product_data