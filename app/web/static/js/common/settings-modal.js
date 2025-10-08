/**
 * Settings Modal Functionality
 * 채팅 설정 모달을 관리하는 JavaScript 파일
 */

class SettingsModal {
    constructor() {
        this.modal = null;
        this.modalThemeToggle = null;
        this.themeLabel = null;
        this.assistantSelect = null;
        this.planModeRadio = null;
        this.devModeRadio = null;

        // 현재 설정값들
        this.currentSettings = {
            theme: 'dark',
            assistant: 'claude',
            chatMode: 'plan'
        };

        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        // DOM 요소들 가져오기
        this.modal = document.getElementById('settingsModal');
        this.modalThemeToggle = document.getElementById('modalThemeToggle');
        this.themeLabel = document.getElementById('themeLabel');
        this.assistantSelect = document.getElementById('assistantSelect');
        this.planModeRadio = document.getElementById('planMode');
        this.devModeRadio = document.getElementById('devMode');

        if (!this.modal) {
            console.warn('Settings modal not found');
            return;
        }

        // 이벤트 리스너 등록
        this.setupEventListeners();

        // 초기 설정값 로드
        this.loadCurrentSettings();

        // UI 초기화
        this.updateUI();
    }

    setupEventListeners() {
        // 설정 버튼 클릭 이벤트
        const settingsBtn = document.getElementById('settingsBtn');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => this.openModal());
        }

        // 모달 닫기 이벤트들
        const closeBtn = document.getElementById('closeSettingsModal');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal());
        }

        const cancelBtn = document.getElementById('cancelSettings');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => this.closeModal());
        }

        // 오버레이 클릭으로 닫기
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // ESC 키로 닫기
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.closeModal();
            }
        });

        // 저장 버튼
        const saveBtn = document.getElementById('saveSettings');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveSettings());
        }

        // 로그아웃 버튼
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.handleLogout());
        }

        // 모달 내부 테마 토글
        if (this.modalThemeToggle) {
            this.modalThemeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // 테마 변경 감지 (외부에서 변경된 경우)
        document.addEventListener('themeChanged', (e) => {
            this.currentSettings.theme = e.detail.theme;
            this.updateThemeUI();
        });
    }

    loadCurrentSettings() {
        // localStorage에서 설정 로드
        this.currentSettings.theme = localStorage.getItem('theme') || 'dark';
        this.currentSettings.assistant = localStorage.getItem('assistant') || 'claude';
        this.currentSettings.chatMode = localStorage.getItem('chatMode') || 'plan';

        // 시스템 테마 선호도 확인 (테마 설정이 없을 때)
        if (!localStorage.getItem('theme')) {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.currentSettings.theme = prefersDark ? 'dark' : 'white';
        }
    }

    updateUI() {
        this.updateThemeUI();
        this.updateAssistantUI();
        this.updateChatModeUI();
    }

    updateThemeUI() {
        if (this.themeLabel) {
            this.themeLabel.textContent = this.currentSettings.theme === 'dark' ? '다크 모드' : '화이트 모드';
        }
    }

    updateAssistantUI() {
        if (this.assistantSelect) {
            this.assistantSelect.value = this.currentSettings.assistant;
        }
    }

    updateChatModeUI() {
        if (this.planModeRadio && this.devModeRadio) {
            if (this.currentSettings.chatMode === 'plan') {
                this.planModeRadio.checked = true;
            } else {
                this.devModeRadio.checked = true;
            }
        }
    }

    openModal() {
        // 현재 설정값들을 다시 로드
        this.loadCurrentSettings();
        this.updateUI();

        // 모달 표시
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // 배경 스크롤 방지

        // 첫 번째 포커스 가능한 요소에 포커스
        const firstFocusable = this.modal.querySelector('button, select, input');
        if (firstFocusable) {
            firstFocusable.focus();
        }
    }

    closeModal() {
        this.modal.classList.remove('active');
        document.body.style.overflow = ''; // 배경 스크롤 복원
    }

    toggleTheme() {
        const newTheme = this.currentSettings.theme === 'dark' ? 'white' : 'dark';
        this.currentSettings.theme = newTheme;

        // 전역 테마 토글 함수 호출
        if (window.setTheme) {
            window.setTheme(newTheme);
        } else if (window.themeToggle) {
            // theme-toggle.js의 인스턴스 직접 호출
            window.themeToggle.setThemeProgrammatically(newTheme);
        }

        this.updateThemeUI();
    }

    saveSettings() {
        // 현재 UI에서 설정값들 읽어오기
        if (this.assistantSelect) {
            this.currentSettings.assistant = this.assistantSelect.value;
        }

        if (this.planModeRadio && this.devModeRadio) {
            this.currentSettings.chatMode = this.planModeRadio.checked ? 'plan' : 'dev';
        }

        // localStorage에 저장
        localStorage.setItem('theme', this.currentSettings.theme);
        localStorage.setItem('assistant', this.currentSettings.assistant);
        localStorage.setItem('chatMode', this.currentSettings.chatMode);

        // 설정 변경 이벤트 발생
        this.dispatchSettingsChangeEvent();

        // 모달 닫기
        this.closeModal();

        // 성공 메시지 표시 (선택사항)
        this.showSuccessMessage();
    }

    dispatchSettingsChangeEvent() {
        const event = new CustomEvent('settingsChanged', {
            detail: { ...this.currentSettings }
        });
        document.dispatchEvent(event);
    }

    showSuccessMessage() {
        // 간단한 토스트 메시지 표시
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: #4ade80;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            z-index: 10000;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        `;
        toast.textContent = '설정이 저장되었습니다.';

        document.body.appendChild(toast);

        // 애니메이션
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });

        // 3초 후 제거
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // 외부에서 설정 가져오기
    getSettings() {
        return { ...this.currentSettings };
    }

    // 외부에서 설정 변경
    updateSetting(key, value) {
        if (this.currentSettings.hasOwnProperty(key)) {
            this.currentSettings[key] = value;
            localStorage.setItem(key, value);
            this.updateUI();
            this.dispatchSettingsChangeEvent();
        }
    }

    // 로그아웃 처리
    async handleLogout() {
        // 확인 대화상자 표시
        if (!confirm('정말 로그아웃하시겠습니까?')) {
            return;
        }

        try {
            const response = await fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                // 모달 닫기
                this.closeModal();
                // 로그인 페이지로 리다이렉트
                window.location.href = '/login';
            } else {
                alert('로그아웃 중 오류가 발생했습니다.');
            }
        } catch (error) {
            console.error('Logout error:', error);
            alert('서버에 연결할 수 없습니다.');
        }
    }
}

// 전역 인스턴스 생성
window.settingsModal = new SettingsModal();

// 다른 스크립트에서 사용할 수 있도록 유틸리티 함수들 제공
window.getSettings = () => window.settingsModal.getSettings();
window.updateSetting = (key, value) => window.settingsModal.updateSetting(key, value);

// 설정 변경 이벤트 리스너 예제
// document.addEventListener('settingsChanged', (e) => {
//     console.log('Settings changed:', e.detail);
//     const { theme, assistant, chatMode } = e.detail;
//     // 설정 변경에 따른 추가 로직 구현
// });