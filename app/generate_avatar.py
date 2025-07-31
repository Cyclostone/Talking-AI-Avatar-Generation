from diffusers import StableDiffusionPipeline
import torch
import os

# Create directory for images if it doesn't exist
os.makedirs("app/images", exist_ok=True)

# Check if MPS (Metal Performance Shaders) is available for Mac
if torch.backends.mps.is_available():
    device = "mps"
    print("Using MPS (Metal) acceleration")
else:
    device = "cpu"
    print("Using CPU for inference")

# Load the model with appropriate settings for Mac
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to(device)

prompt = "Professional Indian Man, Front-facing, smiling, clean background, photo-realistic"
print(f"Generating image with prompt: '{prompt}'")
image = pipe(prompt, num_inference_steps=30, height=512, width=512).images[0]

image.save("app/images/avatar.jpg")
print("Avatar image saved to app/images/avatar.jpg")