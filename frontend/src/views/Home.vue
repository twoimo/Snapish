<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-4xl bg-white shadow-lg overflow-hidden rounded-lg">
            <main class="pb-20 px-4">
                <!-- 오늘의 물때 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/map-location-service"
                            class="flex justify-between items-center p-2 w-full hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium mr-2">오늘의 물때</h2>
                            <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                        </router-link>
                    </div>
                    <MulddaeWidget></MulddaeWidget>
                </section>

                <!-- 내가 잡은 물고기 섹션 -->
                <section v-if="isAuthenticated" class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/catches"
                            class="flex justify-between items-center p-2 w-full hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium mr-2">내가 잡은 물고기</h2>
                            <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                        </router-link>
                    </div>
                    <div v-if="isLoadingCatches" class="text-center text-gray-500">
                        Loading...
                    </div>
                    <div v-else-if="displayedCatches.length > 0" class="overflow-x-auto touch-pan-x"
                        @scroll="loadMoreCatches">
                        <div class="flex space-x-4">
                            <div v-for="catchItem in displayedCatches" :key="catchItem.id"
                                class="bg-gray-50 p-4 rounded-lg shadow-sm flex-shrink-0 w-80 h-64">
                                <img :src="`${BACKEND_BASE_URL}/uploads/${catchItem.imageUrl}`" alt="Catch Image"
                                    class="w-full h-48 object-cover rounded-lg mb-2 cursor-pointer"
                                    @click="openImagePopup(catchItem.imageUrl)" />
                                <p class="text-gray-800 text-sm text-center">{{ catchItem.detections[0].label }}
                                </p>
                                <p class="text-gray-600 text-xs text-center mb-2">신뢰도: {{
                                    catchItem.detections[0].confidence.toFixed(2)
                                }}%</p>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-gray-500 flex flex-col items-center p-2">아직 잡은 물고기가 없습니다.</div>
                </section>

                <!-- 오늘의 핫이슈 섹션 -->
                <section>
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/community"
                            class="flex justify-between items-center p-2 w-full hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium">오늘의 핫이슈</h2>
                            <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                        </router-link>
                    </div>
                    <div class="space-y-3">
                        <article v-for="i in 5" :key="i"
                            class="bg-gray-50 rounded-lg p-4 shadow-sm hover:bg-gray-100 transition">
                            <div class="flex gap-3">
                                <div
                                    class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center flex-shrink-0">
                                    <ImageIcon class="w-8 h-8 text-gray-400" />
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-medium mb-1">게시물 제목</h3>
                                    <p class="text-sm text-gray-600 mb-2">게시물 내용 미리보기입니다. 여기에 간단한 설명이 들어갑니다.</p>
                                    <div class="flex items-center text-sm text-gray-500">
                                        <ClockIcon class="w-4 h-4 mr-1" />
                                        <span>오늘 • 23분 전</span>
                                    </div>
                                </div>
                                <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                            </div>
                        </article>
                    </div>
                </section>
            </main>
        </div>
    </div>
    <div v-if="isImagePopupVisible" class="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-30"
        @click="isImagePopupVisible = false">
        <div class="relative flex justify-center items-center" @click.stop>
            <img :src="popupImageUrl" alt="Popup Image"
                class="max-w-full max-h-full object-contain rounded-lg border border-gray-200 shadow-lg" />
            <button @click="isImagePopupVisible = false"
                class="absolute top-2 right-2 bg-white text-black rounded-full p-1 hover:bg-gray-200 transition-colors duration-300">
                &times;
            </button>
        </div>
    </div>
    <input type="file" @change="handleImageUpload" />
    <div v-if="isAuthenticated">
        <img :src="avatarUrl" alt="User Avatar" class="avatar" />
    </div>
    <div v-else>
        <img src="/default-avatar.webp" alt="Default Avatar" class="avatar" />
    </div>
</template>

<script setup>
import {
    ChevronRightIcon,
    ImageIcon,
    ClockIcon,
} from 'lucide-vue-next'
import { onMounted, computed, ref } from "vue";
import { useStore } from "vuex";
import MulddaeWidget from '../components/MulddaeWidget.vue';
import axios from 'axios'; // Import axios
import { useRouter } from 'vue-router'; // Import useRouter

