from ai.tools.anthropic import Anthropic

from ai.system_prompt import FULLSTACK_DEVELOPER

class ToolAgents:
    def __init__(self):
        self.anthropic = Anthropic(system_prompt=FULLSTACK_DEVELOPER)

    async def chat(self, message):
        async for chunk in self.anthropic.chat(message):
            yield chunk