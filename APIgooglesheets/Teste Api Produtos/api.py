import requests
from openpyxl import Workbook

def fetch_and_insert_data():
    base_url = "https://lojalivreeleve.vtexcommercestable.com.br/api/catalog_system/pvt/products/GetProductAndSkuIds"
    increment = 20
    start = 1
    skus = []

    while True:
        url = f"{base_url}?_from={start}&_to={start + increment - 1}"
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "X-VTEX-API-AppKey": "vtexappkey-lojalivreeleve-VNEHUA",
            "X-VTEX-API-AppToken": "LTPWSHLJWLMTZMDBNIMBYXJQOJTCGMWNGGQUNSJYFDEKGUVYLZHKOZJCXCBLIBGUZHNQZOSFLMRQYSMOIPSQXQSPZQXVDISFLRHOVAXXNJFTNSWSBYQPEWOAWQNPYABV"
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        for value in data["data"].values():
            skus.extend(value)

        start += increment
        if start > data["range"]["total"]:
            break

    # Agora você pode inserir os dados em um arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.append(["IDSKU"])

    for sku in skus:
        ws.append([sku])

    wb.save("dados.xlsx")

if __name__ == "__main__":
    fetch_and_insert_data()
