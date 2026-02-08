import json
import os
from openai import OpenAI
from src.utils import load_config

class Extractor:
    def __init__(self):
        self.config = load_config()
        self.llm_cfg = self.config['llm']
        
        # Check if API key is set, otherwise potential mock mode or error
        if self.llm_cfg['api_key'] == "YOUR_API_KEY_HERE":
             print("Warning: API Key not configured. Extraction calls will fail or need mocking.")
             
        self.client = OpenAI(
            api_key=self.llm_cfg['api_key'],
            base_url=self.llm_cfg.get('base_url', 'https://api.openai.com/v1')
        )
        self.model = self.llm_cfg['model']
        self.temperature = self.llm_cfg.get('temperature', 0.0)

    def extract(self, text_chunk: str) -> dict:
        """
        Extract entities and relations from a text chunk.
        Returns a dict with 'entities' and 'relationships'.
        """
        system_prompt = self._build_system_prompt()
        user_prompt = f"Text to extract from:\n{text_chunk}"
        
        if self.llm_cfg['api_key'] == "YOUR_API_KEY_HERE":
             print("Warning: API Key not configured. Using Mock Mode.")
             return self._mock_extract(text_chunk)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"} 
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error during extraction: {e}")
            return {"entities": [], "relationships": []}

    def _mock_extract(self, text):
        return {
            "entities": [
                {"id": "高启强", "type": "Person", "description": "京海市卖鱼贩"},
                {"id": "安欣", "type": "Person", "description": "京海市公安局警官"},
                {"id": "旧厂街", "type": "Location", "description": "充满烟火气的老城区"},
                {"id": "京海市", "type": "Location", "description": "故事发生地"}
            ],
            "relationships": [
                {"source": "高启强", "target": "旧厂街", "type": "locatedAt"},
                {"source": "安欣", "target": "高启强", "type": "friendOf", "description": "吃饺子建立的交情"}
            ]
        }

    def _build_system_prompt(self):
        return """
You are an expert Knowledge Graph Extractor.
Your task is to extract structural information from the provided text and output it in JSON format.
The schema is loosely based on cnSchema.

**Entity Types**:
- Person (e.g., 高启强, 安欣)
- Organization (e.g., 建工集团, 公安局)
- Location (e.g., 京海市, 旧厂街)
- Event (e.g., 冲突, 吃饭)

**Relationship Types**:
- worksFor, memberOf, leaderOf
- friendOf, relativeOf, enemyOf, colleagueOf
- locatedAt
- participant
- nextEvent (temporal sequence)

**Output Format**:
{
  "entities": [
    {"id": "Unique Name", "type": "Type", "description": "Short description"}
  ],
  "relationships": [
    {"source": "Source Entity ID", "target": "Target Entity ID", "type": "RELATION_TYPE", "description": "Context"}
  ]
}
Ensure the JSON is valid. If no information is found, return empty lists.
"""

if __name__ == "__main__":
    # Simple test
    extractor = Extractor()
    text = "高启强住在旧厂街，他是高启盛的哥哥。"
    # print(extractor.extract(text)) 
    print("Extractor initialized.")
