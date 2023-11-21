from fastapi import FastAPI, Request, BackgroundTasks, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from retrieve import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class questionObj(BaseModel):
    text: str

@app.post("/inference")
async def inference(question: questionObj):
    try:
        # question = 'what is the significance of german sailors to the hamburger'
        answer = get_answer(question.text)
        return answer

    except Exception as e:
        print(e)
        return {'content':f'Error:{e}','url':'no url'}


if __name__ == '__main__':
    uvicorn.run(app, port=4242, host='0.0.0.0')