function isResponseCompleted(interval, status) {
    if (!status) {
        clearInterval(interval);
        createMessage("죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.", true);
        return false;
    }

    return true;
}

async function processStream(firstMessage, interval, response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let textMessage = firstMessage;
    let toolMessage = null;
    let isFirstResponse = true;
    let assistantResponse = "";
    let buffer = "";

    while (true) {
        const {done, value} = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, {stream: true});
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
                            clearInterval(interval);
                            if (!isFirstResponse) {
                                textMessage = createMessage("", true); // 새로운 박스 생성 및 타겟팅
                            }
                            isFirstResponse = false;
                            assistantResponse = '';                  // chunk 초기화
                        }

                        if (data.type === "text_chunk") {
                            assistantResponse += data.text;
                            textMessage.innerHTML = md.render(assistantResponse);
                        }

                        if (data.type === "text_result") {
                            if (toolMessage) {
                                updateToolStatus(toolMessage, true);
                                toolMessage = null;
                            }
                        }

                        if (data.type === "tool_use") {
                            if (!toolMessage) {
                                toolMessage = createToolMessage();
                            }
                            addUseSteps(toolMessage, data.name, md.render(JSON.stringify(data.input, null, 2)));
                        }

                        if (data.type === "tool_result") {
                            toolMessage && addResultSteps(toolMessage, data.content, data.is_error);
                        }

                        if (data.type === "tool_error") {
                            toolMessage && addErrorSteps(toolMessage, data.error);
                        }

                        if (data.type === "result_error") {
                            console.log("result error 호출");
                            if (toolMessage) {
                                updateToolStatus(toolMessage, false);
                                toolMessage = null;
                            }

                            textMessage = createMessage(data.error, true);
                            assistantResponse = '';
                        }

                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                } catch (parseError) {
                    console.error('Error parsing streaming data:', parseError, 'Line:', line);
                }
            }
        }
    }
}

function createLoadingInterval(firstMessage) {
    const contentElement = firstMessage.querySelector('.markdown-content');
    let dotCount = 0;

    return setInterval(() => {
        dotCount = (dotCount % 3) + 1;
        contentElement.textContent = '.'.repeat(dotCount);
    }, 500);
}

function createMessage(message,
                       isAgent = false,
                       steps = "Working",
                       profilePath = "/image/mobius-nox.gif") {

    const messageContainer = `
        <div class="message-wrapper">
            <div class="message ${isAgent ? 'assistant' : 'user'}">
                <div class="message-icon">
                    <img src="${profilePath}" alt="agent-profile" class="assistant-icon" />
                </div>
                <div class="message-content">
                    <div class="markdown-content scroll">${message}</div>
                    <div class="timestamp">${formatTime()}</div>
                </div>
            </div>
        </div>
    `
    chatContainer.insertAdjacentHTML("beforeend", messageContainer)
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return chatContainer.lastElementChild.querySelector(".message-content");
}

function createToolMessage(profilePath = "/image/mobius-nox.gif") {
    const uniqueId = 'tool-message-' + Date.now() + '-' + Math.random().toString(36).slice(2, 2 + 9);

    const messageContainer = `
        <div class="message-wrapper">
            <div class="message assistant tool-use">
                <div class="message-icon">
                    <img src="${profilePath}" alt="agent-profile" class="assistant-icon" />
                </div>
                <div class="message-content tool-content">
                    <div class="tool-header" onclick="toggleToolContent('${uniqueId}')" style="cursor: pointer;">
                        <span class="tool-label">작업중</span>
                        <div class="tool-status-container">
                            <div class="tool-status-spinner"></div>
                        </div>
                        <svg class="toggle-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="transform: rotate(-90deg);">
                            <path d="M19 9L12 16L5 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div class="collapsible-content" id="${uniqueId}" style="display: none;">
                        <div class="tool-steps"></div>
                        <div class="timestamp">${formatTime()}</div>
                    </div>
                </div>
            </div>
        </div>
    `
    chatContainer.insertAdjacentHTML("beforeend", messageContainer)
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return chatContainer.lastElementChild.querySelector(".message-content")
}

function addUseSteps(element, name, value) {
    const steps = `
        <div class="tool-step tool-use-step">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 사용</span>
                <span class="tool-name">${name}</span>
            </div>
            <div class="tool-input">${value}</div>
        </div>
    `
    addSteps(element, steps);
}

function addResultSteps(element, content, isError) {
    const steps = `
        <div class="tool-step tool-result-step ${isError ? 'failure' : 'success'}">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 결과</span>
                <span class="tool-status ${isError ? 'failure' : 'success'}">${isError ? '실패' : '성공'}</span>
            </div>
            <div class="tool-output">${content}</div>
        </div>
    `;
    addSteps(element, steps);
}

function addErrorSteps(element, error) {
    const steps = `
        <div class="tool-step tool-error-step">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 오류</span>
            </div>
            <div class="tool-error-content">${error}</div>
        </div>
    `;
    addSteps(element, steps);
    updateToolStatus(element, false);
}

function addSteps(element, steps) {
    const stepContainer = element.querySelector('.tool-steps');
    stepContainer.insertAdjacentHTML("beforeend", steps);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateToolStatus(element, isCompleted) {
    const stepContainer = element.querySelector('.tool-steps');
    const labelContainer = element.querySelector('.tool-label');
    const statusContainer = element.querySelector('.tool-status-container');

    if (stepContainer.classList.contains('tool-error-step')) {
        return;
    }

    labelContainer.textContent = isCompleted ? "완료" : "실패";

    if (statusContainer) {
        // 작업 완료 - 스피너를 성공/실패 아이콘으로 교체
        const iconClass = isCompleted ? "fa-check-circle" : "fa-times-circle";
        const iconColor = isCompleted ? '#047857' : '#b91c1c';
        statusContainer.outerHTML = `<i class="fa ${iconClass}" style="color: ${iconColor}; font-size: 16px;"></i>`;
    }
}

// 도구 메시지 토글 함수
function toggleToolContent(contentId) {
    const content = document.getElementById(contentId);
    const header = content.closest('.tool-content').querySelector('.tool-header');
    const toggleIcon = header.querySelector('.toggle-icon');

    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggleIcon.style.transform = 'rotate(0deg)';
    } else {
        content.style.display = 'none';
        toggleIcon.style.transform = 'rotate(-90deg)';
    }
}