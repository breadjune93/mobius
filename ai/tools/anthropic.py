from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ToolUseBlock, TextBlock, ToolResultBlock

import asyncio
import ai.tools.models.blocks as blocks


def _is_critical_error(error_content: str) -> bool:
    """에러가 심각한지 판단"""
    critical_patterns = [
        "requested permissions",
    ]

    return any(pattern in error_content.lower() for pattern in critical_patterns)


class Anthropic:
    def __init__(self,
                 system_prompt: str):
        self.client = None
        self._initialize(system_prompt)

    def _initialize(self, system_prompt):
        self.client = ClaudeSDKClient(
            options=ClaudeAgentOptions(
                model="claude-sonnet-4-5",
                system_prompt=system_prompt,
                max_turns=5
            )
        )

    async def chat(self, message):
        try:
            async with self.client as client:
                await client.query(message)

                async for message in client.receive_response():
                    message_type = type(message).__name__
                    print(f"message: {message}")

                    if message_type == "AssistantMessage":
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if isinstance(block, ToolUseBlock):
                                    yield blocks.tool_use(block)

                                if isinstance(block, TextBlock):
                                    yield blocks.text_start()

                                    words = block.text.split(' ')
                                    for i, word in enumerate(words):
                                        if i > 0:
                                            yield blocks.text_chunk(' ')  # 줄바꿈 추가
                                        yield blocks.text_chunk(word)
                                        await asyncio.sleep(0.05)  # 단어별 지연

                                    # 메시지 block 종료
                                    yield blocks.text_end()


                    if message_type == "UserMessage":
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if isinstance(block, ToolResultBlock):
                                    if getattr(block, 'is_error', True):
                                        if _is_critical_error(block.content):
                                            print("권한 오류로 인한 대화 종료")
                                            yield blocks.tool_error(block)
                                            # yield {"error": "Critical error occurred", "done": True}
                                            return

                                    yield blocks.tool_result(block)

                    elif message_type == "ResultMessage":
                        print(f"[SUCCESS] 작업 완료!")
                        print(f"[COST] 토큰 비용: ${message.total_cost_usd:.4f}")
                        print(f"[TIME] 작업 시간: {message.duration_ms}ms")
                        print(f"[TURNS] 작업 횟수: {message.num_turns}")

                    elif message_type == "ErrorMessage":
                        print(f"\n[ERROR] 오류!: {message.error}")
                        if "Permission denied" in str(message.error):
                            print("[PERMISSION DENIED] 작업에 대한 권한이 거부되었습니다.")
                        yield {"error": str(message.error), "done": True}
                        return

        except Exception as e:
            import traceback
            error_detail = f"{str(e)}\n{traceback.format_exc()}"
            print(f"[ERROR] Chat error: {error_detail}")
            yield {"error": str(e), "done": True}

