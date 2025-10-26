import asyncio
import ai.tools.models.blocks as blocks

from claude_agent_sdk import *
from typing import AsyncGenerator, Dict

DEFAULT_MODEL = "claude-sonnet-4-5"
DEFAULT_SYSTEM = "당신은 기상캐스터입니다. 날씨정보에 대한 정보를 전달해주세요."
DEFAULT_TURNS = 5


async def stream_claude(
    prompt: str,
    model: str,
    instructions: str,
    max_turns: int,
    temperature: float,
    allow_tools: list[str],
    disallowed_tools: list[str],
    mcp_servers: dict,
    sub_agents: object,
    session_id: str
) -> AsyncGenerator[Dict, None]:
    print("stream_claude 호출")

    async with ClaudeSDKClient(
        ClaudeAgentOptions(
            model=model,
            system_prompt=instructions,
            max_turns=max_turns,
            permission_mode=,
            resume=session_id,
        )
    ) as client:
        await client.query(prompt)
        print("메시지 쿼리 실행")

        async for message in client.receive_response():
            message_type = type(message).__name__
            print(f"메시지: {message}")

            if hasattr(message, "content"):
                for block in message.content:
                    if message_type == "AssistantMessage":
                        if isinstance(block, ToolUseBlock):
                            yield blocks.tool_use(block)

                        if isinstance(block, TextBlock):
                            print(f"메세지 시작: {message_type}")
                            yield blocks.text_start()

                            words = block.text.split(' ')
                            print(f"워드: {words}")
                            for i, word in enumerate(words):
                                if i > 0:
                                    yield blocks.text_chunk(' ')  # 줄바꿈 추가
                                yield blocks.text_chunk(word)
                                await asyncio.sleep(0.05)  # 단어별 지연

                            # 메시지 block 종료
                            yield blocks.text_result(block)

                    if message_type == "UserMessage":
                        if isinstance(block, ToolResultBlock):
                            if getattr(block, 'is_error', True):
                                if _is_critical_error(block.content):
                                    print("권한 오류로 인한 대화 종료")
                                    yield blocks.tool_error(block)
                                    return

                            yield blocks.tool_result(block)

            elif message_type == "ResultMessage":
                if hasattr(message, "subtype"):
                    if message.subtype == 'error_max_turns':
                        yield blocks.result_error(message.subtype, message.session_id, "최대 턴수를 초과했습니다. 관리자에 문의하세요.")
                        return
                    elif message.subtype != 'success':
                        yield blocks.result_error(message.subtype, message.session_id, "알수 없는 오류입니다. 관리자에 문의하세요.")
                        return

                print(f"[SUCCESS] 작업 완료!")
                print(f"[COST] 토큰 비용: ${message.total_cost_usd:.4f}")
                print(f"[TIME] 작업 시간: {message.duration_ms}ms")
                print(f"[TURNS] 작업 횟수: {message.num_turns}")

def _is_critical_error(error_content: str) -> bool:
    """에러가 심각한지 판단"""
    critical_patterns = [
        "requested permissions",
    ]

    return any(pattern in error_content.lower() for pattern in critical_patterns)