const pylonForm = document.querySelector("form[name=create-pylon]")
const pylonButton = pylonForm.querySelector('button[name=create-pylon]');
const pylonButtonText = pylonButton.querySelector("span");
const pylonLoadingSpinner = pylonButton.querySelector(".loading-spinner");

const editPylonForm = document.querySelector("form[name=edit-pylon]")
const editPylonButton = editPylonForm.querySelector('button[name=edit-pylon]');
const editPylonButtonText = editPylonButton.querySelector("span");
const editPylonLoadingSpinner = editPylonButton.querySelector(".loading-spinner");

window.pylonCreateModal = new Modal(
    document.querySelector("#create_pylon"),
    document.querySelector("#create_pylon_modal")
);

window.pylonEditModal = new Modal(
    null,
    document.querySelector("#edit_pylon_modal")
);

document.addEventListener("DOMContentLoaded", async function() {
    await getPylons();
})

pylonForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    await createPylon();
})

editPylonForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    await updatePylon();
})

// 새로고침 버튼
document.getElementById("refresh_nexus").addEventListener("click", function() {
    location.reload();
})

// 검색 기능
document.getElementById("search_pylon").addEventListener("input", function(e) {
    searchPylons(e.target.value);
})

async function getPylons() {
    try {
        const response = await window.api.get('/api/v1/nexus/pylons');
        const body = await response.body;

        if (response.status) {
            const pylons = await body['pylons'];

            const pylonContainer = document.getElementById('pylon_gallery');
            const pylonEmpty = document.getElementById('pylon_empty');
            const totalPylon = document.getElementById('total_pylon');

            if (pylons && pylons.length > 0) {
                // 빈 상태 숨기기
                pylonEmpty.style.display = 'none';

                // 파일런 개수 업데이트
                totalPylon.textContent = `total - ${pylons.length} Pylon`;

                // 파일런 카드 생성
                pylons.forEach(pylon => {
                    const pylonCard = createPylonCard(pylon);
                    pylonContainer.insertBefore(pylonCard, pylonEmpty);
                });
            } else {
                // 파일런이 없으면 빈 상태 표시
                pylonEmpty.style.display = 'block';
                totalPylon.textContent = 'total - 0 Pylon';
            }
        } else {
            alert(body.detail || '파일런 조회에 실패했습니다.');
        }
    } catch (error) {
        alert(error.detail || '파일런을 조회할 수 없습니다. 잠시 후 다시 시도해주세요.');
        location.href = "/login";
    }
}

function createPylonCard(pylon) {
    const pylonGroup = document.createElement('div');
    pylonGroup.className = 'pylon-group';
    pylonGroup.setAttribute('data-space-id', pylon.id);
    pylonGroup.onclick = () => joinPylon(pylon.id);

    // 타입에 따른 클래스 설정
    const typeClass = pylon.goal.toLowerCase();
    const typeText = pylon.goal === 'PLAN' ? '작업' : '일반';

    // 날짜 포맷팅
    const createdDate = new Date(pylon.created_at).toISOString().split('T')[0];

    pylonGroup.innerHTML = `
        <div class="pylon-cover">
            <img src="${pylon.image_url || getRandomPylonImage()}" alt="${pylon.title}">
            <div class="pylon-overlay">
                <div class="pylon-actions">
                    <button class="pylon-action-btn edit-btn" onclick="event.stopPropagation(); openEditModal(${pylon.id})" title="수정">
                        <i class="fa fa-cog"></i>
                    </button>
                    <button class="pylon-action-btn delete-btn" onclick="event.stopPropagation(); deletePylon(${pylon.id})" title="삭제">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>

        <div class="pylon-content">
            <div class="pylon-header">
                <h3 class="pylon-title">${pylon.title}</h3>
                <span class="pylon-type ${typeClass}">${typeText}</span>
            </div>
            <p class="pylon-description">${pylon.description}</p>
            <div class="pylon-stats">
                <div class="stat-item">
                    <i class="fa fa-user"></i>
                    <span>유저 ${pylon.user_count}명</span>
                </div>
                <div class="stat-item">
                    <i class="fa fa-layer-group"></i>
                    <span>에이전트 ${pylon.agent_count}명</span>
                </div>
                <div class="stat-item">
                    <i class="fa fa-clock"></i>
                    <span>${createdDate}</span>
                </div>
            </div>
        </div>
    `;

    return pylonGroup;
}

function joinPylon(pylonId) {
    window.location.href = `/pylon?id=${pylonId}`;
}

