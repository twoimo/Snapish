from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용

# 모델 로드
model = YOLO('./models/yolo11n_ep20_confi83_predict.pt')  # 모델 경로 지정

# 라벨 매핑 (영어 -> 한국어)
labels_korean = {
    0: '넙치',
    1: '조피볼락',
    2: '참돔',
    3: '감성돔',
    4: '돌돔'
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다.'}), 400

    file = request.files['image']
    img_bytes = file.read()

    try:
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')  # RGB로 변환
    except Exception as e:
        return jsonify({'error': '이미지 파일을 열 수 없습니다.'}), 400

    # 모델 예측
    results = model(img, exist_ok=True, device='cpu')  # 필요에 따라 device 설정

    # 예측 결과에서 라벨 추출 및 한국어로 치환
    labels = []
    for result in results:
        for cls in result.boxes.cls:
            cls_int = int(cls)
            korean_label = labels_korean.get(cls_int, '알 수 없는 라벨')
            labels.append(korean_label)
    print("labels: ", labels)

    return jsonify({'labels': labels})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)