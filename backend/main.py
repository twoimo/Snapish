from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용

# 모델 로드
model = YOLO('./models/yolo11m_ep50_confi91_predict.pt')  # 모델 경로 지정

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

    # 예측 결과에서 라벨 및 신뢰도 추출 및 한국어로 치환
    detections = []
    for result in results:
        for cls, conf in zip(result.boxes.cls, result.boxes.conf):
            cls_int = int(cls)
            korean_label = labels_korean.get(cls_int, '알 수 없는 라벨')
            confidence = float(conf)
            detections.append({
                'label': korean_label,
                'confidence': confidence
            })
    print("detections before sorting: ", detections)

    # 신뢰도 순으로 정렬 (높은 신뢰도 먼저)
    detections.sort(key=lambda x: x['confidence'], reverse=True)
    print("detections after sorting: ", detections)

    # 후보군이 없을 경우 '알 수 없음'으로 설정
    if not detections:
        detections.append({
            'label': '알 수 없음',
            'confidence': 0.0
        })
        print("No detections found. Appended '알 수 없음'.")

    return jsonify({'detections': detections})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)