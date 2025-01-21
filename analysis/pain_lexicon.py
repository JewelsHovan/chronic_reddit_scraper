from typing import Dict, List
import json

class PainLexicon:
    def __init__(self):
        self.terms: Dict[str, Dict] = {}
        self.categories: Dict[str, List[str]] = {
            "physical": [],
            "intensity": [],
            "location": [],
            "temporal": [],
            "impact": []
        }
        
    def add_term(self, term: str, entry: Dict):
        """Add a new term to the lexicon"""
        if term not in self.terms:
            self.terms[term] = entry
            # Add to relevant categories
            for category in entry["categories"]:
                self.categories[category].append(term)
                
    def get_related_terms(self, term: str) -> List[str]:
        """Get terms similar to the input term"""
        if term in self.terms:
            return self.terms[term]["metadata"]["synonyms"]
        return []
    
    def export_lexicon(self, filepath: str):
        """Export the lexicon to JSON"""
        with open(filepath, 'w') as f:
            json.dump({
                "terms": self.terms,
                "categories": self.categories
            }, f, indent=2)