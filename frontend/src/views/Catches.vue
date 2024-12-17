<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-4xl bg-white shadow-lg">
            <main class="p-4">
                <div v-if="displayedCatches.length > 0" class="grid grid-cols-2 gap-4">
                    <div v-for="(catchItem, index) in displayedCatches" :key="index"
                        class="bg-gray-50 p-4 rounded-lg shadow-sm">
                        <img :src="catchItem.imageUrl" alt="Catch Image"
                            class="w-full h-32 object-cover rounded-lg mb-2" />
                        <p class="text-gray-800 text-sm text-center flex justify-center items-center">
                            {{ catchItem.detections[0].label }}
                            <span v-if="catchItem.detections[0].label === '알 수 없음'" class="ml-2 cursor-pointer"
                                @click="openEditPopup(catchItem)">
                                <!-- Edit Icon -->
                                <Edit class="h-4 w-4 text-blue-500" />
                            </span>
                        </p>
                        <p class="text-gray-600 text-xs text-center">{{ catchItem.catch_date }}</p>
                        <p class="text-gray-600 text-xs text-center">신뢰도: {{
                            catchItem.detections[0].confidence.toFixed(2) }}</p>
                    </div>
                </div>
                <div v-else-if="!loading" class="text-gray-500 text-center">아직 잡은 물고기가 없습니다.</div>
                <div v-if="loading" class="text-center text-gray-500 mt-4">Loading...</div>
                <div ref="loadMoreTrigger" class="text-center text-gray-500 mt-4"></div>
                <div v-if="isEditPopupVisible"
                    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div class="bg-white p-4 rounded-lg">
                        <h2 class="text-lg mb-2 text-center">데이터 수정</h2>
                        <div class="mb-2">
                            <label class="block text-sm">라벨</label>
                            <input v-model="selectedCatch.detections[0].label" class="border p-2 w-full" />
                        </div>
                        <div class="mb-2">
                            <label class="block text-sm">날짜</label>
                            <input type="date" v-model="selectedCatch.catch_date" class="border p-2 w-full" />
                        </div>
                        <div class="mb-2">
                            <label class="block text-sm">신뢰도</label>
                            <input type="number" step="0.01" v-model.number="selectedCatch.detections[0].confidence"
                                class="border p-2 w-full" />
                        </div>
                        <button @click="saveEdit" class="mt-2 bg-blue-500 text-white px-4 py-2 rounded">저장</button>
                        <button @click="isEditPopupVisible = false"
                            class="mt-2 bg-gray-300 text-black px-4 py-2 rounded">취소</button>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { Edit } from 'lucide-vue-next';

const store = useStore();
const catches = computed(() => store.getters.catches);
const loading = ref(false);
const isEditPopupVisible = ref(false);
const selectedCatch = ref(null);
const displayedCatches = ref([]);
const itemsToLoad = 6;
const loadMoreTrigger = ref(null);

onMounted(() => {
    if (store.getters.isAuthenticated) {
        store.dispatch('fetchCatches').then(() => {
            displayedCatches.value = catches.value.slice(0, itemsToLoad);
        });
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

function loadMoreCatches() {
    loading.value = true;
    setTimeout(() => {
        const currentLength = displayedCatches.value.length;
        const moreCatches = catches.value.slice(currentLength, currentLength + itemsToLoad);
        displayedCatches.value = [...displayedCatches.value, ...moreCatches];
        loading.value = false;
    }, 1000); // Simulate loading delay
}

function openEditPopup(catchItem) {
    selectedCatch.value = { ...catchItem };
    isEditPopupVisible.value = true;
}

function saveEdit() {
    store.dispatch('updateCatch', selectedCatch.value).then(() => {
        // Update displayedCatches after successful update
        const index = displayedCatches.value.findIndex(catchItem => catchItem.id === selectedCatch.value.id);
        if (index !== -1) {
            displayedCatches.value[index] = { ...selectedCatch.value };
        }
        isEditPopupVisible.value = false;
    }).catch(() => {
        // Handle error (optional)
        alert('데이터 업데이트에 실패했습니다.');
    });
}
</script>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

/* Optional: style the edit icon if needed */
.cursor-pointer:hover svg {
    stroke: #3b82f6;
}
</style>
