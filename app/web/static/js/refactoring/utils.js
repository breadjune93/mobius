export const qs  = (sel, root=document) => root.querySelector(sel);
export const qsa = (sel, root=document) => Array.from(root.querySelectorAll(sel));
export const on  = (el, type, fn, opts) => el?.addEventListener(type, fn, opts);

export const formatTime = (d=new Date()) => d.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});

export function ensureAriaLive() {
  let node = qs('#aria_live_region');
  if (!node) {
    node = document.createElement('div');
    node.id = 'aria_live_region';
    node.setAttribute('role','status');
    node.setAttribute('aria-live','polite');
    node.style.cssText = 'position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0,0,0,0)';
    document.body.appendChild(node);
  }
  return (msg) => (node.textContent = msg || '');
}
export const ariaLive = ensureAriaLive();

export function autosizeTextarea(ta, maxPx=500) {
  if (!ta) return;
  ta.style.height = 'auto';
  const styleMax = parseFloat(getComputedStyle(ta).maxHeight) || maxPx;
  const h = Math.min(ta.scrollHeight, styleMax);
  ta.style.height = `${h}px`;
  ta.classList.toggle('on-scroll', ta.scrollHeight > styleMax);
}

export function showAlertModal(message, title='알림') {
  const t = qs('#alert_modal_title');
  const m = qs('#alert_modal_message');
  if (t) t.textContent = title;
  if (m) m.textContent = message;
  // window.Modal 인스턴스가 있으면 사용, 없으면 백업으로 단순 표시
  if (window.alertModal?.open) window.alertModal.open();
  else qs('#alert_modal')?.classList?.add?.('open');
  ariaLive(`${title}: ${message}`);
}