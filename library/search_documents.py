from owlready2 import get_ontology
from datetime import datetime

# Load ontology
ontology = get_ontology("data/ontology.owl").load()
Document = ontology.Document

def get_all_text_fields(individual):
    """Extracts all string-based literal values from an individual's data properties."""
    text_fields = []
    for prop in individual.get_properties():
        if prop.python_name.startswith("has"):
            values = list(prop[individual])
            for val in values:
                if isinstance(val, str):
                    text_fields.append(val)
    return text_fields

def search_documents(keyword, doc_type=None, category=None, college=None, date_filter=None):
    results = []

    keyword_tokens = keyword.lower().split()

    for doc in Document.instances():
        # Collect text fields
        all_text_fields = get_all_text_fields(doc)
        combined_text = " ".join(all_text_fields).lower()

        # Collect metadata
        types = [t.name.lower() for t in getattr(doc, "hasType", [])]
        categories = [c.name.lower() for c in getattr(doc, "hasCategory", [])]
        colleges = [col.name.lower() for col in getattr(doc, "belongsToCollege", [])]

        combined_meta = " ".join(types + categories + colleges)
        search_space = combined_text + " " + combined_meta

        # Match keywords
        if not all(token in search_space for token in keyword_tokens):
            continue

        # Apply optional filters
        if doc_type and doc_type.lower() not in types:
            continue
        if category and category.lower() not in categories:
            continue
        if college and college.lower() not in colleges:
            continue

        # 📅 Filter by date
        if date_filter:
            try:
                doc_dates = getattr(doc, "hasDatePublished", [])
                if len(date_filter) == 4:  # Year only
                    filter_year = int(date_filter)
                    if not any(d.year == filter_year for d in doc_dates):
                        continue
                elif len(date_filter) == 7:  # Year + Month
                    filter_date = datetime.strptime(date_filter, "%Y-%m")
                    if not any(d.year == filter_date.year and d.month == filter_date.month for d in doc_dates):
                        continue
                else:
                    print(f"⚠️ Invalid date format: {date_filter}. Use YYYY or YYYY-MM.")
                    continue
            except ValueError:
                print(f"⚠️ Error parsing date filter: {date_filter}")
                continue

        # Store matching document
        results.append({
            "title": doc.hasTitle[0] if hasattr(doc, "hasTitle") and doc.hasTitle else "No Title",
            "author": doc.hasAuthor[0] if hasattr(doc, "hasAuthor") and doc.hasAuthor else "Unknown",
            "keywords": doc.hasKeywords if hasattr(doc, "hasKeywords") else [],
            "abstract": doc.hasAbstract[0] if hasattr(doc, "hasAbstract") and doc.hasAbstract else "",
            "type": types[0] if types else "Unknown",
            "category": categories[0] if categories else "Unknown",
            "college": colleges[0] if colleges else "Unknown",
            "date": doc.hasDatePublished[0] if hasattr(doc, "hasDatePublished") and doc.hasDatePublished else None
        })

    return results

if __name__ == "__main__":
    print("🔍 Document Search Engine")
    query = input("Enter keyword to search documents: ").strip()
    type_filter = input("Filter by Type (optional): ").strip() or None
    category_filter = input("Filter by Category (optional): ").strip() or None
    college_filter = input("Filter by College (optional): ").strip() or None
    date_filter = input("Filter by Date (YYYY or YYYY-MM, optional): ").strip() or None

    matches = search_documents(query, type_filter, category_filter, college_filter, date_filter)

    if matches:
        print(f"\n✅ Found {len(matches)} documents matching '{query}':\n")
        for i, doc in enumerate(matches, 1):
            print(f"{i}. Title: {doc['title']}")
            print(f"   Author: {doc['author']}")
            print(f"   Date Published: {doc['date']}")
            print(f"   Keywords: {', '.join(doc['keywords'])}")
            print(f"   Abstract: {doc['abstract']}")
            print(f"   Type: {doc['type']}, Category: {doc['category']}, College: {doc['college']}\n")
    else:
        print(f"❌ No documents found matching '{query}'.")
