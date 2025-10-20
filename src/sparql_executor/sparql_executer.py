"""
SPARQL Query Executor for ATAI Chatbot
--------------------------------------
Loads the RDF graph from data/atai_dataset/graph.nt
and executes user-entered SPARQL queries.
"""

from rdflib import ConjunctiveGraph

GRAPH_PATH = "data/atai_dataset/graph.nt"

# Load the RDF graph globally once
g = ConjunctiveGraph()
print(f"🔍 Loading RDF graph from {GRAPH_PATH}...")
g.parse(GRAPH_PATH, format="nt")
print(f"✅ RDF graph loaded with {len(g)} triples.")


def query_executor(message: str, room=None):
    """
    Executes a SPARQL query string against the loaded RDF graph.
    Parameters:
        message (str): SPARQL query text
        room: optional chat interface object (with .post_messages)
    Returns:
        reply (str): textual result of the query
    """
    query = (message or "").strip()
    if not query:
        reply = "Empty input."
        if room:
            room.post_messages(reply)
        else:
            print(reply)
        return reply

    try:
        result = g.query(query)
        rows = []
        for r in result:
            values = [str(v) for v in r]
            for i, val in enumerate(values):
                if "wikidata.org/entity/" in val:
                    qid = val.split("/")[-1]
                    values[i] = f"({qid})"
            rows.append(" ".join(values))

        reply = "\n".join(rows) if rows else "No results found."

    except Exception as e:
        reply = f"Error while executing query! Please check SPARQL syntax.\n({e})"

    if room:
        room.post_messages(reply)
    else:
        print("💡 Reply:")
        print(reply)

    return reply
