from base64 import b64decode
import os
import binascii

response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

response_data = json.loads(response.text)
access_token = response_data['access_token']


response_pdf = requests.get(
    'http://23.88.98.237:8069/api/report/get_pdf',
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Token': access_token
    },
    data = json.dumps({
        "report_name":  "fleet_rent.key_return_report_pdf",
        "ids": [contract_id],
    }),
)

pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])



stripped = pdf_file.replace('\\n', '')
bytes = b64decode(stripped, validate=True)

f = open("temp.pdf", "wb")
f.write(bytes)
f.close()
os.system("lp temp.pdf")