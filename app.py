from flask import Flask
import threading
from main import main  # bu sening bot funksiyang

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti ✅"

def run_bot():
    main()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=port)
