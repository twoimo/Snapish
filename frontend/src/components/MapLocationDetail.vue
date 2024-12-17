<template>
  <div class="details-content">
    <button class="close-btn" @click="$emit('close')">닫기</button>  
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

.close-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #ff5a5a;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.close-btn:hover {
  background-color: #e04e4e;
}

</style>
