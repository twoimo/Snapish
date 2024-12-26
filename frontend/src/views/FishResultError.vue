<template>
    <div class="error-container">
        <div class="error-content">
            <img :src="errorImage" alt="Error" class="error-icon">
            <h2>{{ errorMessage }}</h2>
            <p>{{ errorDescription }}</p>
            <div class="button-group">
                <button @click="goBack" class="back-button">
                    이전으로
                </button>
                <button @click="goToCamera" class="camera-button">
                    다시 촬영하기
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FishResultError',
    data() {
        return {
            errorTypes: {
                no_detection: {
                    message: '물고기를 감지할 수 없습니다.',
                    description: '물고기가 포함된 사진을 다시 촬영해주세요.',
                    // image: require('@/assets/no-detection.png')
                },
                low_confidence: {
                    message: '물고기를 정확하게 인식할 수 없습니다.',
                    description: '더 선명한 사진으로 다시 시도해주세요.',
                    // image: require('@/assets/low-confidence.png')
                }
            }
        }
    },
    computed: {
        errorType() {
            return this.$route.query.errorType || 'no_detection'
        },
        errorMessage() {
            return this.$route.query.message || this.errorTypes[this.errorType].message
        },
        errorDescription() {
            return this.errorTypes[this.errorType].description
        },
        errorImage() {
            return this.errorTypes[this.errorType].image
        }
    },
    methods: {
        goBack() {
            this.$router.go(-1)
        },
        goToCamera() {
            this.$router.push('/camera')
        }
    }
}
</script>

<style scoped>

</style>