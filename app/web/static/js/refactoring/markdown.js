// 전역 markdownit(예: CDN) 사용 → 보강 설정 후 md 인스턴스 export
const mdGlobal = window.markdownit?.({ html:true, breaks:true, linkify:true, typographer:true });
if (!mdGlobal) {
  throw new Error('markdown-it이 로드되지 않았습니다. index.html에서 CDN을 먼저 불러오세요.');
}

mdGlobal.renderer.rules.heading_open = (tokens, idx) => {
  const level = tokens[idx].markup?.length || 1;
  return `<h${level} class="response-header-${level===1?'1':'2'}">${level===1?'<br>':''}`;
};
mdGlobal.renderer.rules.paragraph_open = () => '<p class="response-paragraph">';
mdGlobal.renderer.rules.code_block = (tokens, idx) =>
  `<pre class="response-code-block"><code>${mdGlobal.utils.escapeHtml(tokens[idx].content)}</code></pre>`;
mdGlobal.renderer.rules.code_inline = (tokens, idx) =>
  `<code class="response-code-line">${mdGlobal.utils.escapeHtml(tokens[idx].content)}</code>`;
mdGlobal.renderer.rules.fence = (tokens, idx) => {
  const token = tokens[idx];
  const info = token.info ? mdGlobal.utils.escapeHtml(token.info.trim()) : '';
  const lang = info ? ` class="language-${info.split(/\s+/g)[0]}"` : '';
  return `<pre class="response-code-fence"><code${lang}>${mdGlobal.utils.escapeHtml(token.content)}</code></pre>`;
};

export const md = mdGlobal;