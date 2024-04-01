# Python Fastapi Pydantic_v2 Mongodb

```bash
# Create a new project using Python 3.12, specifically:
  $ pipenv --python 3.12
  
# Install the requirements:
  $ pipenv install --dev

# Activate virtual environment:
  $ pipenv shell

# Configure the location of your MongoDB database:
export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"

# Start the service:
uvicorn app:app --reload
```
