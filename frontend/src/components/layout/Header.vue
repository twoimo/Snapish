<template>
  <header class="bg-white shadow">
    <nav class="container mx-auto px-4 py-3 flex justify-between items-center">
      <h1 class="text-xl font-bold">SNAPish</h1>
      <div class="flex items-center gap-4">
        <button class="p-2">
          <BellIcon class="w-6 h-6" />
        </button>
        <button class="p-2">
          <Settings2Icon class="w-6 h-6" />
        </button>
      </div>
    </nav>
  </header>
</template>

<script>
import { BellIcon, Settings2Icon } from 'lucide-vue-next'

export default {
  name: 'AppHeader',
  components: {
    BellIcon,
    Settings2Icon
  }
}
</script>
