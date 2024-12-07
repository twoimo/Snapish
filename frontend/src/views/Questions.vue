<template>
  <div class="questions">
    <h1 class="text-2xl font-bold mb-4">Questionnaire</h1>
    <Questions />
  </div>
</template>

<script>
import Questions from '@/components/Questions.vue'

export default {
  name: 'QuestionsView',
  components: {
    Questions
  }
}
</script>
