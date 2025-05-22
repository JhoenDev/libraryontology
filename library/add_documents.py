from owlready2 import get_ontology
from datetime import date
import csv

# Load the ontology
ontology = get_ontology("data/ontology.owl").load()

# Use existing classes from the ontology
Document = ontology.Document
Article = ontology.Article
Book = ontology.Book
Research = ontology.Research
Math = ontology.Math
Science = ontology.Science
Computer = ontology.Computer
CollegeOfComputerScience = ontology.CollegeOfComputerScience

# Helper to convert string to date
def parse_date(datestr):
    try:
        year, month, day = map(int, datestr.split("-"))
        return date(year, month, day)
    except:
        return None

# Load documents from CSV
with open("data/documents.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Create document with a safe unique name
        doc_name = row['title'].replace(" ", "_").replace(",", "").replace(".", "")
        doc = Document(doc_name)

        doc.hasTitle = [row['title']]
        doc.hasAuthor = [row['author']]
        doc.hasDatePublished = [parse_date(row['datepublish'])]
        doc.hasPublisher = [row['publisher']]
        doc.hasKeywords = [row['keywords']]
        doc.hasAbstract = [row['abstract']]

        # Match type
        if row['type'].lower() == "article":
            doc.hasType = [Article()]
        elif row['type'].lower() == "book":
            doc.hasType = [Book()]
        elif row['type'].lower() == "research":
            doc.hasType = [Research()]

        # Match category
        if row['category'].lower() == "math":
            doc.hasCategory = [Math()]
        elif row['category'].lower() == "science":
            doc.hasCategory = [Science()]
        elif row['category'].lower() == "computer":
            doc.hasCategory = [Computer()]

        # Match college (only one example here, add more if needed)
        if row['college'].lower() == "college of computer science":
            doc.belongsToCollege = [CollegeOfComputerScience()]

# Save updated ontology
ontology.save(file="data/ontology.owl")

print("✅ Documents successfully added from CSV to ontology.")
