<template>
  <div class="details-content">
    <div class="button-container">
      <button class="check-btn" >위치 확인</button> 
      <button class="close-btn" @click="$emit('close')">닫기</button> 
    </div>

    <br>
    <section class=" mb-6 pt-4">   
      <div class="place-name"> {{ location.location_id }} </div>
      <p><strong>주소:</strong> {{ location.address_ko }}</p>
      <p><strong>설명:</strong> {{ location.details }}</p>
    </section>

    <section class="mb-6 pt-4">
      날씨
    </section>
  </div>
</template>

<script>
export default {
  props: {
    location: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>

.place-name {
  font-size: 32px;
  font-weight: bold;
}

.details-content {
  padding: 20px;
  overflow-y: auto;
  max-height: 100%;
}

/* 버튼을 오른쪽 끝으로 이동 */
.button-container {
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
  gap: 10px; /* 버튼 사이 간격 */
}

/* 위치 확인 버튼 스타일 */
.check-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #4caf50; /* 초록색 */
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.check-btn:hover {
  background-color: #45a045; /* 진한 초록색 */
}

.close-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #ff5a5a;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  float: right;
}

.close-btn:hover {
  background-color: #e04e4e;
}

</style>
