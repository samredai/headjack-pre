"""
An agent that can answer basic questions

"Are there any metrics about..."
"Are there any metrics pertaining to..."
"Tell me about this metric..."
"Are these metrics compatible"
"Tell me about the dimensions that are available for metric x..."
"""
import asyncio
from typing import List, AsyncGenerator, Optional
from headjack_server.models import Tool, Agent, Utterance, Thought, Answer
from headjack_server.tools.metric_search import MetricSearchTool
import lmql


class BasicQAAgent(Agent):
    description = "An agent that answers basic questions about metrics."
    ref_name = "basic_qa"
    
    @lmql.query
    async def __call__(self, input: AsyncGenerator[Utterance, None]) -> Optional[Utterance]:
        tool_prompt = "Here are the tools you choose from:"+"\n".join(f"{tool.ref_name}: {tool.description}" for tool in self.tools)
        tool_refs = {tool.ref_name: tool for tool in tools}
        parent_utterance = None
        """
        argmax
            "As a helpful agent, you must find an answer for the user.\n"
            "To do so, you can leverage tools until you have a final answer or no answer.\n"
            "You will respond in one of the following forms of\n"
            "Thought: use tool\n"
            "Thought: final answer\n"
            "Thought: no answer\n"
            "{tool_prompt}"
            async for utterance in input():
                utterance.parent = parent_utterance
                parent_utterance = utterance
                "{str(utterance)}\n"
                "Thought: [THOUGHT]"
                thought = Thought(utterance = THOUGHT, agent = self, parent = parent_utterance)
                parent_utterance = thought
                if THOUGHT == 'use tool':
                    "Tool: [TOOL]\n"
                    observation = await tool_refs[TOOL](utterance)
                    observation.parent = parent_utterance
                    parent_utterance = observation
                elif THOUGHT == 'final answer':
                    "Answer: [ANSWER]"
                    answer = Answer(utterance = ANSWER, agent = self)
                else:
                    "I cannot respond."
                    
            
        from
            {model_identifier}
        where
            THOUGHT in {"use tool", "final answer", "no answer"} and
            STOPS_AT(THOUGHT, \n)
        distribution 
            TOOL in set(tool_refs.keys())
        """
        return parent_utterance
    
        
async def main():
    from headjack_server.models import cli_agent_input
    model = ''
    agent = BasicQAAgent([MetricSearchTool(model, "Tool to search for metric knowledge.", "metric_knowledge", nodes = False),
                          MetricSearchTool(model, "Tool to search for metric nodes.", "metric_nodes", knowledge = False)])
    
    asyncio.run(agent(cli_agent_input()))
