from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio


async def interactive_session():
    async with ClaudeSDKClient(
            ClaudeAgentOptions(
                model="claude-sonnet-4-5",
                system_prompt="당신은 기상캐스터입니다. 날씨정보에 대한 정보를 전달해주세요.",
                max_turns=5
            )
    ) as client:
        # 초기 메시지 전송
        await client.query("오늘 대한민국 날씨가 어떤가요?")

        # 응답 처리
        async for msg in client.receive_response():
            message_type = type(msg).__name__
            print(f"message: {message_type}")
            print(msg)

asyncio.run(interactive_session())