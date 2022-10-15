import os
import time
import uuid

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from pydantic import BaseModel, Field
from stable_diffusion_tf.stable_diffusion import StableDiffusion
from tensorflow import keras

height = int(os.environ.get("WIDTH", 512))
width = int(os.environ.get("WIDTH", 512))
mixed_precision = os.environ.get("MIXED_PRECISION", "no") == "yes"

if mixed_precision:
    keras.mixed_precision.set_global_policy("mixed_float16")

generator = StableDiffusion(img_height=height, img_width=width, jit_compile=False)

app = FastAPI(title="Stable Diffusion API")


class GenerationRequest(BaseModel):
    prompt: str = Field(..., title="Input prompt", description="Input prompt to be rendered")
    scale: float = Field(default=7.5, title="Scale", description="Unconditional guidance scale: eps = eps(x, empty) + scale * (eps(x, cond) - eps(x, empty))")
    steps: int = Field(default=50, title="Steps", description="Number of dim sampling steps")
    seed: int = Field(default=None, title="Seed", description="Optionally specify a seed for reproduceable results")


class GenerationResult(BaseModel):
    download_id: str = Field(..., title="Download ID", description="Identifier to download the generated image")
    time: float = Field(..., title="Time", description="Total duration of generating this image")


@app.get("/")
def home():
    return {"message": "See /docs for documentation"}

@app.post("/generate", response_model=GenerationResult)
def generate(req: GenerationRequest):
    start = time.time()
    id = str(uuid.uuid4())
    img = generator.generate(req.prompt, num_steps=req.steps, unconditional_guidance_scale=req.scale, temperature=1, batch_size=1, seed=req.seed)
    path = os.path.join("/app/data", f"{id}.png")
    Image.fromarray(img[0]).save(path)
    alapsed = time.time() - start
    
    return GenerationResult(download_id=id, time=alapsed)

@app.get("/download/{id}", responses={200: {"description": "Image with provided ID", "content": {"image/png" : {"example": "No example available."}}}, 404: {"description": "Image not found"}})
async def download(id: str):
    path = os.path.join("/app/data", f"{id}.png")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png", filename=path.split(os.path.sep)[-1])
    else:
        raise HTTPException(404, detail="No such file")
