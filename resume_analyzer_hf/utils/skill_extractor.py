from transformers import pipeline

_ner = pipeline("token-classification",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple")

def extract_skills(text: str):
    ents = _ner(text)
    skills = [e["word"] for e in ents if e["entity_group"] in ["MISC", "ORG", "PER"]]
    return list(set([s.strip().lower() for s in skills if not s.startswith("##") and len(s)>2]))
