import requests
import random
import xlwt
from time import sleep

def check_airdrop(wallet: str, proxies: list = None):
    url = f'https://starkrocket.xyz/api/check_wallet?address={wallet}'

    if proxies:
        proxy = random.choice(proxies)
        _proxies = {
            "http": proxy,
            "https": proxy
        }        
        response = requests.get(url, proxies=_proxies)
    else:
        response = requests.get(url)

    try:
        data = response.json()
        result = data.get("result", {})
        points = result.get("points")
        criteria = result.get("criteria", {})
        eligible = result.get("eligible")
       
        bridge_volume = criteria.get("bridge_volume", [])
        contracts_variety = criteria.get("contracts_variety", [])
        transaction_volume = criteria.get("transaction_volume", [])
        transactions_frequency = criteria.get("transactions_frequency", [])
        transactions_over_time = criteria.get("transactions_over_time", [])
        
        print(f"Wallet: {wallet}, Points: {points}, Eligible: {eligible}")
        print(f"Bridge Volume: {bridge_volume}")
        print(f"Contracts Variety: {contracts_variety}")
        print(f"Transaction Volume: {transaction_volume}")
        print(f"Transactions Frequency: {transactions_frequency}")
        print(f"Transactions Over Time: {transactions_over_time}")
      
        return {"wallet": wallet, "points": points, "eligible": eligible,
                "bridge_volume": bridge_volume, "contracts_variety": contracts_variety,
                "transaction_volume": transaction_volume,
                "transactions_frequency": transactions_frequency,
                "transactions_over_time": transactions_over_time}
    except Exception as e:
        print(f"Failed to parse JSON response for wallet {wallet}, reason: {e}")
        return None

def save_to_excel(results, output_file="results.xls"):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Results")

    headers = ["№", "Wallet", "Points", "Eligible",
               "Bridge Volume", "Contracts Variety",
               "Transaction Volume", "Transactions Frequency",
               "Transactions Over Time"]

    for col, header in enumerate(headers):
        sheet.write(0, col, header)

    for i, result in enumerate(results, start=1):
        sheet.write(i, 0, i)
        sheet.write(i, 1, result["wallet"])
        sheet.write(i, 2, result["points"])
        sheet.write(i, 3, result["eligible"])
        sheet.write(i, 4, str(result["bridge_volume"]))
        sheet.write(i, 5, str(result["contracts_variety"]))
        sheet.write(i, 6, str(result["transaction_volume"]))
        sheet.write(i, 7, str(result["transactions_frequency"]))
        sheet.write(i, 8, str(result["transactions_over_time"]))

    workbook.save(output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    with open("wallets.txt", "r") as file:
        wallets = [w.strip() for w in file]

    with open("proxies.txt", "r") as file:
        proxies = [p.strip() for p in file]

    results = []

    for wallet in wallets:
        try:
            result = check_airdrop(wallet, proxies)
            if result:
                results.append(result)
        except Exception as e:
            print(f'Failed to check wallet {wallet}, reason: {e}')
        finally:
            sleep(1)

    save_to_excel(results)
