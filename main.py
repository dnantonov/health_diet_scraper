import json
import csv
import random
import requests
from time import sleep
from bs4 import BeautifulSoup

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=talbe_calorie"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w") as file:
#     file.write(src)

# with open("index.html") as file:
#     src = file.read()
    
# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     all_categories_dict[item_text] = item_href
    
# with open('all_categories_dict.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)
    
iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text
    
    with open(f"data/{count}_{category_name}.html", "w") as file:
        file.write(src)
        
    with open(f"data/{count}_{category_name}.html") as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    
    # проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue
    
    # собираем заголовки таблицы
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    
    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )
        
        # собираем данные продуктов
        products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
        
        product_info = []
        for item in products_data:
            product_tds = item.find_all("td")
            
            title = product_tds[0].find("a").text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text
            
            product_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates
                }
            )
            
            with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    
    
    count += 1
    print(f"# Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1
    print(f"Осталось итераций: {iteration_count}")
    
    if iteration_count == 0:
        print("Работа завершена")
        break
    
    sleep(random.randrange(2, 4))
