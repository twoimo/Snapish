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
                map : null,
                mapHeight: '80vh'
            }
        },
        mounted() {
            this.mapHeight = this.mapType === 'A' ? '80vh' : '40vh';
            if (this.mapType === 'A') {
                this._initializeKakaoMap_fullview();
            } else {
                this._initializeKakaoMap_spotview();
            }
        },
        methods: {
            _initializeKakaoMap_fullview() {
                try {
                    const script = document.createElement("script");
                    const key = process.env.VUE_APP_KAKAO_API_KEY;
                    
                    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}&libraries=clusterer`;
                    document.head.appendChild(script);

                    script.onload = () => { 
                        try {
                            kakao.maps.load(() => {
                                // 1. 지도 생성
                                var container = document.getElementById('kakaoMap');
                                var options = {
                                    center: new kakao.maps.LatLng(36.0, 128.0),
                                    level: 15
                                };
                                var map = new kakao.maps.Map(container, options);

                                // 2. 지도 생성이 끝난 후 클러스터러 실행
                                map.addListener('tilesloaded', () => { // 지도 타일 로드 완료 이벤트
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
                            });
                        } catch (error) {
                            console.error(error);
                            alert("Maps Fullview:" + error.message);
                        } finally {
                            console.log("load KAKAOmap _ Spotview");
                        }
                    };

                } catch (error) {
                    console.error(error);
                    alert('Kakao 지도 스크립트 로드 중 문제가 발생했습니다.');
                }
            },
            _initializeKakaoMap_spotview() {
                try {
                    const script = document.createElement("script");
                    const key = process.env.VUE_APP_KAKAO_API_KEY;
                    
                    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}`;
                    document.head.appendChild(script);

                    script.onload = () => { 
                        kakao.maps.load(() => {
                            try {
                                // 1. 지도 초기화
                                const container = document.getElementById('kakaoMap');
                                const options = {
                                    center: new kakao.maps.LatLng(
                                        parseFloat(this.locations[0].latitude),
                                        parseFloat(this.locations[0].longitude)
                                    ),
                                    level: 15
                                };
                                const map = new kakao.maps.Map(container, options);

                                // 2. 지도 타일 로드 완료 이벤트 등록
                                map.addListener('tilesloaded', () => {
                                    console.log('지도 타일이 모두 로드되었습니다.');

                                    // 타일 로드 후 실행할 작업
                                    const marker = new kakao.maps.Marker({
                                        position: new kakao.maps.LatLng(
                                            parseFloat(this.locations[0].latitude),
                                            parseFloat(this.locations[0].longitude)
                                        )
                                    });
                                    marker.setMap(map);
                                });
                            } catch (error) {
                                console.error(error);
                                alert("Maps Spotview:" + error.message);
                            } finally {
                                console.log("load KAKAOmap _ Spotview");
                            }
                        })
                    }
                } catch (error) {
                    console.error(error);
                    alert('Kakao 지도 스크립트 로드 중 문제가 발생했습니다.');
                }
            }
        }
    }
 

</script>

<style scoped>
    #kakaoMap {
        width: 100%;
        height: v-bind(mapHeight);
        margin: 0px auto;
        display: block;
    } 
</style>