<!-- filepath: /c:/Users/twoimo/Documents/GitHub/Snapish/frontend/src/views/EditProfile.vue -->
<template>
    <div class="edit-profile-container">
        <h1>프로필 수정</h1>
        <form @submit.prevent="handleEditProfile">
            <input v-model="fullName" type="text" placeholder="이름" required />
            <input v-model="email" type="email" placeholder="이메일" required />
            <!-- 추가 필드 -->
            <button type="submit">저장</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const fullName = ref('');
const email = ref('');
const router = useRouter();
const store = useStore();

const handleEditProfile = async () => {
    try {
        await store.dispatch('updateProfile', {
            full_name: fullName.value,
            email: email.value,
            // 추가 필드
        });
        router.push('/profile');
    } catch (error) {
        alert('프로필 수정에 실패했습니다.');
        console.error('프로필 수정 오류:', error);
    }
};
</script>

<style scoped>
.edit-profile-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.edit-profile-container h1 {
    margin-bottom: 1.5rem;
    text-align: center;
}

.edit-profile-container form {
    display: flex;
    flex-direction: column;
}

.edit-profile-container input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.edit-profile-container button {
    padding: 0.75rem;
    background-color: #38c172;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.edit-profile-container button:hover {
    background-color: #2fa24c;
}
</style>