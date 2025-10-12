import { get, stream } from './api.js';
import { qs, autosizeTextarea, ariaLive, showAlertModal } from './utils.js';
import {
  createMessage, createLoadingInterval, isResponseCompleted, processStream
} from './messages.js';

export function initPylon() {
  const $formTextarea   = qs('.form-textarea');
  const $sendButton     = qs('.send-button');
  const $agentSelect    = qs('#agent_select');
  const $addAgentTrig   = qs('#add_agent');
  const $addAgentBtn    = qs('button[name=add-agent]');

  const pylonId = new URLSearchParams(location.search).get('id');
  let pylonAgentCount = 0;

  // 모달 어댑트: 기존 전역 Modal이 있으면 활용
  if (window.Modal) {
    window.addAgentModal = new window.Modal($addAgentTrig, qs('#add_agent_modal'));
    window.alertModal    = new window.Modal(null, qs('#alert_modal'));
  }

  $addAgentTrig?.addEventListener('click', loadAgents);
  $agentSelect?.addEventListener('change', onSelectAgent);
  $addAgentBtn?.addEventListener('click', createAgent);
  $formTextarea?.addEventListener('input', (e) => autosizeTextarea(e.target));
  $formTextarea?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendStreamMessage(); }
  });
  $sendButton?.addEventListener('click', sendStreamMessage);

  getPylon();

  async function getPylon() {
    try {
      const res = await get(`/api/v1/nexus/pylon/${pylonId}`);
      const body = await res.body;
      if (!res.status) throw new Error(body?.detail || '파일런 정보를 불러올 수 없습니다.');

      const pylon = body?.pylon || {};
      qs('#pylon_title') && (qs('#pylon_title').textContent = pylon.title || '');
      qs('#pylon_desc')  && (qs('#pylon_desc').textContent  = pylon.description || '');

      pylonAgentCount = pylon.agent_count || 0;
      if (pylonAgentCount) qs('.empty-state')?.classList.add('disabled');
      ariaLive('파일런 정보를 불러왔습니다.');
    } catch (e) {
      showAlertModal(e.message || '파일런 정보를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.');
      location.href = '/nexus';
    }
  }

  async function loadAgents() {
    try {
      const res = await get('/api/v1/pylon/agents');
      const body = await res.body;
      const list = body?.agents;
      if (!res.status || !Array.isArray(list)) throw new Error('에이전트 목록을 불러올 수 없습니다.');

      if ($agentSelect) {
        $agentSelect.innerHTML = '<option value="">에이전트를 선택하세요</option>';
        const frag = document.createDocumentFragment();
        for (const a of list) {
          const opt = document.createElement('option');
          opt.value = a.id;
          opt.textContent = `${a.name}(${a.id})`;
          opt.dataset.agent = JSON.stringify(a);
          frag.appendChild(opt);
        }
        $agentSelect.appendChild(frag);
      }
      const $detail = qs('#agent_detail');
      if ($detail) $detail.style.display = 'none';
      ariaLive('에이전트 목록을 불러왔습니다.');
    } catch (e) {
      console.error('에이전트 로드 에러:', e);
      showAlertModal(e.message || '에이전트 목록을 불러오는 중 오류가 발생했습니다.');
    }
  }

  function onSelectAgent(e) {
    const opt = e.target.options[e.target.selectedIndex];
    const $detail = qs('#agent_detail');
    if (!opt?.value || !$detail) { if ($detail) $detail.style.display = 'none'; return; }
    try {
      const agent = JSON.parse(opt.dataset.agent);
      qs('#agent_detail_name').textContent = `${agent.name}(${agent.id})`;
      qs('#agent_detail_assistant').textContent = agent.assistant || 'N/A';
      qs('#agent_detail_model').textContent = agent.model || 'N/A';
      qs('#agent_detail_description').textContent = agent.description || '설명 없음';
      $detail.style.display = 'block';
    } catch (err) {
      console.error('에이전트 정보 파싱 에러:', err);
      $detail.style.display = 'none';
    }
  }

  async function createAgent() {
    window.addAgentModal?.close?.();
    const id = $agentSelect?.value;
    if (!id) return showAlertModal('에이전트를 선택하세요.');

    try {
      const res = await get(`/api/v1/pylon/agent/${id}`);
      if (!res.status) throw new Error('에이전트 추가에 실패했습니다. 관리자에 문의하세요.');
      const body = await res.body;
      const agent = body?.agent;
      if (!agent) throw new Error('에이전트 정보를 찾을 수 없습니다.');

      qs('.empty-state')?.classList.add('disabled');

      const first = createMessage('', true);
      const loading = createLoadingInterval(first);
      const introducePrompt =
        `${JSON.stringify(agent)}\n1. json 객체에서 name 을 항상 처음에 소개.\n2. 객체의 내용으로 짧게(100자 이내) 어떤 역할을 수행하는지 설명.`;

      const s = await stream('/api/v1/pylon/stream/claude', { message: introducePrompt });
      if (!isResponseCompleted(loading, s.status)) return;
      await processStream(first, loading, s.response);
    } catch (e) {
      console.error('에이전트 생성 에러:', e);
      showAlertModal(e.message || '에이전트 추가 중 오류가 발생했습니다.');
    }
  }

  async function sendStreamMessage() {
    const ta = $formTextarea;
    const msg = ta?.value?.trim();
    if (!msg) return showAlertModal('메시지를 입력해주세요.');

    ta.value = '';
    autosizeTextarea(ta);
    createMessage(msg);

    const first = createMessage('', true);
    const loading = createLoadingInterval(first);

    try {
      const s = await stream('/api/v1/pylon/stream/claude', { message: msg });
      if (!isResponseCompleted(loading, s.status)) return;
      await processStream(first, loading, s.response);
    } catch (e) {
      console.error('메세지 스트림 에러:', e);
      clearInterval(loading);
      createMessage('죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.', true);
    }
  }
}