<!-- filepath: /c:/Users/twoimo/Documents/GitHub/Snapish/frontend/src/views/Signup.vue -->
<template>
    <div class="signup-container">
        <h1 class="text-3xl font-bold text-center mb-6">회원가입</h1>
        <form @submit.prevent="handleSignup">
            <input v-model="username" type="text" placeholder="아이디" required />
            <input v-model="email" type="email" placeholder="이메일" required />
            <input v-model="password" type="password" placeholder="비밀번호" required />
            <input v-model="confirmPassword" type="password" placeholder="비밀번호 확인" required />
            <button type="submit">회원가입</button>
        </form><br>
        <p>
            이미 계정이 있으신가요?
            <router-link to="/login" class="text-blue-500 hover:underline">로그인</router-link>
        </p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; // Vuex 스토어 사용

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();
const store = useStore();

const handleSignup = async () => {
    if (password.value !== confirmPassword.value) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
    }

    try {
        await store.dispatch('signup', {
            username: username.value,
            email: email.value,
            password: password.value,
        });

        // 회원가입 후 로그인 페이지로 이동
        router.push('/login');
    } catch (error) {
        alert('회원가입 실패: 이미 사용 중인 아이디나 이메일입니다.');
        console.error('회원가입 오류:', error);
    }
};
</script>

<style scoped>
.signup-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.signup-container h1 {
    margin-bottom: 1.5rem;
}

.signup-container form {
    display: flex;
    flex-direction: column;
}

.signup-container input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.signup-container button {
    padding: 0.75rem;
    background-color: #38c172;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.signup-container button:hover {
    background-color: #2fa24c;
}
</style>