# CLAUDE.md
이 파일은 Claude Code(claude.ai/code)가 이 저장소의 코드로 작업할 때 지침을 제공합니다.

## Project Overview
FastAPI와 Anthropic의 Claude API를 사용하여 구축된 Python 기반 AI 에이전트 애플리케이션입니다.<br>
이 시스템은 스트리밍 채팅 인터페이스를 통해 <br>
다양한 AI 에이전트 페르소나(웹 디자이너, 풀스택 개발자, 배포 전문가 등)와 상호 작용할 수 있는 웹 인터페이스를 제공합니다.

## Commands

### 애플리케이션 실행
```bash
  python chat/main.py
```
http://localhost:1993 에서 FastAPI 서버가 시작됩니다.

### 환경설정
`.env` 파일에 다음이 포함되어 있는지 확인하세요.
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key  
- `GOOGLE_API_KEY`: Google API key

### 종속성
이 프로젝트는 종속성 관리를 위해 pip를 사용합니다. 다음을 사용하여 종속성을 설치하세요.
```bash
pip install fastapi uvicorn python-dotenv langchain-openai langchain-anthropic claude-code-sdk
```

## Architecture

### Core Components

**Main Application (`main.py`)**
- Entry point that initializes FastAPI app with static file mounting
- Serves the chat interface and includes API routes

**AI Module (`ai/`)**
- `chains.py`: LangChain wrapper for OpenAI and Anthropic models
- `system_prompt.py`: Contains system prompts for different AI personas (FULLSTACK_DEVELOPER, WEB_DESIGNER, MARKUP_DEVELOPER, DEPLOYMENT_SPECIALIST, EVENT_MONITOR)
- `tools/anthropic.py`: Direct Anthropic API integration with streaming support
- `tools/models/`: Model-specific configurations

**Agent Module (`agent/`)**
- `developer.py`: DevelopAgent class that wraps Anthropic client with FULLSTACK_DEVELOPER persona
- Provides async chat streaming functionality

**Chat Module (`chat/`)**
- `route.py`: FastAPI router with chat endpoint that streams responses
- `chat.py`: FastAPI app configuration
- `views/`: Static HTML/CSS/JS files for the web interface

### Architecture Flow
```
Web Interface → FastAPI Route → DevelopAgent → Anthropic API → Stream Response
```

### Key Design Patterns

1. **Streaming Responses**: Uses FastAPI's StreamingResponse for real-time chat updates
2. **Agent Pattern**: Encapsulates AI personas in agent classes with specific system prompts
3. **Static File Serving**: FastAPI mounts static directories for frontend assets
4. **Environment Configuration**: Uses python-dotenv for API key management

### System Prompts
The application supports multiple AI personas defined in `ai/system_prompt.py`:
- `FULLSTACK_DEVELOPER`: Java 17/Spring Boot 3 expert with specific architectural guidelines
- `WEB_DESIGNER`: Modern web design and UX specialist  
- `MARKUP_DEVELOPER`: HTML/CSS markup specialist
- `DEPLOYMENT_SPECIALIST`: DevOps and infrastructure expert
- `EVENT_MONITOR`: System monitoring and observability specialist

## File Structure
```
agent-n/
├── main.py                 # FastAPI application entry point
├── .env                    # Environment variables (API keys)
├── agent/
│   └── developer.py        # DevelopAgent class
├── ai/
│   ├── chains.py          # LangChain model wrappers
│   ├── system_prompt.py   # AI persona system prompts
│   └── tools/
│       └── anthropic.py   # Direct Anthropic API client
└── chat/
    ├── route.py           # FastAPI routing
    ├── chat.py            # FastAPI configuration
    └── views/             # Static web assets
```

## Development Notes

- The application uses async/await patterns for streaming responses
- Currently configured for Claude Sonnet 4 model (`claude-sonnet-4-20250514`)
- Static files are served from `views/` subdirectories (css, js, image)
- Error handling is implemented in the streaming endpoint
- The web interface expects Server-Sent Events (SSE) format responses