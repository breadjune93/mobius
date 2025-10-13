// markdown-it 인스턴스 생성 및 설정
const md = window.markdownit({
    html: true,
    breaks: true,        // 단일 줄바꿈을 <br>로 변환
    linkify: true,       // URL을 자동으로 링크로 변환
    typographer: true    // 타이포그래피 개선
});

// heading 커스텀 렌더러 - 상하 여백 축소
for (let i = 1; i <= 6; i++) {
    md.renderer.rules.heading_open = function (tokens, idx, options, env, renderer) {
        const level = tokens[idx].markup.length;
        if (level === 1) return `<h${level} class="response-header-1">`;
        return `<h${level} class="response-header-2">`;
    };
}

// paragraph 커스텀 렌더러 - 상하 여백 축소
md.renderer.rules.paragraph_open = function (tokens, idx, options, env, renderer) {
    return `<p class="response-paragraph">`;
};


// 코드 블록 커스텀 렌더러
md.renderer.rules.code_block = function (tokens, idx) {
    const token = tokens[idx];
    const content = token.content;
    return `<pre class="response-code-block"><code>${md.utils.escapeHtml(content)}</code></pre>`;
};

// 인라인 코드 커스텀 렌더러
md.renderer.rules.code_inline = function (tokens, idx) {
    const token = tokens[idx];
    const content = token.content;
    return `<code class="response-code-line">${md.utils.escapeHtml(content)}</code>`;
};

// fenced 코드 블록 커스텀 렌더러 (```로 감싼 코드)
md.renderer.rules.fence = function (tokens, idx, options, env, renderer) {
    const token = tokens[idx];
    const info = token.info ? md.utils.escapeHtml(token.info.trim()) : '';
    const langClass = info ? ` class="language-${info.split(/\s+/g)[0]}"` : '';
    const content = token.content;

    return `<pre class="response-code-fence"><code${langClass}>${md.utils.escapeHtml(content)}</code></pre>`;
};