"""
Tools to use to query for metrics
"""
from typing import List

import lmql
from dataclasses import dataclass

from lmql.utils.nputil import topk
from headjack_server.models import Document, Tool, Observation, Utterance

async def metric_search(
    query: str,
    metric_queries: List[str],
    dimension_queries: List[str],
    knowledge: bool = True,
    nodes: bool = True,
    top_k: int = 5,
    metric_threshold: float = 0.0,
    dimension_threshold: float = 0.0,
) -> List[Document]:
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
    metric_queries: List[str] = []
    dimension_queries: List[str] = []
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

@dataclass
class MetricSearchTool(Tool):
    default_description = "Search for metrics and knowledge."
    default_ref_name = "metric_search"
    n_metrics: int = 3
    n_dimensions: int = 5
    knowledge: bool = True
    nodes: bool = True
    top_k: int = 5
    metric_threshold: float = 0.0
    dimension_threshold: float = 0.0
    
    async def __call__(self, utterance: Utterance)->Observation:
        query = utterance.utterance
        metric_queries, dimension_queries = await query_extract_queries(self.model_identifier, query, self.n_metrics, self.n_dimensions)
        results = await metric_search(query, metric_queries, dimension_queries, knowledge = self.knowledge, nodes = self.nodes, top_k = self.top_k, metric_threshold = self.metric_threshold, dimension_threshold = self.dimension_threshold)
        return Observation(utterance=str((metric_queries, dimension_queries)), tool = self, parent= utterance)