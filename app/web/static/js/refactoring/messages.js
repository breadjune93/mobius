import {md} from './markdown.js';
import {formatTime, qs} from './utils.js';

const chatContainer = () => qs('.chat-container');

function createContents(message) {
    return `
    <div class="markdown-content scroll">${message || ''}</div>
    <div class="timestamp">${formatTime()}</div>
  `;
}

export function createMessage(message, isAgent = false, isTools = false, steps = 'Working', profilePath = '/image/mobius-nox.gif') {
    const cc = chatContainer();
    if (!cc) return null;
    const tpl = `
    <div class="message-wrapper">
        <div class="message ${isAgent ? 'assistant' : 'user'} ${isTools ? 'tool-use' : ''}">
            <div class="message-icon">
                <img src="${profilePath}" alt="agent-profile" class="assistant-icon" />
            </div>
            <div class="message-content ${isTools ? 'tool-content' : ''}">
                ${isTools ? createTools(steps) : createContents(message)}
            </div>
        </div>
    </div>`;
    cc.insertAdjacentHTML('beforeend', tpl);
    cc.scrollTop = cc.scrollHeight;
    return cc.lastElementChild.querySelector('.message-content');
}

// ---- Tool message helpers (기존 DOM 구조 유지) ----
function createTools() {
    return `<div class="tool-header" data-target="" ></div>`;
} // 실제 UI가 있다면 여기 유지

export function createToolMessage(profilePath = '/image/mobius-nox.gif') {
    const cc = chatContainer();
    if (!cc) return null;
    const id = 'tool-message-' + Date.now() + '-' + Math.random().toString(36).slice(2, 11);
    const tpl = `
    <div class="message-wrapper">
      <div class="message assistant tool-use">
        <div class="message-icon">
          <img src="${profilePath}" alt="agent-profile" class="assistant-icon" />
        </div>
        <div class="message-content tool-content">
          <div class="tool-header" data-target="${id}" style="cursor:pointer;">
            <span class="tool-label">작업중</span>
            <div class="tool-status-container"><div class="tool-status-spinner"></div></div>
            <svg class="toggle-icon" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M19 9L12 16L5 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div class="collapsible-content" id="${id}" style="display:none;">
            <div class="tool-steps"></div>
            <div class="timestamp">${formatTime()}</div>
          </div>
        </div>
      </div>
    </div>`;
    cc.insertAdjacentHTML('beforeend', tpl);
    cc.scrollTop = cc.scrollHeight;
    return cc.lastElementChild.querySelector('.message-content');
}

// 이벤트 위임(토글)
document.addEventListener('click', (e) => {
    const header = e.target.closest('.tool-header');
    if (!header) return;
    const id = header.getAttribute('data-target');
    const content = id && document.getElementById(id);
    const icon = header.querySelector('.toggle-icon');
    if (!content) return;
    const shown = content.style.display !== 'none';
    content.style.display = shown ? 'none' : 'block';
    if (icon) icon.style.transform = shown ? 'rotate(-90deg)' : 'rotate(0deg)';
});

export function addUseSteps(element, name, valueHtml) {
    const stepContainer = element.querySelector('.tool-steps');
    stepContainer?.insertAdjacentHTML('beforeend', `
    <div class="tool-step tool-use-step">
      <div class="tool-step-header">
        <span class="tool-step-label">도구 사용</span>
        <span class="tool-name">${name}</span>
      </div>
      <div class="tool-input">${valueHtml}</div>
    </div>`);
    chatContainer().scrollTop = chatContainer().scrollHeight;
}

export function addResultSteps(element, contentHtml, isError) {
    const stepContainer = element.querySelector('.tool-steps');
    stepContainer?.insertAdjacentHTML('beforeend', `
    <div class="tool-step tool-result-step ${isError ? 'failure' : 'success'}">
      <div class="tool-step-header">
        <span class="tool-step-label">도구 결과</span>
        <span class="tool-status ${isError ? 'failure' : 'success'}">${isError ? '실패' : '성공'}</span>
      </div>
      <div class="tool-output">${contentHtml}</div>
    </div>`);
    chatContainer().scrollTop = chatContainer().scrollHeight;
}

