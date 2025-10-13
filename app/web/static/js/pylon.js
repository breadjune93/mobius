const formTextarea = document.querySelector('.form-textarea');
const sendButton = document.querySelector('.send-button');
const chatContainer = document.querySelector('.chat-container');
const agentSelect = document.querySelector('#agent_select');
const addAgentTrigger = document.querySelector('#add_agent');
const addAgent = document.querySelector('button[name=add-agent]');

const urlParams = new URLSearchParams(window.location.search);
const pylonId = urlParams.get('id');

let pylonAgentCount = 0;
let agents = []; // 전역 변수로 에이전트 목록 저장

getPylon();

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

/***********************
 *        Event        *
 ***********************/
// 에이전트 추가(모달)
addAgentTrigger?.addEventListener("click", loadAgents);

// 에이전트 선택
agentSelect?.addEventListener('change', handleAgentSelection);

// 에이전트 생성
addAgent?.addEventListener('click', createAgent);

// 프롬프트 입력
formTextarea?.addEventListener('input', (e) => keywordInput(e.target));

// 프롬프트 Enter 전송
formTextarea?.addEventListener('keydown', (e) => keydownSendStreamMessage(e));

// 프롬프트 전송
sendButton?.addEventListener('click', sendStreamMessage);


/***********************
 *       Function      *
 ***********************/
async function getPylon() {
    try {
        const response = await window.api.get(`/api/v1/nexus/pylon/${pylonId}`);
        const body = await response.body;
        console.log("pylon body: ", body);

        if (response.status) {
            const pylon = await body['pylon'];
            const pylonTitle = document.querySelector('#pylon_title');
            const pylonDesc = document.querySelector('#pylon_desc');
            const emptyState = document.querySelector('.empty-state');

            pylonTitle && (pylonTitle.textContent = pylon?.title);
            pylonDesc && (pylonDesc.textContent = pylon?.description);

            pylonAgentCount = pylon?.agent_count || 0;

            pylonAgentCount !== 0 && emptyState?.classList.add("disabled");
        } else if (response) {
            alert(body.detail || '파일런 정보를 불러올 수 없습니다.');
            window.location.href = '/nexus';
        }
    } catch (error) {
        alert(error.detail || '파일런 정보를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.');
        window.location.href = '/nexus';
    }
}

// 에이전트 리스트 조회
async function loadAgents() {
    try {
        const response = await window.api.get('/api/v1/pylon/agents');
        const body = await response.body;

        if (response.status && body["agents"]) {
            const agents = body["agents"];
            const agentSelect = document.querySelector('#agent_select');

            if (agentSelect) {
                agentSelect.innerHTML = '<option value="">에이전트를 선택하세요</option>';

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

async function createAgent() {
    window.addAgentModal.close();

    const agentSelect = document.querySelector("#agent_select");
    const emptyState = document.querySelector(".empty-state");
    const agentResponse = await window.api.get(`/api/v1/pylon/agent/${agentSelect.value}`);

    if (!agentResponse.status) {
        showAlertModal('에이전트 추가에 실패했습니다. 관리자에 문의하세요.');
        return;
    }

    const body = await agentResponse.body;
    const agent = await body['agent'];
    emptyState?.classList.add("disabled");

    const firstMessage = createMessage("", true);
    const loadingInterval = createLoadingInterval(firstMessage);

    const introducePrompt = JSON.stringify(agent) + `
        1. json 객체에서 name 을 항상 처음에 소개.
        2. 객체의 내용으로 짧게(100자 이내) 어떤 역할을 수행하는지 설명.
    `;

    console.log("소개 프롬프트: ", introducePrompt);

    try {
        const streamResponse = await window.api.stream('/api/v1/pylon/stream/claude', {
            message: introducePrompt
        });

        if (!isResponseCompleted(loadingInterval, streamResponse.status)) {
            return;
        }

        await processStream(firstMessage, loadingInterval, streamResponse.response);

        // TODO: 응답 받은 메시지에서 session ID와 에이전트 데이터들로 chats와 sessions 테이블에 저장
    } catch (error) {
        console.error('인트로 스트림 에러:', error);
        clearInterval(loadingInterval);
        createMessage("죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.", true);
    }
}

function keywordInput(element) {
    const style = window.getComputedStyle(element);
    const maxHeight = parseFloat(style.maxHeight);
    const scrollHeight = element.scrollHeight;

    element.style.height = 'auto';
    element.style.height = `${Math.min(scrollHeight, 500)}px`;

    (scrollHeight > maxHeight) ? element.classList.add('on-scroll') : element.classList.remove('on-scroll');
}

async function keydownSendStreamMessage(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        await sendStreamMessage();
    }
}

async function sendStreamMessage() {
    const message = formTextarea.value.trim();

    // if (pylonAgentCount === 0) {
    //     showAlertModal('에이전트를 먼저 추가해주세요.');
    //     return;
    // }

    if (!message) {
        showAlertModal('메시지를 입력해주세요.');
        return;
    }

    // 입력창 초기화
    formTextarea.value = '';

    // 사용자 메시지를 채팅에 추가
    createMessage(message);

    const firstMessage = createMessage("", true);
    const loadingInterval = createLoadingInterval(firstMessage);

    try {
        const streamResponse = await window.api.stream('/api/v1/pylon/stream/claude', { message: message });

        // 스트림 연결 확인
        if (!isResponseCompleted(loadingInterval, streamResponse.status)) {
            return;
        }

        await processStream(firstMessage, loadingInterval, streamResponse.response);

    } catch (error) {
        console.error('메세지 스트림 에러:', error);
        clearInterval(loadingInterval);
        createMessage("죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.", true);
    }
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


