import sys, asyncio
if sys.platform.startswith("win"):
    print("set_event_loop_policy 호출")
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())