export function addErrorSteps(element, errorHtml) {
    const stepContainer = element.querySelector('.tool-steps');
    stepContainer?.insertAdjacentHTML('beforeend', `
    <div class="tool-step tool-error-step">
      <div class="tool-step-header"><span class="tool-step-label">도구 오류</span></div>
      <div class="tool-error-content">${errorHtml}</div>
    </div>`);
    updateToolStatus(element, false);
}

export function updateToolStatus(element, isCompleted) {
    const label = element.querySelector('.tool-label');
    const statusWrap = element.querySelector('.tool-status-container');
    if (element.querySelector('.tool-error-step')) return;
    if (label) label.textContent = isCompleted ? '완료' : '실패';
    if (statusWrap) {
        const iconClass = isCompleted ? 'fa-check-circle' : 'fa-times-circle';
        const iconColor = isCompleted ? '#047857' : '#b91c1c';
        statusWrap.outerHTML = `<i class="fa ${iconClass}" style="color:${iconColor};font-size:16px;"></i>`;
    }
}

export function createLoadingInterval(messageElement) {
    const contentEl = messageElement.querySelector('.markdown-content');
    let dot = 0;
    return setInterval(() => {
        dot = (dot % 3) + 1;
        if (contentEl) contentEl.textContent = '.'.repeat(dot);
    }, 500);
}

export function isResponseCompleted(interval, status) {
    if (!status) {
        clearInterval(interval);
        createMessage('죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.', true);
        return false;
    }
    return true;
}

// SSE/NDJSON 스트림 파서
export async function processStream(firstMessage, interval, response) {
    try {
        const reader = response?.body?.getReader?.();
        if (!reader) throw new Error('ReadableStream을 찾을 수 없습니다.');
        const decoder = new TextDecoder();
        let textMessage = firstMessage;
        let toolMessage = null;
        let isFirst = true;
        let assistant = '';
        let buffer = '';

        for (; ;) {
            const {value, done} = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, {stream: true});
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                try {
                    const data = JSON.parse(line.slice(6).trim());
                    if (data.type === 'text_start') {
                        clearInterval(interval);
                        if (!isFirst) textMessage = createMessage('', true);
                        isFirst = false;
                        assistant = '';
                    }
                    if (data.type === 'text_chunk') {
                        assistant += data.text;
                        textMessage.innerHTML = md.render(assistant);
                    }
                    if (data.type === 'tool_use') {
                        toolMessage ||= createToolMessage();
                        addUseSteps(toolMessage, data.name, md.render('```json\n' + JSON.stringify(data.input, null, 2) + '\n```'));
                    }
                    if (data.type === 'tool_result') {
                        toolMessage && addResultSteps(toolMessage, md.render(String(data.content ?? '')), data.is_error);
                    }
                    if (data.type === 'tool_error') {
                        toolMessage && addErrorSteps(toolMessage, md.render(String(data.error ?? '')));
                    }
                    if (data.type === 'text_end') {
                        if (toolMessage) {
                            updateToolStatus(toolMessage, true);
                            toolMessage = null;
                        }
                    }
                    if (data.type === 'result_error') {
                        if (toolMessage) {
                            updateToolStatus(toolMessage, false);
                            toolMessage = null;
                        }
                        textMessage = createMessage(String(data.error ?? '에러'), true);
                        assistant = '';
                    }
                    chatContainer().scrollTop = chatContainer().scrollHeight;
                } catch (e) {
                    console.error('스트림 파싱 오류:', e, 'Line:', line);
                }
            }
        }
    } catch (err) {
        console.error('processStream 실패:', err);
        clearInterval(interval);
        createMessage('스트림 처리 중 오류가 발생했습니다.', true);
    }
}