<template>
    <div class="flex items-center justify-center bg-gray-100" style="min-height: calc(100vh - 112px);">
        <div class="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
            <h1 class="text-4xl font-semibold text-center text-gray-800 mb-6">로그인</h1>
            <form @submit.prevent="handleLogin" class="space-y-4">
                <div>
                    <label for="username">아이디</label>
                    <input type="text" id="username" v-model="username" required
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                    <label for="password">비밀번호</label>
                    <input type="password" id="password" v-model="password" required
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <button type="submit"
                    class="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    로그인
                </button>
            </form>
            <p v-if="errorMessage" class="mt-6 text-center text-red-600">{{ errorMessage }}</p>
            <p class="mt-6 text-center text-gray-600">
                아직 계정이 없으신가요?
                <router-link to="/signup" class="text-blue-500 hover:underline">회원가입</router-link>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();
const store = useStore();

const handleLogin = async () => {
    try {
        await store.dispatch('login', {
            username: username.value,
            password: password.value,
        });

        router.push('/profile');
    } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
            errorMessage.value = error.response.data.message;
        } else {
            errorMessage.value = '로그인 중 오류가 발생했습니다.';
        }
        console.error('로그인 오류:', error);
    }
};
</script>
