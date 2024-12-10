# Snapish: 물고기 판별 AI 웹 서비스
![image](https://github.com/user-attachments/assets/ce26f167-06ef-4978-b4bb-d459eeed751b)

# 백엔드
먼저 백엔드 폴더로 이동하세요. `cd backend`. 제공된 `environment.yml`을 사용하여 필요한 패키지가 있는 새로운 conda 환경을 생성하고, 그 다음에 새로 생성된 환경을 활성화하는 것을 권장합니다.
```bash
conda env create -n snapish --file environment.yml
conda activate snapish
```
예측 모델의 가중치를 [여기](https://owncloud.tuwien.ac.at/index.php/s/kotvEsald31Pw51)에서 다운로드하세요. 백엔드에 `models` 폴더를 생성하고 (`mkdir models`), 다운로드한 `*.pth` 파일을 이 디렉토리에 복사하세요.

플라스크 앱을 다음과 같이 시작하세요.
```bash
$env:FLASK_APP="main.py"
flask run --host=0.0.0.0
```

# 프론트엔드
백엔드 폴더에 있는 경우 `cd ../frontend`를 실행하여 프론트엔드 폴더로 이동하세요.
프론트엔드를 설정하고 실행하기 위해서는 node.js가 필요하므로 [여기](https://nodejs.org/en/)의 지침을 따르세요.
이제 필요한 패키지를 다음과 같이 설치하세요 (시간이 좀 걸릴 수 있습니다):
```bash
npm install
```
추천 항목(여기서는 여행지의 사진)의 이미지를 [여기](https://owncloud.tuwien.ac.at/index.php/s/h70PGy8EkqtQKxs)에서 다운로드하세요. `public` 폴더 아래에 `pics` 폴더를 생성하세요 (`mkdir public/pics`). 다운로드한 `*.zip`의 내용을 새로 생성된 `pics` 디렉토리에 복사하세요. 이제 `public/pics/destination_id/pic_id.jpg` 구조가 되어야 합니다.

프론트엔드를 다음과 같이 컴파일하고 실행하세요.
```bash
npm run serve
```
