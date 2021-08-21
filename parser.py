from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import traceback

# В переменную URL Вписать ссылку в кавычках
#URL = "https://www.ozon.ru/category/apparatnaya-kosmetologiya-6325/?text=мезороллер"
URL = "https://www.wildberries.ru/catalog/0/search.aspx?xfilters=xsubject%3Bdlvr%3Bbrand%3Bprice%3Bkind%3Bcolor%3Bwbsize%3Bseason%3Bconsists&xparams=subject%3D1560&xshard=beauty&sort=popular&search=мезороллер"

# в переменную SELLER вписать название продавца в кавычках, если нужно другое!
# Если я правильно понял, то для WB нужно писать "ИП Майорова Алина Андреевна"
SELLER = "ИНТЕРНЕТ РЕВОЛЮЦИЯ ООО"

# Время загрузки страницы. Можно увеличить, если будут ошибки, уменьшать НЕ РЕКОМЕНДУЕТСЯ!
SLEEP_TIME = 5

# Страница, с которой начинать поиск
START_PAGE = 1

class Parse:

	def __init__(self, URL, SELLER, SLEEP_TIME, START_PAGE):
		
		path_dir = os.path.dirname(os.path.abspath(__file__))

		if 'ozon.ru' in URL or 'wildberries.ru' in URL:
			self.URL = URL
			if SELLER:
				self.SELLER = SELLER.lower()
				self.SLEEP_TIME = SLEEP_TIME
				self.START_PAGE = START_PAGE
				if not type(SLEEP_TIME) == int:
					raise "В переменную SLEEP_TIME Нужно вставить целое число без кавычек!"

				if 'wildberries.ru' in URL:
					self.platform = 'wb'
				elif 'ozon.ru' in URL:
					self.platform = 'ozon'

				driver_url = path_dir + "/chromedriver.exe"
				self.driver = webdriver.Chrome(executable_path=driver_url)
			else:
				raise "Впишите название продавца в переменную SELLER"
		else:
			raise "Парсер предназначен только для ozon.ru и wildberries.ru"
		self.result = []
		

	#def open_url(self, page = 1):
	#	pass

	def open_page(self, page=1):
		if not 'page' in self.URL:
			if self.platform == 'ozon':
				URL = self.URL.replace("?", f"?page={page}&")
			else:
				URL = self.URL.replace("&search", f"&page={page}&search")
			self.driver.get(URL)
			for i in range(self.SLEEP_TIME):
				os.system('cls')
				if self.result:
					for j in self.result:
						print(f"Обнаружено совпадение. Страница: {j['page']}")
				print(f"Open Page {page}", '.' * i)
				sleep(1)
			return {"source": self.driver.page_source, 'url': URL, 'page': page}
		else:
			raise "Вставьте ссылку с первой страницы"

	def open_tab(self, tab, page):
		self.driver.execute_script(f"window.open('https://www.wildberries.ru{tab}','_blank');")
		main_tab = self.driver.window_handles[0]
		new_tab = self.driver.window_handles[1]
		self.driver.switch_to.window(new_tab)
		class_ = "seller__content"
		page_soup = BeautifulSoup(self.driver.page_source)
		block = page_soup.find('p', class_=class_)
		if block is not None:
			text = block.get_text(strip=True)
			if self.SELLER in text.lower():
				self.result.append(
					{'url': f'https://www.wildberries.ru{tab}', 'page': page}
					)
				print(f"Найдено совпадение на странице {page}\nСсылка: https://www.wildberries.ru{tab}")
			status = True
		else:
			status = False
			print("BLOCK NONE")
		self.driver.close()
		self.driver.switch_to.window(main_tab)
		sleep(self.SLEEP_TIME-SLEEP_TIME/2)
		return status
		

	def parse(self,):
		page = START_PAGE - 1
		need_find = True
		have_error = False
		while need_find:
			page += 1
			html = self.open_page(page)
			soup = BeautifulSoup(html['source'])
			if self.platform == 'ozon':
				
				items = soup.findAll('div', class_='a0c6')
				
				if items != []:
					for item in items:
						try:
							class_ = "j4 as3 ay9 a0f6 f-tsBodyM d8e5"
							block = item.find('span', class_=class_)
							if block is not None:
								text = block.get_text(strip=True)
								if self.SELLER in text.lower():
									self.result.append(
										{'url': html['url'], 'page': html['page']}
										)
									print(self.result)
							else:
								print("block NONE:", block)
						except:
							os.system('cls')
							need_find = False
							have_error = True
							print(traceback.format_exc())
				else:
					need_find = False

			elif self.platform == 'wb':
				items = soup.findAll('div', class_='product-card j-card-item')
				if items != []:
					tabs = []
					for item in items:
						try:
							tab = item.find('a').get('href')
							tabs.append(tab)
						except:
							os.system('cls')
							need_find = False
							have_error = True
							print(traceback.format_exc())
					for tab in tabs:
						while not self.open_tab(tab, page):
							pass
				else:
					need_find = False
		if self.result:
			for i in self.result:
				print(f"Страница: {i['page']} | URL: {i['url']}")
		else:
			print("*" * 50)
			print("Совпадений не найдено. Попробуйте увеличить значение SLEEP_TIME через несколько минут.")
			print("!" * 50)
			print(traceback.format_exc())
		if have_error:
			print("*" * 50)
			print(f"Возникла ошибка. Обработано {page - 1} Страниц\n\nЗапустите скрипт с этой страницы через несколько минут")
			print("!" * 50)
		else:
			print("Ошибок не возникло, пройдены все страницы :)")
		self.driver.close()

if __name__ == '__main__':
	parser = Parse(URL, SELLER, SLEEP_TIME, START_PAGE)
	parser.parse()