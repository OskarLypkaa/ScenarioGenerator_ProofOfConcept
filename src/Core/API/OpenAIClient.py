import base64
from openai import OpenAI
import os
from utilities.logger import log

class OpenAIClient:
    def __init__(self, sApiKey: str, sModel: str = "gpt-4.1-2025-04-14"):
        self.sModel = sModel
        self.client = OpenAI(api_key=sApiKey)
        log.debug(f"OpenAI client initialized with model {sModel}")

    def _imageToBase64(self, sImagePath: str) -> str:
        with open(sImagePath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def sendStepToAI(self, sPrompt: str, lImagePaths: list[str]) -> str:
        lContent = [{"type": "text", "text": sPrompt}]

        for sPath in lImagePaths:
            lContent.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{self._imageToBase64(sPath)}"
                }
            })

        log.info(f"Sending prompt to OpenAI with {len(lImagePaths)} image(s)")
        response = self.client.chat.completions.create(
            model=self.sModel,
            messages=[
                {
                    "role": "user",
                    "content": lContent
                }
            ],
            max_tokens=500
        )
        log.debug("Received response from OpenAI")

        return response.choices[0].message.content
