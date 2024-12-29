<template>
  <header class="bg-white shadow">
    <!-- 네비게이션 바 -->
    <nav class="container mx-auto px-4 py-3 flex justify-between items-center">
      <!-- 사이트 제목 -->
      <h1 class="text-xl font-bold cursor-pointer" @click="$router.push('/')">SNAPISH</h1>
      <div class="flex items-center">
        <button class="p-2" @click="handleLogout" title="로그아웃">
          <LogOutIcon class="w-6 h-6" />
        </button>
      </div>
    </nav>
  </header>
</template>

<script>
import { LogOutIcon } from 'lucide-vue-next'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AppHeader',
  components: {
    LogOutIcon
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const handleLogout = async () => {
      await store.dispatch('logout')
      router.push('/login')
    }

    return {
      handleLogout
    }
  }
}
</script>
