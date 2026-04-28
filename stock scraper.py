from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

user = "adeenamer@gmail.com"
pwd = "Adeen@syed.sons@15674"

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)


driver.get('https://app02.splendidaccounts.com')

username = driver.find_element(By.XPATH, "//input[@id='input-username']")
username.send_keys(user)

password = driver.find_element(By.XPATH, "//input[@id='input-password']")
password.send_keys(pwd)

driver.find_element(By.XPATH, "//button[@class = 'status-success appearance-filled full-width size-large shape-rectangle nb-transition']").click()
wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='scrollable']")))

driver.get("https://app02.splendidaccounts.com/#/syed-sons715/1018/reports/inventory-detail")
wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped']")))


driver.find_elements(By.XPATH, "//button[@type = 'submit']")[0].click()


wait = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tr[@class='ng-star-inserted']")))
time.sleep(2)
data = driver.find_elements(By.XPATH, "//tr[@class = 'ng-star-inserted']")


df_list = []
for tr in data:                                                                    #I extract the data from the table
  item_list = []
  all_text = tr.find_elements(By.TAG_NAME, "td")

  if len(all_text) < 7: continue

  if all_text[6].text:
    quant = int(float(all_text[6].text.replace(",", "").split(" ")[0]))
  else: quant = 0

  item_list = [all_text[2].text, all_text[5].text, quant]
  df_list.append(item_list)


all_stock_df = pd.DataFrame(df_list, columns = ["Product", "Branch", "Stock"])

branch_stock_df = all_stock_df.pivot_table(
    index='Product',
    columns='Branch',
    values='Stock',
    fill_value=0
).reset_index()

# branch_stock_df.columns.name = None # Remove the 'Branch' name from columns axis

print(branch_stock_df)

driver.quit()

branch_stock_df.to_excel(r"C:\\Users\\adeen\\Desktop\\All Stock Data.xlsx", index = False)
