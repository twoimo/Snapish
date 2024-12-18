<template>
    <div class="min-h-screen bg-white flex flex-col items-center">
        <div class="bg-white w-full max-w-4xl rounded-lg mt-6">
            <!-- 프로필 헤더 -->
            <div v-if="user" class="p-6 flex flex-col items-center">
                <!-- Avatar 및 사용자 정보 -->
                <div class="flex flex-col items-center space-y-4">
                    <!-- 아바타 -->
                    <div class="w-32 h-32 rounded-full bg-gray-200 flex-shrink-0" :style="{
                        backgroundImage: `url(${user.avatar || '/default-avatar.webp'})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }"></div>

                    <!-- 사용자 정보 -->
                    <div class="text-center">
                        <h1 class="text-2xl font-semibold text-gray-800">
                            {{ user.full_name || user.username }}
                        </h1>
                        <p class="text-gray-600 mt-1">{{ user.tier || '낚시 초보자' }}</p>
                    </div>
                </div>

                <!-- 액션 버튼 -->
                <div class="flex items-center space-x-6 mt-4">
                    <!-- 프로필 수정 -->
                    <button @click="editProfile" class="text-blue-500 hover:text-blue-600 flex items-center space-x-1"
                        aria-label="Edit Profile">
                        <Edit class="h-6 w-6" />
                        <span class="text-sm font-medium">프로필 수정</span>
                    </button>

                    <!-- 로그아웃 -->
                    <button @click="logout" class="text-red-500 hover:text-red-600 flex items-center space-x-1"
                        aria-label="Logout">
                        <LogOut class="h-6 w-6" />
                        <span class="text-sm font-medium">로그아웃</span>
                    </button>
                </div>
            </div>

            <!-- 낚시 잡기, 팔로워, 팔로잉 -->
            <div v-if="stats" class="flex justify-around py-6 border-t border-gray-200">
                <div class="text-center cursor-pointer" @click="goToCatches">
                    <div class="text-2xl font-bold text-gray-800">{{ stats.catches || 0 }}</div>
                    <div class="text-gray-500 text-sm">Catches</div>
                </div>
                <div class="text-center">
                    <div class="text-2xl font-bold text-gray-800">{{ stats.followers || 0 }}</div>
                    <div class="text-gray-500 text-sm">Followers</div>
                </div>
                <div class="text-center">
                    <div class="text-2xl font-bold text-gray-800">{{ stats.following || 0 }}</div>
                    <div class="text-gray-500 text-sm">Following</div>
                </div>
            </div>

            <!-- 4x4 Grid of Icons and Names -->
            <div class="p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-6">전체 서비스</h2>
                <div class="grid grid-cols-4 gap-4">
                    <div v-for="service in services" :key="service.id" class="flex flex-col items-center">
                        <!-- Changed from service._id -->
                        <template v-if="service.name.includes('서비스')">
                            <Settings class="w-8 h-8 mb-2" />
                        </template>
                        <template v-else>
                            <img :src="service.icon" alt="Service Icon" class="w-16 h-16 mb-2" />
                        </template>
                        <span class="text-gray-700">{{ service.name }}</span>
                    </div>
                </div>
            </div>

            <!-- Display catches if authenticated -->
            <div v-if="isAuthenticated" class="p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-6">내 캐치</h2>
                <ul>
                    <li v-for="catchItem in catches" :key="catchItem.id" class="mb-4">
                        <img :src="catchItem.photoUrl ? `${BACKEND_BASE_URL}/uploads/${catchItem.photoUrl}` : '/placeholder.svg'"
                            alt="Catch Image" class="w-32 h-32 object-cover mb-2 cursor-pointer"
                            @click="openImagePopup(catchItem.photoUrl)" />
                        <p class="text-gray-700">물고기: {{ catchItem.detections[0].label }}</p>
                        <p class="text-gray-700">신뢰도: {{ catchItem.detections[0].confidence }}</p>
                    </li>
                </ul>
            </div>

            <!-- Image Popup -->
            <div v-if="isImagePopupVisible"
                class="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-30"
                @click="isImagePopupVisible = false">
                <div class="relative max-w-full max-h-full" @click.stop>
                    <img :src="popupImageUrl" alt="Popup Image"
                        class="w-full h-full object-contain rounded-lg border border-gray-200 shadow-lg" />
                    <button @click="isImagePopupVisible = false"
                        class="absolute top-2 right-2 bg-white text-black rounded-full p-1 hover:bg-gray-200 transition-colors duration-300">
                        &times;
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { Edit, LogOut, Settings } from 'lucide-vue-next';

const store = useStore();
const router = useRouter();

const user = computed(() => store.getters.user);
const stats = computed(() => {
    const originalStats = store.getters.stats;
    return {
        catches: store.getters.catches.length || 0, // Fetch catches from the store
        followers: originalStats?.followers || 0,
        following: originalStats?.following || 0,
    };
});
const services = computed(() => [
    { id: 1, icon: '/icons/service1.png', name: '서비스 1' },
    { id: 2, icon: '/icons/service2.png', name: '서비스 2' },
    { id: 3, icon: '/icons/service3.png', name: '서비스 3' },
    { id: 4, icon: '/icons/service4.png', name: '서비스 4' },
    { id: 5, icon: '/icons/service5.png', name: '서비스 5' },
    { id: 6, icon: '/icons/service6.png', name: '서비스 6' },
    { id: 7, icon: '/icons/service7.png', name: '서비스 7' },
    { id: 8, icon: '/icons/service8.png', name: '서비스 8' },
    { id: 9, icon: '/icons/service9.png', name: '서비스 9' },
    { id: 10, icon: '/icons/service10.png', name: '서비스 10' },
    { id: 11, icon: '/icons/service11.png', name: '서비스 11' },
    { id: 12, icon: '/icons/service12.png', name: '서비스 12' },
    { id: 13, icon: '/icons/service12.png', name: '서비스 13' },
    { id: 14, icon: '/icons/service12.png', name: '서비스 14' },
    { id: 15, icon: '/icons/service12.png', name: '서비스 15' },
    { id: 16, icon: '/icons/service12.png', name: '서비스 16' },
]);

const isAuthenticated = computed(() => store.getters.isAuthenticated);
const catches = computed(() => store.getters.catches);

// Define backend base URL
const BACKEND_BASE_URL = 'http://localhost:5000';

const isImagePopupVisible = ref(false);
const popupImageUrl = ref('');

function openImagePopup(imageUrl) {
    popupImageUrl.value = `${BACKEND_BASE_URL}/uploads/${imageUrl}`; // Updated to include BACKEND_BASE_URL
    isImagePopupVisible.value = true;
}

onMounted(() => {
    store.dispatch("fetchCatches"); // Fetch catches when the component is mounted
    if (isAuthenticated.value) {
        store.dispatch('fetchCatches');
    }
});

const logout = () => {
    localStorage.removeItem('token');
    store.dispatch('logout');
    router.push('/login');
};

const editProfile = () => {
    router.push('/edit-profile');
};

const goToCatches = () => {
    router.push('/catches');
};
</script>

<style scoped>
/* 미세 조정 */
@media (min-width: 768px) {
    .md\:flex-row {
        flex-direction: row;
    }

    .md\:items-center {
        align-items: center;
    }

    .md\:justify-between {
        justify-content: space-between;
    }
}

.fixed {
    position: fixed;
}

.absolute {
    position: absolute;
}

/* Ensure pop-up images are displayed correctly */
.object-contain {
    object-fit: contain;
}
</style>