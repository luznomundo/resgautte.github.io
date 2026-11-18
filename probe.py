import urllib.request
import urllib.error
import json
import base64

URL = "https://api.misticpay.com/api/transactions/create"
pk = "pk_fd2d53baae9d0ac0b6600a0b4271b14b"
sk = "sk_7ac314f61204cebbe642f9c8f2025777e897611cf2f2367b2130ed799f7d6fb8"
auth_full = "Basic " + base64.b64encode(f"{pk}:{sk}".encode()).decode()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": auth_full
}

# In check_account, Victor's document is "53117377867".
# What if the merchant document cannot be the payer? We tested other CPFs and got 422.
# What if MisticPay has different transaction types?
# Let's test with different parameters in payload:
variations = [
    {"amount": 5.0, "payerName": "Lucas Silva", "payerDocument": "11144477735", "description": "Doacao"},
    {"amount": 10.0, "payerName": "Lucas Silva", "payerDocument": "11144477735", "description": "Doacao"},
    {"amount": 5, "payerName": "Lucas Silva", "payerDocument": "11144477735", "description": "Doacao"},
]

for p in variations:
    try:
        req = urllib.request.Request(URL, data=json.dumps(p).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            print("RESPOSTA 200:", resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}:", e.read().decode())
