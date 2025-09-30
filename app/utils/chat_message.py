from types import MappingProxyType
from typing import Final

TOOLS: Final = MappingProxyType({
    "Task": "작업 관리",
    "Bash": "실행",
    "Glob": "파일 패턴 매칭",
    "Grep": "텍스트 검색",
    "ExitPlanMode": "계획 모드 종료",
    "Read": "파일 읽기",
    "Edit": "파일 편집",
    "MultiEdit": "여러 파일 동시 편집",
    "Write": "파일 쓰기",
    "NotebookEdit": "노트 파일 편집",
    "WebFetch": "웹 페이지 가져오기",
    "TodoWrite": "할일 작성",
    "WebSearch": "웹 검색",
    "BashOutput": "출력 처리",
    "KillBash": "프로세스 종료"
})