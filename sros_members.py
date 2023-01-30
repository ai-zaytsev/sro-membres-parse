import requests
import csv

def get_sro_id_list():
    url = "https://api-open-nostroy.anonamis.ru/api/sro/list"
    page = 1
    r = requests.post(url, json={"filters": {"state": "enabled"}, "page": page, "pageCount": "100", "sortBy": {}})
    data_dict = r.json()
    countPages = data_dict['data']['countPages']
    ids = []
    for page in range(1, int(countPages)+1):
        r = requests.post(url, json={"filters": {"state": "enabled"}, "page": page, "pageCount": "100", "sortBy": {}})
        data_dict = r.json()
        data = data_dict['data']['data']
        ids += [item['id'] for item in data]
    return ids

def write_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(data+'\n')

def get_member_list_sro(id_sro):
    url = f"https://api-open-nostroy.anonamis.ru/api/sro/{id_sro}/member/list"
    page = 1
    r = requests.post(url, json={"filters": {"member_status": 1}, "page": page, "pageCount": "100", "sortBy": {}})
    data_dict = r.json()
    countPages = data_dict['data']['countPages']
    members = []

    sro_info_url = f"https://api-open-nostroy.anonamis.ru/api/sro/{id_sro}"
    sro_info_request = requests.post(sro_info_url)
    data_dict_sro = sro_info_request.json()
    data_sro = [data_dict_sro['data']['registration_number'], data_dict_sro['data']['full_description']]

    for page in range(1, int(countPages)+1):
        r = requests.post(url, json={"filters": {"member_status": 1}, "page": page, "pageCount": "100", "sortBy": {}})
        data_dict = r.json()
        data = data_dict['data']['data']

        members += [[str(item['id']), item['full_description'], item['inn']] for item in data]
    
    sro_members = [data_sro+member for member in members]

    return sro_members

for id in get_sro_id_list():
    for _ in get_member_list_sro(id):
        write_to_file("sro_members_data.txt", ';'.join(_))
