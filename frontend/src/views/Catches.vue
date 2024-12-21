<template>
    <div class="min-h-screen bg-gray-50">
        <!-- 상단 검색/필터 영역 -->
        <div class="sticky top-0 bg-white shadow-sm z-10 px-4 py-3">
            <div class="max-w-4xl mx-auto">
                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="relative flex-grow">
                        <input 
                            type="text" 
                            v-model="searchQuery" 
                            placeholder="물고기 검색..." 
                            class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                        />
                        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    </div>
                    <div class="flex gap-2">
                        <select 
                            v-model="sortOption" 
                            class="px-4 py-2 rounded-lg border border-gray-200 bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors cursor-pointer"
                        >
                            <option value="latest">최신순</option>
                            <option value="oldest">오래된순</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <!-- 메인 콘텐츠 영역 -->
        <main class="max-w-4xl mx-auto px-4 py-6">
            <!-- 로딩 상태 -->
            <div v-if="loading" class="flex justify-center items-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>

            <!-- 데이터 없음 상태 -->
            <div v-else-if="!filteredCatches.length" class="flex flex-col items-center justify-center py-12 text-gray-500">
                <Fish class="w-16 h-16 mb-4 text-gray-300" />
                <p class="text-lg">아직 잡은 물고기가 없습니다.</p>
                <p class="text-sm mt-2">물고기를 잡아서 추억을 기록해보세요!</p>
            </div>

            <!-- 물고기 목록 -->
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div v-for="catchItem in filteredCatches" 
                    :key="catchItem.id"
                    class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden"
                >
                    <!-- 이미지 섹션 -->
                    <div class="relative aspect-[4/3] overflow-hidden bg-gray-100">
                        <img 
                            :src="`${BACKEND_BASE_URL}/uploads/${catchItem.imageUrl}`" 
                            alt="Catch Image"
                            class="w-full h-full object-cover cursor-pointer hover:scale-105 transition-transform duration-300"
                            @click="openImagePopup(catchItem.imageUrl)"
                        />
                    </div>

                    <!-- 정보 섹션 -->
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h3 class="text-lg font-semibold text-gray-800">
                                {{ catchItem.detections[0].label }}
                            </h3>
                            <div class="flex gap-2">
                                <button 
                                    @click="openEditModal(catchItem)"
                                    class="p-1.5 rounded-full hover:bg-gray-100 transition-colors"
                                >
                                    <Edit class="w-4 h-4 text-blue-500" />
                                </button>
                                <button 
                                    @click="confirmDelete(catchItem.id)"
                                    class="p-1.5 rounded-full hover:bg-gray-100 transition-colors"
                                >
                                    <Trash class="w-4 h-4 text-red-500" />
                                </button>
                            </div>
                        </div>

                        <div class="space-y-1.5">
                            <div class="flex items-center text-sm text-gray-600">
                                <Calendar class="w-4 h-4 mr-2" />
                                {{ catchItem.catch_date }}
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <Target class="w-4 h-4 mr-2" />
                                신뢰도: {{ (catchItem.detections[0].confidence * 100).toFixed(2) }}%
                            </div>
                            <div v-if="catchItem.weight_kg || catchItem.length_cm" class="flex items-center text-sm text-gray-600">
                                <Scale class="w-4 h-4 mr-2" />
                                <span v-if="catchItem.weight_kg">{{ catchItem.weight_kg }}kg</span>
                                <span v-if="catchItem.weight_kg && catchItem.length_cm" class="mx-2">|</span>
                                <span v-if="catchItem.length_cm">{{ catchItem.length_cm }}cm</span>
                            </div>
                            <div v-if="catchItem.memo" class="flex items-start text-sm text-gray-600">
                                <FileText class="w-4 h-4 mr-2 mt-0.5" />
                                <p class="line-clamp-2">{{ catchItem.memo }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 더 보기 트리거 -->
            <div ref="loadMoreTrigger" class="h-10 mt-6"></div>
        </main>

        <!-- 모달 컴포넌트들 -->
        <EditFishModal
            v-if="showEditModal"
            :isVisible="showEditModal"
            :catchData="selectedCatch"
            @close="showEditModal = false"
            @save="handleFishDataSave"
        />

        <!-- 이미지 팝업 -->
        <div v-if="isImagePopupVisible"
            class="fixed inset-0 bg-black bg-opacity-90 flex justify-center items-center z-50"
            @click="isImagePopupVisible = false"
        >
            <div class="relative max-w-4xl w-full mx-4" @click.stop>
                <img 
                    :src="popupImageUrl" 
                    alt="Popup Image"
                    class="w-full h-auto rounded-lg shadow-xl"
                />
                <button 
                    @click="isImagePopupVisible = false"
                    class="absolute top-4 right-4 p-2 bg-white rounded-full hover:bg-gray-100 transition-colors"
                >
                    <X class="w-5 h-5" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { Edit, Trash, Search, Fish, Calendar, Target, Scale, FileText, X } from 'lucide-vue-next';
import EditFishModal from '../components/EditFishModal.vue';

const store = useStore();
const catches = computed(() => store.getters.catches);
const loading = ref(true);
const showEditModal = ref(false);
const selectedCatch = ref(null);
const displayedCatches = ref([]);
const itemsToLoad = 8;
const loadMoreTrigger = ref(null);
const isImagePopupVisible = ref(false);
const popupImageUrl = ref('');
const searchQuery = ref('');
const sortOption = ref('latest');

const filteredCatches = computed(() => {
    const catchesFiltered = displayedCatches.value.filter(catchItem => {
        return catchItem.detections[0].label.toLowerCase().includes(searchQuery.value.toLowerCase());
    });

    if (sortOption.value === 'latest') {
        return catchesFiltered.sort((a, b) => b.id - a.id);
    } else {
        return catchesFiltered.sort((a, b) => a.id - b.id);
    }
});

// Define backend base URL
const BACKEND_BASE_URL = 'http://localhost:5000';

onMounted(async () => {
    if (store.getters.isAuthenticated) {
        try {
            await store.dispatch('fetchCatches');
            const sortedCatches = store.getters.catches
                .slice()
                .sort((a, b) => new Date(b.catch_date) - new Date(a.catch_date));
            displayedCatches.value = sortedCatches;
        } catch (error) {
            console.error('Error fetching catches:', error);
        } finally {
            loading.value = false;
        }
    } else {
        loading.value = false;
    }

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !loading.value) {
            loadMoreCatches();
        }
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 1.0
    });

    if (loadMoreTrigger.value) {
        observer.observe(loadMoreTrigger.value);
    }
});

