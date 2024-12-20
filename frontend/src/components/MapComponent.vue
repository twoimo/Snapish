<template>
    <div>
        <div id="kakaoMap"></div>
    </div>
</template>

<script>
    export default {
        props: {
            locations: {
                type: Array,
                required: true,
            },
            mapType: {
                type: String,
                default: 'A'
            }
        },
        data () {
            return {
                map : null
            }
        },
        mounted() {
            if (this.mapType === 'A') {
                this._initializeKakaoMap_A();
            } else {
                this._initializeKakaoMap_B();
            }
        },
        methods: {
            _initializeKakaoMap_A() {
                try {
                    const script = document.createElement("script");
                    const key = process.env.VUE_APP_KAKAO_API_KEY
                    
                    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}&libraries=clusterer`;
                    document.head.appendChild(script);

                    script.onload = () => { 
                        kakao.maps.load(() => {
                            var container = document.getElementById('kakaoMap');
                            var options = {
                                center: new kakao.maps.LatLng(36.0, 128.0),
                                level: 15
                            };
                            var map = new kakao.maps.Map(container, options);

                            var clusterer = new kakao.maps.MarkerClusterer({
                                map: map,
                                averageCenter: true,
                                minLevel: 10
                            });

                            var markers = this.locations.map(location => {
                                return new kakao.maps.Marker({
                                    position: new kakao.maps.LatLng(
                                        parseFloat(location.latitude),
                                        parseFloat(location.longitude)
                                    ),
                                });
                            });

                            clusterer.addMarkers(markers);
                        });
                    };
                } catch (error) {
                    alert("Maps A:" + error.message);
                } finally {
                    console.log("load KAKAOmap A");
                }
            },
            _initializeKakaoMap_B() {
                try {
                    const script = document.createElement("script");
                    const key = process.env.VUE_APP_KAKAO_API_KEY
                    
                    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}&libraries=clusterer`;
                    document.head.appendChild(script);

                    script.onload = () => { 
                        kakao.maps.load(() => {
                            var container = document.getElementById('kakaoMap');
                            var options = {
                                center: new kakao.maps.LatLng(36.0, 128.0),
                                level: 13
                            };
                            var map = new kakao.maps.Map(container, options);

                            var clusterer = new kakao.maps.MarkerClusterer({
                                map: map,
                                averageCenter: true,
                                minLevel: 8
                            });

                            var markers = this.locations.map(location => {
                                return new kakao.maps.Marker({
                                    position: new kakao.maps.LatLng(
                                        parseFloat(location.latitude),
                                        parseFloat(location.longitude)
                                    ),
                                });
                            });

                            clusterer.addMarkers(markers);
                        });
                    };
                } catch (error) {
                    alert("Maps B:" + error.message);
                } finally {
                    console.log("load KAKAOmap B");
                }
            }
        }
    }
</script>

<style scoped>
    #kakaoMap {
        width: 100%; /* 적절한 너비로 설정 */
        height: 80vh; /* 뷰포트 높이의 80% */
        margin: 0px auto; /* 상단 여백은 17px, 좌우 가운데 정렬 */
        display: block; /* 가운데 정렬을 위해 블록 요소로 설정 */
        } 
</style>