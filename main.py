from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'messages': 'Hello World'}

@app.get('/tampilin_angka_dong')
def tampilin_angka_dong():
    a = 50*80/20+2
    return {"hasil": a}