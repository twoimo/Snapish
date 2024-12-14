import os
import logging
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import torch
import io

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    Text,
    DECIMAL,
    JSON,
)
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, declarative_base

from services.weather_service import get_weather_by_coordinates
from services.location_service import get_location_by_coordinates
from services.lunar_mulddae import get_mulddae_cycle, calculate_moon_phase

# 환경 변수 로드
load_dotenv()

# 데이터베이스 설정
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:test1234@localhost:3306/snapish')
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

# 베이스 모델 선언
Base = declarative_base()

# 데이터베이스 모델 정의
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    full_name = Column(String(100))
    age = Column(Integer)
    preferred_font_size = Column(Enum('작은', '중간', '큰'), default='중간')
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship('UserSession', back_populates='user', cascade='all, delete')
    locations = relationship('Location', back_populates='user', cascade='all, delete')
    catches = relationship('Catch', back_populates='user', cascade='all, delete')
    rankings = relationship('Ranking', back_populates='user', cascade='all, delete')
    ai_consent = relationship('AIConsent', back_populates='user', uselist=False, cascade='all, delete')
    fish_diaries = relationship('FishDiary', back_populates='user', cascade='all, delete')
    posts = relationship('CommunicationBoard', back_populates='user', cascade='all, delete')
    tournament_participants = relationship('TournamentParticipant', back_populates='user', cascade='all, delete')


class UserSession(Base):
    __tablename__ = 'UserSessions'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    session_token = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='sessions')


class Location(Base):
    __tablename__ = 'Locations'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    address = Column(String(255))
    manual_entry = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='locations')
    weather_data = relationship('WeatherData', back_populates='location', cascade='all, delete')
    catches = relationship('Catch', back_populates='location', cascade='all, delete')


class FishSpecies(Base):
    __tablename__ = 'FishSpecies'

    species_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('freshwater', 'saltwater'), nullable=False)
    is_prohibited = Column(Boolean, default=False)
    prohibited_season_start = Column(DateTime)
    prohibited_season_end = Column(DateTime)
    seasonal_info = Column(String(255))
    bait_recommendation = Column(String(255))

    catches = relationship('Catch', back_populates='species')


class Catch(Base):
    __tablename__ = 'Catches'

    catch_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    location_id = Column(Integer, ForeignKey('Locations.location_id', ondelete='CASCADE'))
    species_id = Column(Integer, ForeignKey('FishSpecies.species_id', ondelete='SET NULL'))
    catch_date = Column(DateTime, default=datetime.utcnow)
    fish_size_cm = Column(DECIMAL(5, 2))
    photo_url = Column(String(255))
    exif_data = Column(JSON)

    user = relationship('User', back_populates='catches')
    location = relationship('Location', back_populates='catches')
    species = relationship('FishSpecies', back_populates='catches')
    tournament_participants = relationship('TournamentParticipant', back_populates='catch', cascade='all, delete')


class Ranking(Base):
    __tablename__ = 'Rankings'

    ranking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    total_catches = Column(Integer, default=0)
    tier = Column(Enum('입문자', '초급자', '중급자', '낚시왕'), default='입문자')
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='rankings')


class AIConsent(Base):
    __tablename__ = 'AIConsent'

    consent_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'), unique=True)
    consent_given = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='ai_consent')


class FishDiary(Base):
    __tablename__ = 'FishDiaries'

    diary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='fish_diaries')


class CommunicationBoard(Base):
    __tablename__ = 'CommunicationBoard'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='posts')


class WeatherData(Base):
    __tablename__ = 'WeatherData'

    weather_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('Locations.location_id', ondelete='CASCADE'))
    date = Column(DateTime, default=datetime.utcnow)
    weather_info = Column(JSON)
    tide_data = Column(JSON)

    location = relationship('Location', back_populates='weather_data')


class Tournament(Base):
    __tablename__ = 'Tournaments'

    tournament_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    participants = relationship('TournamentParticipant', back_populates='tournament', cascade='all, delete')


class TournamentParticipant(Base):
    __tablename__ = 'TournamentParticipants'

    participant_id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('Tournaments.tournament_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    catch_id = Column(Integer, ForeignKey('Catches.catch_id', ondelete='SET NULL'))
    score = Column(Integer)

    tournament = relationship('Tournament', back_populates='participants')
    user = relationship('User', back_populates='tournament_participants')
    catch = relationship('Catch', back_populates='tournament_participants')

# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# 세션 설정
app.session = Session

# 모델 로드
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO('./models/yolo11m_ep50_confi91_predict.pt').to(device)

# 라벨 매핑 (영어 -> 한국어)
labels_korean = {
    0: '넙치',
    1: '조피볼락',
    2: '참돔',
    3: '감성돔',
    4: '돌돔'
}

# REST API
@app.route('/')
def hello():
    return 'Welcome to SNAPISH'

@app.route('/backend/mulddae', methods=['POST'])
def get_mulddae():
    now_date = request.form.get('nowdate')
    if not now_date:
        return jsonify({"error": "The 'nowdate' parameter is required"}), 400

    try:
        parsed_date = datetime.strptime(now_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        lunar_date, seohae, other = get_mulddae_cycle(parsed_date)
        moon_phase = calculate_moon_phase(parsed_date)
        json_result = {
            "lunar_date": lunar_date,
            "seohae": seohae,
            "other": other,
            "moon_phase": moon_phase,
        }
        return jsonify(json_result)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/backend/predict', methods=['POST'])
def predict():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': '이미지가 업로드되지 않았습니다.'}), 400

    try:
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
    except Exception:
        return jsonify({'error': '이미지 파일을 열 수 없습니다.'}), 400

    try:
        results = model(img, exist_ok=True, device=device)
    except Exception as e:
        logging.error(f"Model prediction error: {e}")
        return jsonify({'error': '예측 중 오류가 발생했습니다.'}), 500

    detections = [
        {
            'label': labels_korean.get(int(cls), '알 수 없는 라벨'),
            'confidence': float(conf)
        }
        for result in results
        for cls, conf in zip(result.boxes.cls, result.boxes.conf)
    ]

    detections.sort(key=lambda x: x['confidence'], reverse=True)
    print("detections after sorting:", detections)

    if not detections:
        detections.append({
            'label': '알 수 없음',
            'confidence': 0.0
        })

    return jsonify({'detections': detections})

# 애플리케이션 종료 시 세션 제거
@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)