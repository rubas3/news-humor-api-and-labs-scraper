import requests, re, csv
from bs4 import BeautifulSoup

BASE_URL = "https://www.marham.pk/labs"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# get all lab links (limit to 10)
lab_links = soup.select(".shadow-card .mt-10 a")[:10]

lab_ids = []

for lab in lab_links:
    link = lab.get("href")

    res = requests.get(link)
    soup2 = BeautifulSoup(res.text, "html.parser")

    script = soup2.find("script", string=re.compile("labId"))
    js_text = script.string

    lab = re.search(r"labId\s*=\s*(\d+)", js_text).group(1)
    
    lab_ids.append(lab)
    
    
all_labs_data = []

for i in lab_ids:
    url = f"https://www.marham.pk/api/lab/tests-optimized?lab_id={i}"

    response = requests.get(url=url)

    if response.status_code == 200:
        try:
            data = response.json()
            
            lab_id = data["id"]
            lab_name = data["name"]
        
            lab_tests = data["lab_tests"]

            for test in lab_tests:
                all_labs_data.append({
                    "lab_id": lab_id,
                    "lab_name": lab_name,
                    "test_id": test['id'],
                    "test_name": test['name'],
                    "test_type": test['type'],
                    "fee": test['fee'],
                    "discount": test['discount'],
                    "discountPercentage": test['discountPercentage'],
                    "discountedFee": test['discountedFee']
                })
        except ValueError as e:
            print(f"JSON decoding failed for lab_id {lab}: {e}")   
        
    else:
        print(f"The response code for lab id: {lab} is not 200")
        
        
if all_labs_data:
    with open('labs_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "lab_id", "lab_name", "test_id", "test_name", "test_type","fee", "discount", "discountPercentage", "discountedFee"
        ])
        writer.writeheader()
        writer.writerows(all_labs_data)

    print("Data saved to labs_data.csv")
    
else: 
    print("No data present to save")
    