watch(() => catches.value, () => {
    updateDisplayedCatches();
}, { deep: true });

function updateDisplayedCatches() {
    const sortedCatches = [...catches.value].sort((a, b) => 
        new Date(b.catch_date) - new Date(a.catch_date)
    );
    displayedCatches.value = sortedCatches;
}

function loadMoreCatches() {
    loading.value = true;
    setTimeout(() => {
        const currentLength = displayedCatches.value.length;
        const sortedCatches = catches.value.slice().sort((a, b) => b.id - a.id);
        const moreCatches = sortedCatches.slice(currentLength, currentLength + itemsToLoad);
        displayedCatches.value = [...displayedCatches.value, ...moreCatches];
        loading.value = false;
    }, 1000);
}

function openEditModal(catchItem) {
    console.log("Opening edit modal for:", catchItem);
    if (!catchItem.id) {
        console.error("Cannot open edit popup: 'id' is undefined.");
        alert("수정할 수 없는 항목입니다: 식별자가 없습니다.");
        return;
    }
    selectedCatch.value = { ...catchItem };
    selectedCatch.value.detections[0].confidence = parseFloat(selectedCatch.value.detections[0].confidence);
    showEditModal.value = true;
}

const handleFishDataSave = async (updatedData) => {
    try {
        const response = await store.dispatch('updateCatch', updatedData);
        showEditModal.value = false;
        const index = displayedCatches.value.findIndex(c => c.id === response.id);
        if (index !== -1) {
            displayedCatches.value[index] = response;
        }
        displayedCatches.value = [...displayedCatches.value];
    } catch (error) {
        console.error('Error saving fish data:', error);
        alert('물고기 정보 저장에 실패했습니다.');
    }
};

function openImagePopup(imageUrl) {
    popupImageUrl.value = `${BACKEND_BASE_URL}/uploads/${imageUrl}`;
    isImagePopupVisible.value = true;
}

function confirmDelete(catchId) {
    if (confirm('정말로 이 항목을 삭제하시겠습니까?')) {
        deleteCatch(catchId);
    }
}

function deleteCatch(catchId) {
    store.dispatch('deleteCatch', catchId).then(() => {
        updateDisplayedCatches();
    }).catch((error) => {
        console.error("Delete error:", error.response ? error.response.data : error.message);
        alert('데이터 삭제에 실패했습니다.');
    });
}
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
