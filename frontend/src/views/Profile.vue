<template>
    <div class="min-h-screen bg-white flex flex-col items-center">
        <div class="bg-white w-full max-w-4xl rounded-lg mt-6">
            <!-- 프로필 헤더 -->
            <div v-if="user" class="p-6 flex flex-col items-center md:flex-row md:items-center md:justify-between">
                <div class="flex items-center">
                    <div class="w-24 h-24 rounded-full bg-gray-200 mb-4 md:mb-0 md:mr-6"
                        :style="{ backgroundImage: `url(${user.avatar || '/default-avatar.png'})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
                    </div>
                    <div class="text-center md:text-left">
                        <h1 class="text-2xl font-bold mb-1">{{ user.full_name || user.username }}</h1>
                        <p class="text-gray-600 flex items-center mb-4">
                            {{ user.tier || '낚시 초보자' }}
                        </p>
                    </div>
                </div>
                <div class="flex space-x-4 mt-4 md:mt-0">
                    <!-- 프로필 수정 아이콘 버튼 -->
                    <button @click="editProfile" class="text-blue-500 hover:text-blue-600 p-2 rounded-md"
                        aria-label="프로필 수정">
                        <!-- 예시 SVG 아이콘 (프로필 수정) -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.196z" />
                        </svg>
                    </button>
                    <!-- 로그아웃 아이콘 버튼 -->
                    <button @click="logout" class="text-red-500 hover:text-red-600 p-2 rounded-md" aria-label="로그아웃">
                        <!-- 예시 SVG 아이콘 (로그아웃) -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                    </button>
                </div>
            </div>
            <div v-else class="p-6 flex flex-col items-center">
                <p>사용자 정보가 로드되지 않았습니다.</p>
                <button @click="logout" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md mt-2">
                    로그아웃
                </button>
            </div>

            <!-- 통계 -->
            <div v-if="stats" class="flex justify-around py-4 border-t border-b">
                <div class="text-center">
                    <div class="font-bold text-xl">{{ stats.catches || 0 }}</div>
                    <div class="text-sm text-gray-600">Catches</div>
                </div>
                <div class="text-center">
                    <div class="font-bold text-xl">{{ stats.followers || 0 }}</div>
                    <div class="text-sm text-gray-600">Followers</div>
                </div>
                <div class="text-center">
                    <div class="font-bold text-xl">{{ stats.following || 0 }}</div>
                    <div class="text-sm text-gray-600">Following</div>
                </div>
            </div>
            <div v-else class="flex justify-around py-4 border-t border-b">
                <div class="text-center">
                    <div class="font-bold text-xl">0</div>
                    <div class="text-sm text-gray-600">Catches</div>
                </div>
                <div class="text-center">
                    <div class="font-bold text-xl">0</div>
                    <div class="text-sm text-gray-600">Followers</div>
                </div>
                <div class="text-center">
                    <div class="font-bold text-xl">0</div>
                    <div class="text-sm text-gray-600">Following</div>
                </div>
            </div>

            <!-- 최근 활동 -->
            <div class="p-6">
                <h2 class="text-lg font-bold mb-4">최근 활동</h2>
                <div v-if="recentActivities && recentActivities.length" class="space-y-4">
                    <div v-for="(activity, index) in recentActivities" :key="index"
                        class="bg-white p-4 rounded-lg shadow-sm">
                        <div class="flex items-start">
                            <img :src="activity.image || '/placeholder.svg'" alt="Fish Image"
                                class="w-20 h-20 rounded-lg object-cover" />
                            <!-- 추가 활동 정보 -->
                            <div class="ml-4">
                                <h3 class="text-md font-semibold">{{ activity.fish }}</h3>
                                <p class="text-gray-600">{{ activity.location }}</p>
                                <p class="text-gray-500 text-sm">{{ activity.date }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>최근 활동이 없습니다.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const user = computed(() => store.getters.user);
const stats = computed(() => store.getters.stats);
const recentActivities = computed(() => store.getters.recentActivities);

const logout = () => {
    // 토큰 삭제
    localStorage.removeItem('token');

    // 스토어 상태 초기화
    store.dispatch('logout');

    // 로그인 페이지로 이동
    router.push('/login');
};

const editProfile = () => {
    router.push('/edit-profile');
};
</script>

<style scoped>
@media (min-width: 768px) {
    .md\\:flex-row {
        flex-direction: row;
    }

    .md\\:items-center {
        align-items: center;
    }

    .md\\:justify-between {
        justify-content: space-between;
    }
}
</style>