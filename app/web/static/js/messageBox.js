

// 사용자 메시지 생성
function createUserMessage(message) {
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    messageWrapper.innerHTML = `
        <div class="message user">
            <div class="message-icon">
                <i class="fa fa-user"></i>
            </div>
            <div class="message-content">
                <span>${message}</span>
                <div class="timestamp">${formatTime()}</div>
            </div>
        </div>
    `;
    chatContainer.appendChild(messageWrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 어시스턴트 메시지 생성
function createAssistantMessage(message) {
    const currentTheme = window.getTheme ? window.getTheme() : 'dark';
    const iconSrc = currentTheme === 'white' ? '/image/mobius-rumos.gif' : '/image/mobius-nox.gif';

    const messageBox = `
        <div class="message-wrapper">
            <div class="message assistant">
                <div class="message-icon">
                    <img src="${iconSrc}" alt="agent-profile" class="assistant-icon" />
                </div>
                <div class="message-content">
                    <div class="markdown-content scroll">${message}</div>
                    <div class="timestamp">${formatTime()}</div>
                </div>
            </div>
        </div>
    `;
    chatContainer.insertAdjacentHTML("beforeend", messageBox)
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return chatContainer.lastElementChild.querySelector(".markdown-content");
}

// 통합 도구 메시지 생성
function createToolMessage() {
    const currentTheme = window.getTheme ? window.getTheme() : 'dark';
    const iconSrc = currentTheme === 'white' ? '/image/mobius-rumos.gif' : '/image/mobius-nox.gif';
    const uniqueId = 'tool-message-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    const messageBox = `
        <div class="message-wrapper">
            <div class="message assistant tool-use">
                <div class="message-icon">
                    <img src="${iconSrc}" alt="agent-profile" class="assistant-icon" />
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
    `;
    chatContainer.insertAdjacentHTML("beforeend", messageBox);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return {
        messageElement: chatContainer.lastElementChild,
        stepsContainer: chatContainer.lastElementChild.querySelector('.tool-steps'),
        statusContainer: chatContainer.lastElementChild.querySelector('.tool-status-container'),
        labelElement: chatContainer.lastElementChild.querySelector('.tool-label')
    };
}

// 도구 사용 단계 추가
function addToolUseStep(toolMessage, toolName, inputValue) {
    const stepHtml = `
        <div class="tool-step tool-use-step">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 사용</span>
                <span class="tool-name">${toolName}</span>
            </div>
            <div class="tool-input">${inputValue}</div>
        </div>
    `;
    toolMessage.stepsContainer.insertAdjacentHTML("beforeend", stepHtml);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 도구 결과 단계 추가
function addToolResultStep(toolMessage, content, isError) {
    const stepHtml = `
        <div class="tool-step tool-result-step ${isError ? 'failure' : 'success'}">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 결과</span>
                <span class="tool-status ${isError ? 'failure' : 'success'}">${isError ? '실패' : '성공'}</span>
            </div>
            <div class="tool-output">${content}</div>
        </div>
    `;
    toolMessage.stepsContainer.insertAdjacentHTML("beforeend", stepHtml);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 도구 에러 단계 추가
function addToolErrorStep(toolMessage, error) {
    const stepHtml = `
        <div class="tool-step tool-error-step">
            <div class="tool-step-header">
                <span class="tool-step-label">도구 오류</span>
            </div>
            <div class="tool-error-content">${error}</div>
        </div>
    `;
    toolMessage.stepsContainer.insertAdjacentHTML("beforeend", stepHtml);
    updateToolStatus(toolMessage, '실패', false);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 도구 상태 업데이트 함수
function updateToolStatus(toolMessage, statusText, isSuccess) {
    const labelElement = toolMessage.labelElement;
    const spinner = toolMessage.statusContainer.querySelector('.tool-status-spinner');
    
    labelElement.textContent = statusText;
    
    if (spinner) {
        if (isSuccess !== null) {
            // 작업 완료 - 스피너를 성공/실패 아이콘으로 교체
            const iconClass = isSuccess ? 'fa-check-circle' : 'fa-times-circle';
            const iconColor = isSuccess ? '#047857' : '#b91c1c';
            spinner.outerHTML = `<i class="fa ${iconClass}" style="color: ${iconColor}; font-size: 16px;"></i>`;
        }
    }
}

// 작업 완료 처리 함수
function completeToolMessage(toolMessage) {
    // 마지막 단계의 결과에 따라 상태 결정
    const lastStep = toolMessage.stepsContainer.lastElementChild;
    let isSuccess = true;
    let statusText = '완료';
    
    if (lastStep) {
        if (lastStep.classList.contains('tool-error-step')) {
            isSuccess = false;
            statusText = '실패';
        } else if (lastStep.classList.contains('tool-result-step')) {
            isSuccess = !lastStep.classList.contains('failure');
            statusText = isSuccess ? '완료' : '실패';
        }
    }
    
    updateToolStatus(toolMessage, statusText, isSuccess);
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