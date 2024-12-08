<template>
    <!-- Header -->
    <header class="sticky top-0 bg-white z-50 px-4 py-3 flex justify-between items-center border-b">
        <h1 class="text-xl font-bold">SNAPish</h1>
        <div class="flex items-center gap-4">
            <button class="p-2">
                <BellIcon class="w-6 h-6" />
            </button>
            <button class="p-2">
                <Settings2Icon class="w-6 h-6" />
            </button>
        </div>
    </header>
    <div class="min-h-screen bg-gray-100">
        <div class="bg-white pb-6">
            <!-- Profile Header -->
            <div class="p-4 flex flex-col items-center">
                <div class="w-24 h-24 rounded-full bg-gray-200 mb-4"></div>
                <h1 class="text-xl font-bold mb-1">홍길동</h1>
                <p class="text-gray-600 flex items-center mb-4">
                    낚시 초보자
                    <FishIcon class="w-4 h-4 ml-1" />
                </p>
                <button class="bg-blue-500 text-white px-6 py-2 rounded-md">
                    프로필 수정
                </button>
            </div>

            <!-- Stats -->
            <div class="flex justify-around py-4 border-t border-b">
                <div class="text-center">
                    <div class="font-bold">156</div>
                    <div class="text-sm text-gray-600">catches</div>
                </div>
                <div class="text-center">
                    <div class="font-bold">230</div>
                    <div class="text-sm text-gray-600">followers</div>
                </div>
                <div class="text-center">
                    <div class="font-bold">184</div>
                    <div class="text-sm text-gray-600">following</div>
                </div>
            </div>
        </div>

        <!-- Recent Activities -->
        <div class="p-4">
            <h2 class="text-lg font-bold mb-4">최근 활동</h2>
            <div class="space-y-4">
                <div v-for="(activity, index) in recentActivities" :key="index"
                    class="bg-white p-4 rounded-lg shadow-sm">
                    <div class="flex items-start">
                        <img :src="activity.image" alt="" class="w-20 h-20 rounded-lg object-cover" />
                        <div class="ml-4">
                            <h3 class="font-bold">{{ activity.fish }}</h3>
                            <p class="text-gray-600">{{ activity.location }}</p>
                            <p class="text-sm text-gray-500">{{ activity.date }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { FishIcon, BellIcon, Settings2Icon } from 'lucide-vue-next'

const recentActivities = [
    {
        fish: '농어',
        location: '부산 해운대',
        date: '2024.02.15',
        image: '/placeholder.svg?height=80&width=80'
    },
    {
        fish: '고등어',
        location: '제주 서귀포',
        date: '2024.02.10',
        image: '/placeholder.svg?height=80&width=80'
    },
    {
        fish: '광어',
        location: '인천 월미도',
        date: '2024.01.10',
        image: '/placeholder.svg?height=80&width=80'
    }
]
</script>