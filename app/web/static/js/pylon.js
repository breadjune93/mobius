const formTextarea = document.querySelector('.form-textarea');
const sendButton = document.querySelector('.send-button');
const chatContainer = document.querySelector('.chat-container');
const addAgent = document.querySelector('#add_agent');
const agentSelect = document.querySelector('#agent_select');

const urlParams = new URLSearchParams(window.location.search);
const pylonId = urlParams.get('id');

let pylonAgentCount = 0;
let agents = []; // 전역 변수로 에이전트 목록 저장

// 에이전트 추가 모달 초기화
window.addAgentModal = new Modal(
    document.querySelector("#add_agent"),
    document.querySelector("#add_agent_modal")
);

// 알림 모달 초기화
window.alertModal = new Modal(
    null,
    document.querySelector("#alert_modal"),
    null
);

getPylon();

// 에이전트 생성
if (addAgent) {
    addAgent.addEventListener("click", loadAgents);
}

// 에이전트 선택
if (agentSelect) {
    agentSelect.addEventListener('change', handleAgentSelection);
}

formTextarea.addEventListener('input', function() {
    const style = window.getComputedStyle(this);
    const maxHeight = parseFloat(style.maxHeight);
    const scrollHeight = this.scrollHeight;

    this.style.height = 'auto';
    this.style.height = `${Math.min(scrollHeight, 500)}px`;

    (scrollHeight > maxHeight) ? this.classList.add('on-scroll') : this.classList.remove('on-scroll');
});


// Enter 검색
formTextarea.addEventListener('keydown', (e) => keydownSendStreamMessage(e));

// 검색
sendButton.addEventListener('click', sendStreamMessage);


async function getPylon() {
    try {
        const response = await window.api.get(`/api/v1/nexus/pylon/${pylonId}`);
        const body = await response.body;
        console.log("pylon body: ", body);

        if (response.status) {
            const pylon = await body['pylon'];
            const pylonTitle = document.querySelector('#pylon_title');
            const pylonDesc = document.querySelector('#pylon_desc');
            const agentEmpty = document.querySelector('#agent_empty');

            pylonTitle && (pylonTitle.textContent = pylon?.title);
            pylonDesc && (pylonDesc.textContent = pylon?.description);

            pylonAgentCount = pylon?.agent_count || 0;

            if (agentEmpty) {
                agentEmpty.style.display = pylonAgentCount === 0 ? 'block' : 'none';
            }
        } else if (response) {
            alert(body.detail || '파일런 정보를 불러올 수 없습니다.');
            window.location.href = '/nexus';
        }
    } catch (error) {
        alert(error.detail || '파일런 정보를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.');
        window.location.href = '/nexus';
    }
}

async function keydownSendStreamMessage(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        await sendStreamMessage();
    }
}

