from dotenv import load_dotenv
load_dotenv()
import os
from App import app

if __name__ == "__main__":
    app.run(debug=os.environ['DEBUG'], port=os.environ['PORT'])