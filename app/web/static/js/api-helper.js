// API 호출 헬퍼 함수들

/**
 * localStorage에서 access_token을 가져오는 함수
 */
function getAccessToken() {
    return localStorage.getItem('access_token');
}

/**
 * access_token을 localStorage에서 제거하는 함수
 */
function removeAccessToken() {
    localStorage.removeItem('access_token');
}

/**
 * Authorization 헤더가 자동으로 포함된 fetch 함수
 */
async function fetchWithAuth(url, options = {}) {
    const token = getAccessToken();

    // 기본 헤더 설정
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // access_token이 있으면 Authorization 헤더 추가
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // fetch 옵션 구성
    const fetchOptions = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, fetchOptions);

        // 401 에러 시 토큰이 만료된 것으로 판단하고 로그인 페이지로 리다이렉트
        if (response.status === 401) {
            removeAccessToken();
            window.location.href = '/login';
            return null;
        }

        return response;
    } catch (error) {
        console.error('API 호출 중 오류 발생:', error);
        throw error;
    }
}

/**
 * POST 요청을 위한 헬퍼 함수
 */
async function postWithAuth(url, data) {
    return fetchWithAuth(url, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * GET 요청을 위한 헬퍼 함수
 */
async function getWithAuth(url) {
    return fetchWithAuth(url, {
        method: 'GET'
    });
}

/**
 * DELETE 요청을 위한 헬퍼 함수
 */
async function deleteWithAuth(url) {
    return fetchWithAuth(url, {
        method: 'DELETE'
    });
}

/**
 * 로그아웃 함수
 */
async function logout() {
    try {
        // 서버에 로그아웃 요청 (토큰 무효화)
        await postWithAuth('/logout', {});
    } catch (error) {
        console.error('로그아웃 요청 중 오류:', error);
    } finally {
        // 클라이언트에서 토큰 제거
        removeAccessToken();
        // 로그인 페이지로 리다이렉트
        window.location.href = '/login';
    }
}

// 전역에서 사용할 수 있도록 window 객체에 등록
if (typeof window !== 'undefined') {
    window.apiHelper = {
        getAccessToken,
        removeAccessToken,
        fetchWithAuth,
        postWithAuth,
        getWithAuth,
        deleteWithAuth,
        logout
    };
}