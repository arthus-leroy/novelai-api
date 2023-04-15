import asyncio
import base64
from pathlib import Path

from boilerplate import API

from novelai_api.ImagePreset import ControlNetModel, ImageModel, ImagePreset


async def main():
    d = Path("results")
    d.mkdir(exist_ok=True)

    async with API() as api_handler:
        api = api_handler.api

        with open(d / "image.png", "rb") as f:
            image = base64.b64encode(f.read()).decode()

        controlnet = ControlNetModel.Form_Lock
        _, mask = await api.low_level.generate_controlnet_mask(controlnet, image)

        preset = ImagePreset()
        preset.controlnet_model = controlnet
        preset.controlnet_condition = base64.b64encode(mask).decode()
        preset.controlnet_strength = 1.5

        # NOTE: for some reasons, the images with controlnet are slightly different
        async for _, img in api.high_level.generate_image("1girl", ImageModel.Anime_Full, preset):
            with open(d / "image_with_controlnet.png", "wb") as f:
                f.write(img)


asyncio.run(main())
