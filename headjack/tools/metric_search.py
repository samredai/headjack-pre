"""
Tools to use to query for metrics
"""
import lmql
from headjack.models import Document
from typing import List

async def metric_search(query: str, metric_queries: List[str], dimension_queries: List[str], knowledge: bool = True, nodes: bool = True, top_k: int = 5, metric_threshold: float = 0.0, dimension_threshold: float = 0.0)->List[Document]:
   """
   Fetches information about a metric
   
   First searches for metrics most similar to metric queries
   Then filters dimensions on those columns to the most similar.
   """
   return []
    

@lmql.query
async def query_extract_queries(model_identifier: str, query: str, n_metrics: int = 3, n_dimensions: int = 5):
    examples = """Here are some examples:
    Query: "What is the total number of registered users for the website?"
    Metrics: "total users", "number of users", "registered users"
    
    Query: "What is the total profit by product category for the year 2022?"
    Metrics: "total profit", "profit", "earnings"
    Dimensions: "product category", "category", "year"
    """
    metric_queries = []
    dimension_queries = []
    """
    argmax
       "You are to extract metrics and dimensions, if any, from the query."
       "{examples}"
       "Query: {query}\n"
       "Metrics: "
       for i in range(n_metrics-1):
       "\"[METRIC]\", "
       metric_queries.append(METRIC.strip())
       "\"[METRIC]\"\n"
       metric_queries.append(METRIC.strip())
       "Dimensions: "
       for i in range(n_dimensions-1):
       "\"[DIMENSION]\", "
       metric_queries.append(DIMENSION.strip())
       "\"[DIMENSION]\"\n"
       metric_queries.append(DIMENSION.strip())
    FROM 
       {model_identifier}
    """
    return metric_queries, dimension_queries