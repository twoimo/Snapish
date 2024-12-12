<template>
    <div>
      <div v-if="loading">정보를 가져오는 중...</div>
      <div v-else-if="mulddae">
        <h2>서해 물때: {{ mulddae.seohae }}</h2>
        <h2>다른 지역 물때: {{ mulddae.other }}</h2>
      </div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>물때 정보를 불러오지 못했습니다.</div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from "vuex";
  
  export default {
    computed: {
      ...mapState(["currentlocation", "loading", "error", "mulddae"]),
    },
    methods: {
      ...mapActions(["fetchMulddae"]),
      fetchTodayMulddae() {
        const today = new Date().toISOString().split("T")[0]; // 오늘 날짜 (YYYY-MM-DD 형식)
        this.fetchMulddae(today);
      },
    },
    mounted() {
      this.fetchTodayMulddae(); // 컴포넌트 로드 시 오늘 날짜로 물때 정보 요청
    },
  };
  </script>