<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-md bg-white shadow-lg">
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

            <!-- Main Content -->
            <main class="pb-20 px-4">
                <!-- Today's Weather -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">오늘의 날씨</h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
                        <div class="flex items-center justify-center h-32 bg-gray-200 rounded">
                            <CloudIcon class="w-12 h-12 text-gray-400" />
                        </div>
                    </div>
                </section>

                <!-- My Catches -->
                <section class="mb-6">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">내가 잡은 물고기</h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div class="grid grid-cols-3 gap-3">
                        <div v-for="i in 3" :key="i" class="bg-gray-50 rounded-lg p-3 shadow-sm">
                            <div class="flex items-center justify-center h-24 bg-gray-200 rounded mb-2">
                                <FishIcon class="w-8 h-8 text-gray-400" />
                            </div>
                            <p class="text-sm text-gray-600">물고기</p>
                            <p class="text-sm">종류</p>
                        </div>
                    </div>
                </section>

                <!-- Community -->
                <section>
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">
                            <router-link to="/community" class="flex flex-col items-center p-2">
                                커뮤니티
                            </router-link>
                        </h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div class="space-y-3">
                        <article v-for="i in 4" :key="i" class="bg-gray-50 rounded-lg p-4 shadow-sm">
                            <div class="flex gap-3">
                                <div
                                    class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center flex-shrink-0">
                                    <ImageIcon class="w-8 h-8 text-gray-400" />
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-medium mb-1">게시물 제목</h3>
                                    <p class="text-sm text-gray-600 mb-2">게시물 내용 미리보기입니다. 여기에 간단한 설명이 들어갑니다.</p>
                                    <div class="flex items-center text-sm text-gray-500">
                                        <ClockIcon class="w-4 h-4 mr-1" />
                                        <span>오늘 • 23분 전</span>
                                    </div>
                                </div>
                                <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                            </div>
                        </article>
                    </div>
                </section>
            </main>

            <!-- Bottom Navigation -->
            <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
                <div class="flex justify-between items-center">
                    <button class="flex flex-col items-center p-2">
                        <HomeIcon class="w-6 h-6" />
                        <span class="text-xs mt-1">커뮤니티</span>
                    </button>
                    <button class="flex flex-col items-center p-2">
                        <PlusCircleIcon class="w-6 h-6" />
                        <span class="text-xs mt-1">사진 찍기</span>
                    </button>
                    <button class="flex flex-col items-center p-2">
                        <UserIcon class="w-6 h-6" />
                        <span class="text-xs mt-1">프로필</span>
                    </button>
                </div>
            </nav>
        </div>
    </div>
</template>

<script setup>
import {
    BellIcon,
    Settings2Icon,
    ChevronRightIcon,
    CloudIcon,
    FishIcon,
    ImageIcon,
    ClockIcon,
    HomeIcon,
    PlusCircleIcon,
    UserIcon
} from 'lucide-vue-next'
</script>