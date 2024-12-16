
<template>
    <div>
        <div id="kakaoMap"></div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                map : null
            }
        },
        mounted() {
                const script = document.createElement("script");
                const key = process.env.VUE_APP_KAKAO_API_KEY
                script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}`;
                document.head.appendChild(script);
                    /*
                    스크립트가 로드 되기전에 kakao객체에 접근하여 kakao객체를 찾지 못해 발생하는 에러를
                    방지하기 위해 스크립트가 로드 된 뒤에 실제 지도를 그리도록 함
                    */
                    script.onload = () => { kakao.maps.load(()=>{
                        var container = document.getElementById('kakaoMap'); //지도를 담을 영역의 DOM 레퍼런스
                        var options = { //지도를 생성할 때 필요한 기본 옵션
                            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
                            level: 3 //지도의 레벨(확대, 축소 정도)
                        };
                        //eslint-disable-next-line no-unused-vars
                        var map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
                    })
                }
        },
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