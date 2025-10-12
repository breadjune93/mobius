// window.api가 있으면 그걸 쓰고, 없으면 fetch로 대체
export async function get(path, opts = {}) {
  if (window.api?.get) return window.api.get(path, opts);
  const res = await fetch(path, { method: 'GET', headers: { 'Content-Type': 'application/json', ...(opts.headers||{}) }});
  const body = await (res.headers.get('content-type')?.includes('application/json') ? res.json() : res.text());
  return { status: res.ok, body };
}

export async function stream(path, body = {}, opts = {}) {
  if (window.api?.stream) return window.api.stream(path, body, opts);
  // 서버가 SSE/Stream을 지원한다고 가정
  const res = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(opts.headers||{}) },
    body: JSON.stringify(body)
  });
  return { status: res.ok ? 200 : res.status, response: res };
}