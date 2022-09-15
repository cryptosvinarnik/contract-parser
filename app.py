from flask import Flask, request, send_file

from utils.saving import save_contract
from utils.scan_api import EVMScan

app = Flask(__name__, static_folder="contracts")


with open("layouts/index.html") as f:
    html = f.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        api_key = request.form.get("api-key")
        contract = request.form.get("address")
        endpoint = request.form.get("endpoint")

        file = save_contract(EVMScan(api_key, endpoint), contract.lower())

        return send_file(file, as_attachment=True)

    return html

if __name__ == "__main__":
    app.run()