async function sendStreamMessage() {
    if (pylonAgentCount === 0) {
        showAlertModal('에이전트를 먼저 추가해주세요.');
        return;
    }

    const message = formTextarea.value.trim();
    if (message) {
        console.log('Sending message:', message);

        // 입력창 초기화
        formTextarea.value = '';

        // 사용자 메시지를 채팅에 추가
        createUserMessage(message);

        // Update current chat preview in sidebar
        const activeChat = document.querySelector('.chat-item.active');
        if (activeChat) {
            const preview = activeChat.querySelector('.chat-preview');
            if (preview) {
                preview.textContent = message.length > 30 ? message.substring(0, 30) + '...' : message;
            }
        }

        let assistantResponse = "";
        let isFirstResponse = true;
        let messageBox = createAssistantMessage(".");
        let loadingInterval = messageLoading(messageBox);
        let currentToolMessage = null;

        try {
            const { status, response } = await window.api.stream('/api/v1/pylon/stream/claude', { message: message });

            if (!status) {
                clearInterval(loadingInterval);
                createAssistantMessage("죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.");
                new Error(`❌ 스트림 오류!: ${response.status}`);
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const {done, value} = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');

                // 마지막 라인은 불완전할 수 있으므로 버퍼에 보관
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const jsonStr = line.substring(6).trim();
                            if (jsonStr) {
                                const data = JSON.parse(jsonStr);

                                console.log("data: ", data);

                                if (data.type === "text_start") {
                                    if (!isFirstResponse) {
                                        messageBox = createAssistantMessage(""); // 새로운 박스 생성 및 타겟팅
                                    }
                                    clearInterval(loadingInterval);
                                    isFirstResponse = false;
                                    assistantResponse = '';                  // chunk 초기화
                                }

                                if (data.type === "text_chunk") {
                                    assistantResponse += data.text;
                                    messageBox.innerHTML = md.render(assistantResponse);
                                }

                                if (data.type === "tool_use") {
                                    if (!currentToolMessage) {
                                        currentToolMessage = createToolMessage();
                                    }
                                    addToolUseStep(currentToolMessage, data.name, md.render(JSON.stringify(data.input, null, 2)));
                                }

                                if (data.type === "tool_result") {
                                    if (currentToolMessage) {
                                        addToolResultStep(currentToolMessage, data.content, data.is_error);
                                    }
                                }

                                if (data.type === "tool_error"){
                                    if (currentToolMessage) {
                                        addToolErrorStep(currentToolMessage, data.error);
                                    }
                                }

                                if (data.type === "text_end") {
                                    console.log('메시지 박스 종료');
                                    // 도구 메시지가 있다면 완료 처리
                                    if (currentToolMessage) {
                                        completeToolMessage(currentToolMessage);
                                        currentToolMessage = null;
                                    }
                                }

                                 chatContainer.scrollTop = chatContainer.scrollHeight;
                            }
                        } catch (parseError) {
                            console.error('Error parsing streaming data:', parseError, 'Line:', line);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('메세지 스트림 에러:', error);
            clearInterval(loadingInterval);
            messageBox.innerHTML = '죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.';
        }
    }
}

// 로딩 점 애니메이션을 위한 함수
function messageLoading(contentBox) {
    let dotCount = 0;
    return setInterval(() => {
        dotCount = (dotCount % 3) + 1;
        contentBox.textContent = '.'.repeat(dotCount);
    }, 500);
}


// 알림 모달 표시 함수
function showAlertModal(message, title = '알림') {
    const alertModalTitle = document.querySelector('#alert_modal_title');
    const alertModalMessage = document.querySelector('#alert_modal_message');

    if (alertModalTitle) {
        alertModalTitle.textContent = title;
    }

    if (alertModalMessage) {
        alertModalMessage.textContent = message;
    }

    window.alertModal.open();
}

// 에이전트 목록 로드 및 selectbox 채우기
async function loadAgents() {
    try {
        const response = await window.api.get('/api/v1/pylon/agents');
        const body = await response.body;

        if (response.status && body["agents"]) {
            const agents = body["agents"];
            const agentSelect = document.querySelector('#agent_select');

            if (agentSelect) {
                // 기존 옵션 제거 (첫 번째 옵션 제외)
                agentSelect.innerHTML = '<option value="">에이전트를 선택하세요</option>';

                // 에이전트 목록을 selectbox에 추가
                agents.forEach(agent => {
                    const option = document.createElement('option');
                    option.value = agent.id;
                    option.textContent = `${agent.name}(${agent.id})`;
                    option.dataset.agent = JSON.stringify(agent); // 에이전트 정보를 data attribute로 저장
                    agentSelect.appendChild(option);
                });
            }

            // 상세 정보 영역 초기화
            const agentDetail = document.querySelector('#agent_detail');
            if (agentDetail) {
                agentDetail.style.display = 'none';
            }
        } else {
            showAlertModal('에이전트 목록을 불러올 수 없습니다.');
        }
    } catch (error) {
        console.error('에이전트 로드 에러:', error);
        showAlertModal('에이전트 목록을 불러오는 중 오류가 발생했습니다.');
    }
}

// 에이전트 선택 시 상세 정보 표시
function handleAgentSelection(event) {
    const selectedOption = event.target.options[event.target.selectedIndex];
    const agentDetail = document.querySelector('#agent_detail');

    if (!selectedOption.value || !agentDetail) {
        if (agentDetail) {
            agentDetail.style.display = 'none';
        }
        return;
    }

    try {
        const agent = JSON.parse(selectedOption.dataset.agent);

        // 상세 정보 표시
        document.querySelector('#agent_detail_name').textContent = `${agent.name}(${agent.id})`;
        document.querySelector('#agent_detail_assistant').textContent = agent.assistant || 'N/A';
        document.querySelector('#agent_detail_model').textContent = agent.model || 'N/A';
        document.querySelector('#agent_detail_description').textContent = agent.description || '설명 없음';

        // 상세 정보 영역 표시
        agentDetail.style.display = 'block';
    } catch (error) {
        console.error('에이전트 정보 파싱 에러:', error);
        agentDetail.style.display = 'none';
    }
}

