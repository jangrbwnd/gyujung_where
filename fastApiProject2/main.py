from fastapi import FastAPI, BackgroundTasks, Response
from fastapi.responses import HTMLResponse, StreamingResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from cv import get_stream_video, inferance, clear_image_folder


app = FastAPI()

IMAGE_FOLDER = './images'

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    clear_image_folder(IMAGE_FOLDER)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def video_streaming():
    return get_stream_video(IMAGE_FOLDER)

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(video_streaming(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/detect", response_class=HTMLResponse)
async def start_video(background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(run_inference)
    return templates.TemplateResponse("index.html", {"request": request})

async def run_inference():
    inference_instance = inferance()
    #result = inference_instance.detector()
    result = inference_instance
    with open('templates/result.txt', 'w') as f:
        f.write(result)


@app.get("/inference_result", response_class=HTMLResponse)
async def get_inference_result():
    with open('templates/result.txt', 'r') as f:
        result = f.read()
        print('결과는:' + result)
    return JSONResponse(content={"result": result})
    #return  result
