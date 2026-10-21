"""
BriefForge Image Extractor
Visual packaging image analysis using Gemini 2.5 Pro Vision and Pillow.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from PIL import Image
import google.generativeai as genai
from core.fusion.fact_store import ExtractedFact

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extracts logos, pack photography details, visual assets, and barcode info from images."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def extract(self, file_path: str) -> List[ExtractedFact]:
        facts: List[ExtractedFact] = []
        path = Path(file_path)
        img = Image.open(file_path)
        
        # Analyze with Gemini Vision if available
        if self.api_key:
            try:
                model = genai.GenerativeModel(self.model_name)
                prompt = (
                    "Analyze this packaging image. Identify the brand, product title, "
                    "certifications/logos visible, imagery type (e.g., cereal bowl with fresh fruit), "
                    "and any printed copy. Return a brief summary."
                )
                response = model.generate_content([prompt, img])
                desc = response.text.strip()
                
                facts.append(ExtractedFact(
                    field="visual_pack_imagery",
                    value=desc,
                    source_file=path.name,
                    source_type="image",
                    source_location="Visual Artwork Image",
                    confidence=0.92,
                    category="creative"
                ))
            except Exception as e:
                logger.warning(f"Image analysis error: {e}")
                
        return facts