async function createPylon() {
    // 폼 데이터 수집
    const formData = new FormData(pylonForm);
    const data = Object.fromEntries(formData.entries());

    // 랜덤 이미지 URL 추가
    data.image_url = getRandomPylonImage();

    isCompleted(false);

    try {
        const response = await window.api.post('/api/v1/nexus/pylon', data);
        console.log("response: ", response);

        if (response && response.ok) {
            const result = await response.json();
            console.log('파일런 생성 완료:', result);

            // 모달 닫기
            window.pylonCreateModal.close();

            // 폼 초기화
            pylonForm.reset();

            // 페이지 새로고침
            location.reload();

            alert('파일런이 생성되었습니다.');
        } else if (response) {
            const error = await response.json();
            alert(error.detail || '파일런 생성에 실패했습니다.');
        }
    } catch (error) {
        console.error('Pylon creation error:', error);
        alert('서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
    } finally {
        isCompleted(true);
    }
}

function isCompleted(flag) {
    pylonButton.disabled = !flag;
    pylonButtonText.textContent = !flag ? "로그인 중..." : "로그인";
    pylonLoadingSpinner.style.display = !flag ? "inline-block" : "none";
}

function isEditCompleted(flag) {
    editPylonButton.disabled = !flag;
    editPylonButtonText.textContent = !flag ? "수정 중..." : "수정";
    editPylonLoadingSpinner.style.display = !flag ? "inline-block" : "none";
}

async function openEditModal(pylonId) {
    try {
        const response = await window.api.get(`/api/v1/nexus/pylon/${pylonId}`);

        if (response && response.ok) {
            const result = await response.json();
            const pylon = result.pylon;

            // 폼에 데이터 채우기
            document.getElementById('edit_pylon_id').value = pylon.id;
            document.getElementById('edit_pylon_title').value = pylon.title;
            document.getElementById('edit_pylon_description').value = pylon.description;
            document.getElementById('edit_pylon_type').value = pylon.goal;

            // 모달 열기
            window.pylonEditModal.open();
        } else if (response) {
            const error = await response.json();
            alert(error.detail || '파일런 정보를 불러올 수 없습니다.');
        }
    } catch (error) {
        console.error('Failed to load pylon:', error);
        alert('파일런 정보를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.');
    }
}

async function updatePylon() {
    const pylonId = document.getElementById('edit_pylon_id').value;
    const formData = new FormData(editPylonForm);
    const data = Object.fromEntries(formData.entries());

    isEditCompleted(false);

    try {
        const response = await window.api.put(`/api/v1/nexus/pylon/${pylonId}`, data);
        console.log("response: ", response);

        if (response && response.ok) {
            const result = await response.json();

            // 파일런 수정 성공
            console.log('Pylon updated successfully:', result);

            // 모달 닫기
            window.pylonEditModal.close();

            // 폼 초기화
            editPylonForm.reset();

            // 페이지 새로고침
            location.reload();

            alert('파일런이 수정되었습니다.');
        } else if (response) {
            const error = await response.json();
            alert(error.detail || '파일런 수정에 실패했습니다.');
        }
    } catch (error) {
        console.error('Pylon update error:', error);
        alert('서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
    } finally {
        isEditCompleted(true);
    }
}

async function deletePylon(pylonId) {
    if (!confirm('정말로 이 파일런을 삭제하시겠습니까?')) {
        return;
    }

    try {
        const response = await window.api.delete(`/api/v1/nexus/pylon/${pylonId}`);
        console.log("response: ", response);

        if (response && response.ok) {
            const result = await response.json();

            // 파일런 삭제 성공
            console.log('Pylon deleted successfully:', result);

            // 페이지 새로고침
            location.reload();

            alert('파일런이 삭제되었습니다.');
        } else if (response) {
            const error = await response.json();
            alert(error.detail || '파일런 삭제에 실패했습니다.');
        }
    } catch (error) {
        console.error('Pylon delete error:', error);
        alert('서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
    }
}

function searchPylons(keyword) {
    const pylonGroups = document.querySelectorAll('.pylon-group');
    const pylonEmpty = document.getElementById('pylon_empty');
    const searchKeyword = keyword.toLowerCase().trim();
    let visibleCount = 0;

    pylonGroups.forEach(group => {
        const title = group.querySelector('.pylon-title')?.textContent.toLowerCase() || '';
        const description = group.querySelector('.pylon-description')?.textContent.toLowerCase() || '';

        if (searchKeyword === '' || title.includes(searchKeyword) || description.includes(searchKeyword)) {
            group.style.display = '';
            visibleCount++;
        } else {
            group.style.display = 'none';
        }
    });

    // 검색 결과가 없을 때 빈 상태 표시
    if (visibleCount === 0 && searchKeyword !== '') {
        pylonEmpty.style.display = 'block';
        pylonEmpty.querySelector('h3').textContent = '검색 결과가 없습니다';
        pylonEmpty.querySelector('p').textContent = `"${keyword}"에 대한 검색 결과를 찾을 수 없습니다.`;
    } else if (visibleCount === 0 && searchKeyword === '') {
        pylonEmpty.style.display = 'block';
        pylonEmpty.querySelector('h3').textContent = '파일런이 없습니다';
        pylonEmpty.querySelector('p').textContent = '새로운 파일런을 만들어 에이전트와 대화를 시작해보세요.';
    } else {
        pylonEmpty.style.display = 'none';
    }

    // 카운트 업데이트
    const totalPylon = document.getElementById('total_pylon');
    if (searchKeyword === '') {
        totalPylon.textContent = `TOTAL - ${pylonGroups.length} Pylon`;
    } else {
        totalPylon.textContent = `검색 결과 - ${visibleCount} Pylon`;
    }
}