// Vuex 스토어 사용
const store = useStore();
const router = useRouter(); // Initialize router

// Define backend base URL
const BACKEND_BASE_URL = 'http://localhost:5000';

const isLoadingCatches = ref(false); // Add loading state

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
    if (!store.state.mulddae) {
        store.dispatch("fetchMulddae");
    }
    if (isAuthenticated.value) {
        isLoadingCatches.value = true; // Start loading
        store.dispatch("fetchCatches").then(() => {
            const sortedCatches = catches.value.slice().reverse();
            displayedCatches.value = sortedCatches.slice(0, itemsToLoad);
            isLoadingCatches.value = false; // End loading
        });
    }
});

// Vuex 스토어에서 잡은 물고기 데이터 가져오기
const catches = computed(() => store.getters.catches);
const isAuthenticated = computed(() => store.getters.isAuthenticated);
const avatarUrl = computed(() =>
    store.getters.user.avatar ? `http://localhost:5000${store.getters.user.avatar}` : '/default-avatar.webp'
);

// 이미지 팝업 관련 상태
const isImagePopupVisible = ref(false);
const popupImageUrl = ref('');

// 잡은 물고기 섹션 관련 상태
const displayedCatches = ref([]);
const itemsToLoad = 2;

function openImagePopup(imageUrl) {
    popupImageUrl.value = `${BACKEND_BASE_URL}/uploads/${imageUrl}`; // Updated to include BACKEND_BASE_URL
    isImagePopupVisible.value = true;
}

function loadMoreCatches(event) {
    const element = event.target;
    if (element.scrollWidth - element.scrollLeft === element.clientWidth) {
        const currentLength = displayedCatches.value.length;
        const sortedCatches = catches.value.slice().reverse();
        const moreCatches = sortedCatches.slice(currentLength, currentLength + itemsToLoad);
        displayedCatches.value = [...displayedCatches.value, ...moreCatches];
    }
}

const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
        if (store.state.isAuthenticated) {
            // Authenticated user: upload file to server
            const formData = new FormData();
            formData.append('image', file);
            try {
                const response = await axios.post('/backend/predict', formData, {
                    headers: {
                        'Authorization': `Bearer ${store.state.token}`,
                        'Content-Type': 'multipart/form-data',
                    },
                    withCredentials: true,
                });
                handlePredictResponse(response.data);
            } catch (error) {
                console.error('Error during Axios POST:', error);
                alert('이미지 업로드 중 오류가 발생했습니다.');
            }
        } else {
            // Unauthenticated user: handle base64 encoding
            const reader = new FileReader();
            reader.onload = async () => {
                const image_base64 = reader.result.split(',')[1]; // Remove data:image/*;base64,
                try {
                    const response = await axios.post('/backend/predict', {
                        image_base64,
                    });
                    handlePredictResponse(response.data);
                } catch (error) {
                    console.error('Error during Axios POST:', error);
                    alert('이미지 업로드 중 오류가 발생했습니다.');
                }
            };
            reader.readAsDataURL(file);
        }
    }
};

const handlePredictResponse = (data) => {
    // Handle the response from the backend
    const detections = data.detections;
    const imageUrl = data.imageUrl || null;
    const imageBase64 = data.image_base64 || null;

    if (detections && detections.length > 0) {
        if (store.state.isAuthenticated) {
            store.dispatch('fetchCatches');
            router.push({
                name: 'FishResultNormal',
                query: {
                    imageUrl,
                    imageBase64,
                    detections: encodeURIComponent(JSON.stringify(detections)),
                },
            });
        } else {
            router.push({
                name: 'FishResultNormal',
                query: {
                    imageBase64,
                    detections: encodeURIComponent(JSON.stringify(detections)),
                },
            });
        }
    } else {
        alert('알 수 없는 물고기입니다.');
    }
};
</script>

<style lang="css">
* {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

*::-webkit-scrollbar {
    display: none;
}

.touch-pan-x {
    -webkit-overflow-scrolling: touch;
    -webkit-overflow-scrolling: touch;
}

.scroll-smooth {
    scroll-behavior: smooth;
}

.hover\:bg-gray-50:hover {
    background-color: #f9fafb;
}

.hover\:bg-gray-100:hover {
    background-color: #f3f4f6;
}

.transition {
    transition: background-color 0.3s ease;
}

.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}
</style>
