/**
 * API 요청/응답 일반화 유틸리티
 * 모든 API 요청을 처리하는 공통 함수들을 제공합니다.
 */

/**
 * localStorage에서 access_token을 가져오는 함수
 */
function getAccessToken() {
    return localStorage.getItem('access_token');
}

/**
 * access_token을 localStorage에 저장하는 함수
 */
function setAccessToken(token) {
    localStorage.setItem('access_token', token);
}

/**
 * access_token을 localStorage에서 제거하는 함수
 */
function removeAccessToken() {
    localStorage.removeItem('access_token');
}

/**
 * API 요청 기본 함수
 * @param {string} url - 요청할 URL
 * @param {Object} options - fetch options
 * @param {boolean} requireAuth - 인증이 필요한 요청인지 여부
 * @returns {Promise<Response>}
 */
async function apiRequest(url, options = {}, requireAuth = true) {
    // 기본 헤더 설정
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // 인증이 필요한 경우 access_token 추가
    if (requireAuth) {
        const token = getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }

    // fetch 옵션 구성
    const fetchOptions = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, fetchOptions);

        // 401 에러 시 토큰이 만료된 것으로 판단하고 로그인 페이지로 리다이렉트
        if (response.status === 401 && requireAuth) {
            removeAccessToken();
            window.location.href = '/login';
            return null;
        }

        return response;
    } catch (error) {
        console.error('API 요청 중 오류 발생:', error);
        throw error;
    }
}

/**
 * GET 요청
 * @param {string} url - 요청할 URL
 * @param {boolean} requireAuth - 인증이 필요한 요청인지 여부
 * @returns {Promise<Response>}
 */
async function apiGet(url, requireAuth = true) {
    return apiRequest(url, { method: 'GET' }, requireAuth);
}

/**
 * POST 요청
 * @param {string} url - 요청할 URL
 * @param {Object} data - 전송할 데이터
 * @param {boolean} requireAuth - 인증이 필요한 요청인지 여부
 * @returns {Promise<Response>}
 */
async function apiPost(url, data, requireAuth = true) {
    return apiRequest(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }, requireAuth);
}

/**
 * PUT 요청
 * @param {string} url - 요청할 URL
 * @param {Object} data - 전송할 데이터
 * @param {boolean} requireAuth - 인증이 필요한 요청인지 여부
 * @returns {Promise<Response>}
 */
async function apiPut(url, data, requireAuth = true) {
    return apiRequest(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    }, requireAuth);
}

/**
 * DELETE 요청
 * @param {string} url - 요청할 URL
 * @param {boolean} requireAuth - 인증이 필요한 요청인지 여부
 * @returns {Promise<Response>}
 */
async function apiDelete(url, requireAuth = true) {
    return apiRequest(url, { method: 'DELETE' }, requireAuth);
}

/**
 * 로그아웃 함수
 */
async function logout() {
    try {
        // 서버에 로그아웃 요청 (토큰 무효화)
        await apiPost('/api/v1/auth/logout', {});
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
    window.api = {
        getAccessToken,
        setAccessToken,
        removeAccessToken,
        request: apiRequest,
        get: apiGet,
        post: apiPost,
        put: apiPut,
        delete: apiDelete,
        logout
    };
}
