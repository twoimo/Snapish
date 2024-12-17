import os
import logging
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
from functools import wraps
import jwt
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
from werkzeug.security import generate_password_hash, check_password_hash
from services.weather_service import get_weather_by_coordinates
from services.location_service import get_location_by_coordinates
from services.lunar_mulddae import get_mulddae_cycle, calculate_moon_phase

# 환경 변수 로드
load_dotenv("./.env")

SQL_KEY = os.getenv("SQL_KEY")

# 데이터베이스 설정
DATABASE_URL = os.getenv('DATABASE_URL', f'mysql+pymysql://root:{SQL_KEY}@localhost:3306/snapish')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
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
    preferred_font_size = Column(Enum('small', 'medium', 'large'), default='medium')
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
CORS(app, supports_credentials=True)  # Update CORS configuration to allow credentials
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

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': '모든 필드를 채워주세요.'}), 400

    session = Session()
    existing_user = session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        session.close()
        return jsonify({'message': '이미 사용 중인 아이디나 이메일입니다.'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        created_at=datetime.utcnow()
    )

    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({'message': '회원가입이 성공적으로 완료되었습니다.'}), 201

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # 실제 서비스에서는 안전한 키로 변경하세요.

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user and check_password_hash(user.password_hash, password):
        # 토큰 생성
        payload = {
            'user_id': user.user_id,
            'exp': datetime.utcnow() + timedelta(hours=24)  # 수정된 부분
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': '로그인 성공',
            'token': token,
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                # 필요한 사용자 정보 추가
            }
        })
    else:
        return jsonify({'message': '로그인 실패'}), 401
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 헤더에서 토큰 가져오기
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': '토큰이 필요합니다.'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']

            session = Session()
            current_user = session.query(User).filter_by(user_id=user_id).first()
            session.close()

            if not current_user:
                return jsonify({'message': '유효하지 않은 토큰입니다.'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '토큰이 만료되었습니다.'}), 401
        except Exception:
            return jsonify({'message': '토큰 인증에 실패하였습니다.'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile(current_user):
    if request.method == 'GET':
        return jsonify({
            'user_id': current_user.user_id,
            'username': current_user.username,
            'email': current_user.email,
            # 필요한 정보 추가
        })
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid input'}), 400
        # 사용자 정보 업데이트
        current_user.username = data.get('username', current_user.username)
        current_user.email = data.get('email', current_user.email)
        # 비밀번호 변경 처리
        if data.get('current_password') and data.get('new_password'):
            if check_password_hash(current_user.password_hash, data['current_password']):
                current_user.password_hash = generate_password_hash(data['new_password'])
            else:
                return jsonify({'message': '현재 비밀번호가 일치하지 않습니다.'}), 400
        session = Session()
        session.add(current_user)
        session.commit()
        session.close()
        return jsonify({'message': '프로필이 성공적으로 업데이트되었습니다.'}), 200

@app.route('/recent-activities', methods=['GET'])
@token_required
def recent_activities(current_user):
    # 최근 활동을 조회하는 로직 (예: 데이터베이스에서 최근 5개의 캐치를 가져오기)
    session = Session()
    activities = session.query(Catch).filter_by(user_id=current_user.user_id).order_by(Catch.catch_date.desc()).limit(5).all()
    session.close()
    
    recent_activities = [
        {
            'fish': catch.species.name if catch.species else '알 수 없음',
            'location': catch.location.address if catch.location else '알 수 없음',
            'date': catch.catch_date.strftime('%Y-%m-%d'),
            'image': catch.photo_url or '/placeholder.svg?height=80&width=80',
        }
        for catch in activities
    ]
    
    return jsonify({'activities': recent_activities})

@app.route('/catches', methods=['POST'])
@token_required
def add_catch(current_user):
    data = request.get_json()
    imageUrl = data.get('imageUrl')
    detections = data.get('detections')

    if not imageUrl or not detections:
        return jsonify({'message': '이미지 URL과 감지 결과가 필요합니다.'}), 400

    session = Session()
    new_catch = Catch(
        user_id=current_user.user_id,
        photo_url=imageUrl,
        exif_data=detections,
        catch_date=datetime.utcnow()
    )
    session.add(new_catch)
    session.commit()
    session.close()

    return jsonify({'message': '캐치가 성공적으로 추가되었습니다.'}), 201

@app.route('/catches', methods=['GET'])
@token_required
def get_catches(current_user):
    session = Session()
    catches = session.query(Catch).filter_by(user_id=current_user.user_id).all()
    session.close()

    return jsonify([{
        'imageUrl': catch.photo_url,
        'detections': catch.exif_data,
        'catch_date': catch.catch_date.strftime('%Y-%m-%d')
    } for catch in catches])


@app.route('/api/map_fishing_spot', methods=['POST'])
# 추후 Token 관련 데코레이터 추가할 것
def map_fishing_spot():
    session = Session()
    fishing_spots = session.query(Location).all()
    session.close()

    try:
        locations = [{
            'location_id': spot.location_id,
            'latitude': spot.latitude,
            'longitude': spot.longitude,
            'address_ko': spot.address
        } for spot in fishing_spots]
        
        
        return jsonify({
            'message': 'DB호출 완료',
            'location': locations
        })
    except Exception as e:
        return jsonify({f'message : 호출 실패, {e}'}), 401

# 애플리케이션 종료 시 세션 제거
@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)