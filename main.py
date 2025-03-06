import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # print(
    #     """
    #     Choose a workflow:
    #     ___________________
    #     1) Chat Bot
    #     2) Website Content builder
    #     3) Resume Builder
    # """
    # )
    # try:
    #     user_input = int(input("You : "))
    # except Exception:
    #     user_input = 0

    # if user_input == 1:
    #     ChatBotBuilder().invoke()
    # elif user_input == 2:
    #     WebsiteContentBuilder().invoke()
    # elif user_input == 3:
    #     ResumeBuilder().invoke()
    # else:
    #     print("Invalid Input")
