import pandas as pd
from owlready2 import get_ontology, onto_path

# Set the path to your ontology
onto_path.append("data")
ontology = get_ontology("data/ontology.owl").load()

# Load documents CSV
df = pd.read_csv("data/documents.csv")

# Print sample documents with related ontology entities
for idx, row in df.iterrows():
    print(f"\nTitle: {row['title']}")
    print(f"Author: {row['author']}")
    print(f"Type: {row['type']}")
    print(f"Category: {row['category']}")
    print(f"College: {row['college']}")
    
    # Check if ontology contains the class
    type_cls = getattr(ontology, row['type'], None)
    category_cls = getattr(ontology, row['category'], None)
    college_cls = getattr(ontology, row['college'], None)

    print(f" - Ontology Type Class: {type_cls}")
    print(f" - Ontology Category Class: {category_cls}")
    print(f" - Ontology College Class: {college_cls}")
