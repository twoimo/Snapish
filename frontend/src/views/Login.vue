<template>
    <div class="flex items-center justify-center bg-gray-100" style="min-height: calc(100vh - 112px);">
        <div class="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
            <h1 class="text-4xl font-semibold text-center text-gray-800 mb-6">로그인</h1>
            <form @submit.prevent="handleLogin" class="space-y-4">
                <input v-model="username" type="text" placeholder="아이디" required
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="password" type="password" placeholder="비밀번호" required
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <button type="submit"
                    class="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    로그인
                </button>
            </form>
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
        alert('로그인 실패: 아이디 또는 비밀번호를 확인하세요.');
        console.error('로그인 오류:', error);
    }
};
</script>
