import pandas as pd
import os
from src.extract.extractor import Extractor
from src.utils import load_config

class Pipeline:
    def __init__(self):
        self.config = load_config()
        self.extractor = Extractor()
        self.chunk_size = self.config['extraction'].get('chunk_size', 1000)

    def run(self, input_file="data/input.txt"):
        print(f"Starting extraction from {input_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"File {input_file} not found.")
            return

        chunks = self._chunk_text(text)
        print(f"Total chunks: {len(chunks)}")
        
        all_entities = []
        all_relationships = []
        
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            result = self.extractor.extract(chunk)
            
            # Simple list extension
            if result:
                new_entities = result.get('entities', [])
                new_relationships = result.get('relationships', [])
                all_entities.extend(new_entities)
                all_relationships.extend(new_relationships)

        self._save_results(all_entities, all_relationships)
        print("Extraction complete.")

    def _chunk_text(self, text):
        # Very simple chunking by paragraphs/newlines
        # In production, use LangChain text splitters
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""
        
        for p in paragraphs:
            if len(current_chunk) + len(p) < self.chunk_size:
                current_chunk += p + "\n"
            else:
                chunks.append(current_chunk)
                current_chunk = p + "\n"
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def _save_results(self, entities, relationships):
        # Deduplication logic for entities
        unique_entities = {e['id']: e for e in entities if 'id' in e}.values()
        
        df_nodes = pd.DataFrame(list(unique_entities))
        df_rels = pd.DataFrame(relationships)
        
        output_dir = "data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        nodes_path = os.path.join(output_dir, "nodes.csv")
        rels_path = os.path.join(output_dir, "relationships.csv")
        
        df_nodes.to_csv(nodes_path, index=False)
        df_rels.to_csv(rels_path, index=False)
        
        print(f"Saved {len(unique_entities)} nodes to {nodes_path}")
        print(f"Saved {len(relationships)} relationships to {rels_path}")

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
