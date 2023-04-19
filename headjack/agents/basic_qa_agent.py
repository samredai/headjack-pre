"""
An agent that can answer basic questions

"Are there any metrics about..."
"Are there any metrics pertaining to..."
"Tell me about this metric..."
"Are these metrics compatible"
"Tell me about the dimensions that are available for metric x..."
"""
from typing import List
from headjack.models import Tool, Agent
import lmql

