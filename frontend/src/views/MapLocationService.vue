<template>
  <div id="container">
    <MapComponent></MapComponent>
  </div>
</template>

<script>
import MapComponent from '../components/MapComponent.vue';
export default {
  components: {
    // MapComponent 등록
    MapComponent,
  },
};
</script>

<style scoped>
#container {
    width: 100%;
    height: 100%;
    max-width: 1500px; /* 전체 컨테이너의 최대 너비 제한 */
    margin: 0 auto; /* 가운데 정렬 */
}
</style>