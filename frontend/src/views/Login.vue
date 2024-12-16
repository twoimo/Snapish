<template>
    <div class="login-container">
        <h1 class="text-3xl font-bold text-center mb-6">로그인</h1>
        <form @submit.prevent="handleLogin">
            <input v-model="username" type="text" placeholder="아이디" required />
            <input v-model="password" type="password" placeholder="비밀번호" required />
            <button type="submit">로그인</button>
        </form><br>
        <p>
            아직 계정이 없으신가요?
            <router-link to="/signup" class="text-blue-500 hover:underline">회원가입</router-link>
        </p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; // Vuex 스토어 사용

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

        // 프로필 페이지로 이동
        router.push('/profile');
    } catch (error) {
        alert('로그인 실패: 아이디 또는 비밀번호를 확인하세요.');
        console.error('로그인 오류:', error);
    }
};
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.login-container h1 {
    margin-bottom: 1.5rem;
}

.login-container form {
    display: flex;
    flex-direction: column;
}

.login-container input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.login-container button {
    padding: 0.75rem;
    background-color: #3490dc;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.login-container button:hover {
    background-color: #2779bd;
}
</style>