Test app to show file sharing using Fast API (Python)
Run these commands in order to run the API:

```
pip install -r requirements.txt
python3 create_db.py
python3 main.py
```
After following the above, the server will start at `localhost:8000`. I suggest going to `localhost:8000/docs` check OpenAPI docs which FastAPI automatically provides.

To run tests, follow:

```
cd tests
pytest
```