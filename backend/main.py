import os
import io
import logging
import random
import pandas as pd
import numpy as np

from PIL import Image
from scipy import spatial
from flask import Flask, jsonify, request
import torch
from torchvision import transforms as trn
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

from services.weather_service import get_weather_by_coordinates
from services.location_service import get_location_by_coordinates

# INIT
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "test.db"))

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)

# # METHODS
# SELF_ASSESSMENT = 1
# SIMPLE_AVERAGE = 2
# ORDERED_WEIGHTED_AVERAGE = 3
# RANDOM = 4

# # STEPS
# STEP_ABOUT = 1
# STEP_IMAGE_SELECTION = 2
# STEP_PROFILE_QUESTIONS = 3
# STEP_RECOMMENDATION = 4
# STEP_THX = 5

# # LOAD MODELS
# model_sun = torch.load('models/sun_chillout.pth',
#                        map_location=lambda storage, loc: storage)
# model_sun.eval()
# model_ind = torch.load('models/independence_history.pth',
#                        map_location=lambda storage, loc: storage)
# model_ind.eval()
# model_know = torch.load('models/knowledge_travel.pth',
#                         map_location=lambda storage, loc: storage)
# model_know.eval()
# model_cult = torch.load('models/culture_indulgence.pth',
#                         map_location=lambda storage, loc: storage)
# model_cult.eval()
# model_social = torch.load('models/social_sports.pth',
#                           map_location=lambda storage, loc: storage)
# model_social.eval()
# model_action = torch.load('models/action_fun.pth',
#                           map_location=lambda storage, loc: storage)
# model_action.eval()
# model_nature = torch.load('models/nature_recreation.pth',
#                           map_location=lambda storage, loc: storage)
# model_nature.eval()

# # LOAD RECOMMENDATION BASE
# df = pd.read_csv("data/recbase.csv")
# df.iloc[:, 1:8] = df.iloc[:, 1:8]/100

# # HELPERS FOR PREDICT
# def transform_image(image_bytes):
#     transform = trn.Compose([
#         trn.Resize(256),
#         trn.CenterCrop(224),
#         trn.ToTensor(),
#         trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#     ])
#     image = Image.open(io.BytesIO(image_bytes))
#     return transform(image).unsqueeze(0)


# def predict_factor(model, img):
#     out = model(img)
#     percentage = torch.nn.functional.softmax(out, dim=1)[0]
#     percentage = percentage.cpu().detach().numpy()[1]
#     return percentage


# def profile_aggregation(img_profiles=[], owa=False, debug=False):
#     profile = np.mean(img_profiles, axis=0)
#     if owa:
#         weights = []
#         num_profiles = len(img_profiles)
#         for i in range(1, (num_profiles+1)):
#             weight = 7*((-i) + num_profiles + 1) / \
#                 (np.sum(range(1, (num_profiles + 1))))
#             weights.append(weight)
#         if debug:
#             logging.info(weights)
#         profile = np.average(img_profiles, axis=0, weights=weights)
#     return profile


# # PREDICT
# def predict_seven_factors(files, debug=True, user=0):
#     img_profiles = []
#     i = 0
#     for file in files:
#         # load img
#         try:
#             i += 1
#             img_bytes = file.read()
#             img = transform_image(img_bytes)
#             # predict factors
#             sun_score = predict_factor(model_sun, img)
#             know_score = predict_factor(model_know, img)
#             ind_score = predict_factor(model_ind, img)
#             cult_score = predict_factor(model_cult, img)
#             social_score = predict_factor(model_social, img)
#             action_score = predict_factor(model_action, img)
#             nature_score = predict_factor(model_nature, img)
#             # persist individual image scores
#             image = ImageProfile(
#                 user_id=user.id,
#                 order=i,
#                 f1=float(sun_score),
#                 f2=float(know_score),
#                 f3=float(ind_score),
#                 f4=float(cult_score),
#                 f5=float(social_score),
#                 f6=float(action_score),
#                 f7=float(nature_score),
#             )
#             db.session.add(image)
#             # update individual img profiles list
#             img_profiles.append([
#                 sun_score,
#                 know_score,
#                 ind_score,
#                 cult_score,
#                 social_score,
#                 action_score,
#                 nature_score])
#             if debug:
#                 logging.info("{} - image {}\nsun chillout:\t\t{}\nknowledge travel:\t{}\nindependence history:\t{}\nculture indulgence:\t{}\nsocial sports:\t\t{}\naction fun:\t\t{}\nnature recration\t{}".format(
#                     user, i, sun_score, know_score, ind_score, cult_score, social_score, action_score, nature_score))
#         except Exception as e:
#             logging.info("{} - Error at image {} - {}".format(user, i, e))
#             continue

#     profile_avg = profile_aggregation(img_profiles)
#     profile_owa = profile_aggregation(img_profiles, owa=True)
#     if debug:
#         logging.info("{} - Profile AVG\nsun chillout:\t\t{}\nknowledge travel:\t{}\nindependence history:\t{}\nculture indulgence:\t{}\nsocial sports:\t\t{}\naction fun:\t\t{}\nnature recration\t{}".format(user, *profile_avg))
#         logging.info("{} - Profile OWA\nsun chillout:\t\t{}\nknowledge travel:\t{}\nindependence history:\t{}\nculture indulgence:\t{}\nsocial sports:\t\t{}\naction fun:\t\t{}\nnature recration\t{}".format(user, *profile_owa))

#     return i, profile_avg, profile_owa


# # RECOMMEND AND HELPERS
# def vectorProfile(p):
#     return [p.f1, p.f2, p.f3, p.f4, p.f5, p.f6, p.f7]


# def recommend_for_profile(method, p):
#     rec_base = df.sample(frac=1).reset_index(drop=True)
#     sf = rec_base.iloc[:, 1:8]
#     tree = spatial.KDTree(sf.values)
#     nn = tree.query(p)
#     dist = nn[0]
#     rec_idx = nn[1]
#     rec = to_recommendation_dict(rec_base.iloc[rec_idx], method=method)
#     return rec, dist


# def all_recommendations(p_avg, p_owa, p_self):
#     rec_avg, rec_avg_dist = recommend_for_profile(
#         SIMPLE_AVERAGE, vectorProfile(p_avg))
#     rec_owa, rec_owa_dist = recommend_for_profile(
#         ORDERED_WEIGHTED_AVERAGE, vectorProfile(p_owa))
#     rec_self, rec_self_dist = recommend_for_profile(
#         SELF_ASSESSMENT, vectorProfile(p_self))
#     rec_random = rec_self
#     while rec_random["gid"] in [rec_avg["gid"], rec_owa["gid"], rec_self["gid"]]:
#         rec_random, rec_random_dist = recommend_for_profile(
#             RANDOM, list(np.random.rand(1, 7)[0]))
#     return [
#         {"rec": rec_avg, "dist": rec_avg_dist},
#         {"rec": rec_owa, "dist": rec_owa_dist},
#         {"rec": rec_self, "dist": rec_self_dist},
#         {"rec": rec_random, "dist": rec_random_dist}
#     ]


# def to_recommendation_dict(row, method):
#     return {
#         "method": method,
#         "gid": int(row.giatacityid),
#         "title": row.title,
#         "subtitle": row.subtitle,
#         "wiki_url": row.wiki_url,
#         "gtravel_url": row.gtravel_url,
#         "pic_num": int(row.pic_num)
#     }


# def build_recommendation(user_id, p_avg, p_owa, p_self):
#     all_rec = all_recommendations(p_avg, p_owa, p_self)
#     random.shuffle(all_rec)
#     recommendation = []
#     recommendation_gids = []
#     for m in all_rec:
#         r = m["rec"]
#         try:
#             position = 1 + recommendation_gids.index(r["gid"])
#             rec = Recommendation(
#                 user_id=user_id,
#                 method=r["method"],
#                 position=position,
#                 gid=r["gid"],
#                 distance=m["dist"],
#                 conflict=True
#             )
#             db.session.add(rec)
#             db.session.commit()
#         except:
#             recommendation_gids.append(r["gid"])
#             recommendation.append(r)
#             rec = Recommendation(
#                 user_id=user_id,
#                 method=r["method"],
#                 position=len(recommendation_gids),
#                 gid=r["gid"],
#                 distance=m["dist"],
#                 conflict=False
#             )
#             db.session.add(rec)
#     db.session.commit()
#     return recommendation


# REST API
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Welcome to Pic2Prof'


@app.route('/backend/selfassessment', methods=['POST'])
def selfassessment():
    if request.method == 'POST':
        # get or add user
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - SELFASSESSMENT REQUEST".format(user))
        # add selfassessment
        profile_self = Profile(
            user_id=user.id,
            method_id=SELF_ASSESSMENT,
            f1=(float(request.form['F1'])/100),
            f2=(float(request.form['F2'])/100),
            f3=(float(request.form['F3'])/100),
            f4=(float(request.form['F4'])/100),
            f5=(float(request.form['F5'])/100),
            f6=(float(request.form['F6'])/100),
            f7=(float(request.form['F7'])/100),
        )
        db.session.add(profile_self)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "persisted": True
        })


@app.route('/backend/time', methods=['POST'])
def time():
    if request.method == 'POST':
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - TIME REQUEST".format(user))
        t = Time(
            user_id=request.form["uuid"],
            step=request.form["step"]
        )
        db.session.add(t)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "persisted": True
        })


@app.route('/backend/display', methods=['POST'])
def display():
    if request.method == 'POST':
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - DISPLAY REQUEST".format(user))
        d = Display(
            user_id=request.form["uuid"],
            display=request.form["display"]
        )
        db.session.add(d)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "persisted": True
        })

@app.route('/backend/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    try:
        # get_location 호출
        try:
            location_name = get_location_by_coordinates(lat, lon)
            logging.info(f"Location fetched successfully: {location_name}")
        except Exception as e:
            logging.error(f"Failed to fetch location: {e}")
            location_name = None

        # get_weather 호출
        try:
            weather_data = get_weather_by_coordinates(lat, lon)
            if location_name:  # location_name이 성공적으로 가져온 경우, 한글명으로 업데이트
                weather_data['location']['name'] = location_name
            logging.info("Weather data fetched successfully.")
            return jsonify(weather_data)
        except Exception as e:
            logging.error(f"Failed to fetch weather data: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/backend/rank', methods=['POST'])
def rank():
    if request.method == 'POST':
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - RANK REQUEST".format(user))
        r = Rank(
            user_id=request.form["uuid"],
            oldIndex=request.form["oldIndex"],
            newIndex=request.form["newIndex"]
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "persisted": True
        })


@app.route('/backend/questions', methods=['POST'])
def questions():
    if request.method == 'POST':
        # get or add user
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - QUESTION ANSWER REQUEST".format(user))
        # add selfassessment
        questions = Questions(
            user_id=user.id,
            q1=request.form['Q1'],
            q2=request.form['Q2'],
            q3=request.form['Q3'],
            q4=request.form['Q4'],
            q5=request.form['Q5'],
            q6_1=request.form['Q6_1'],
            q6_2=request.form['Q6_2'],
            q6_3=request.form['Q6_3'],
            q6_4=request.form['Q6_4'],
            q6_5=request.form['Q6_5'],
            q6_6=request.form['Q6_6'],
            q6_7=request.form['Q6_7'],
            age=request.form['age'],
            gender=request.form['gender'],
            education=request.form['education'],
            travel_frequency=request.form['travel_frequency'],
            message=request.form['message']
        )
        db.session.add(questions)
        profile_self = Profile(
            user_id=user.id,
            method_id=SELF_ASSESSMENT,
            show=False,
            adjusted=request.form['adjusted'],
            f1=(float(request.form['F1'])/100),
            f2=(float(request.form['F2'])/100),
            f3=(float(request.form['F3'])/100),
            f4=(float(request.form['F4'])/100),
            f5=(float(request.form['F5'])/100),
            f6=(float(request.form['F6'])/100),
            f7=(float(request.form['F7'])/100),
        )
        db.session.add(profile_self)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "answers": True,
            "persisted": True
        })


@app.route('/backend/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # get or add user
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            user = User(id=request.form["uuid"])
            db.session.add(user)
        logging.info("{} - PREDICT REQUEST".format(user))
        # get and process files
        files = request.files.getlist("file[]")
        num_received = len(files)
        logging.info("{} - {} files received".format(user, num_received))
        num_processed, profile_avg, profile_owa = predict_seven_factors(
            files, debug=True, user=user)
        show_profile_avg = bool(random.getrandbits(1))
        p_avg = Profile(
            user_id=user.id,
            method_id=SIMPLE_AVERAGE,
            show=show_profile_avg,
            adjusted=False,
            f1=float(profile_avg[0]),
            f2=float(profile_avg[1]),
            f3=float(profile_avg[2]),
            f4=float(profile_avg[3]),
            f5=float(profile_avg[4]),
            f6=float(profile_avg[5]),
            f7=float(profile_avg[6]),
        )
        db.session.add(p_avg)
        p_owa = Profile(
            user_id=user.id,
            method_id=ORDERED_WEIGHTED_AVERAGE,
            show=(not show_profile_avg),
            adjusted=False,
            f1=float(profile_owa[0]),
            f2=float(profile_owa[1]),
            f3=float(profile_owa[2]),
            f4=float(profile_owa[3]),
            f5=float(profile_owa[4]),
            f6=float(profile_owa[5]),
            f7=float(profile_owa[6]),
        )
        db.session.add(p_owa)
        db.session.commit()
        if(show_profile_avg):
            profile = profile_avg
        else:
            profile = profile_owa
        return jsonify({
            "num_received": num_received,
            "num_processed": num_processed,
            "F1": int(profile[0]*100),
            "F2": int(profile[1]*100),
            "F3": int(profile[2]*100),
            "F4": int(profile[3]*100),
            "F5": int(profile[4]*100),
            "F6": int(profile[5]*100),
            "F7": int(profile[6]*100)
        })


@app.route('/backend/recommend', methods=['GET'])
def recommend():
    if request.method == 'GET':
        user_id = request.args.get('uuid')#request.form["uuid"]
        profile_avg = Profile.query.filter_by(user_id=user_id, method_id=SIMPLE_AVERAGE).first()
        profile_owa = Profile.query.filter_by(user_id=user_id, method_id=ORDERED_WEIGHTED_AVERAGE).first()
        profile_self = Profile.query.filter_by(user_id=user_id, method_id=SELF_ASSESSMENT).first()
        if (profile_avg is None) or (profile_owa is None) or (profile_self is None):
            logging.exception('Profile for recommendation not found')
            return """
            No profile for recommendation found! Please, restart User Study by freshly opening the webpage in another window/tab.
            """, 404
        logging.info("{} - RECOMMENDATION REQUEST".format(user_id))
        recommendation = build_recommendation(user_id, profile_avg, profile_owa, profile_self)
        return jsonify(recommendation)


@app.route('/backend/finish', methods=['POST'])
def finihs():
    if request.method == 'POST':
        # get or add user
        user = User.query.filter_by(id=request.form["uuid"]).first()
        if user is None:
            logging.exception('No User for recommendation selection found')
            return """
            Selection Received, but no User with that UUID found!
            """, 404
        logging.info("{} - SELECTION REQUEST".format(user))
        # add selfassessment
        users_selection = User_Selection(
            user_id=request.form['uuid'],
            position=request.form['position'],
            gid=request.form['gid']
        )
        db.session.add(users_selection)
        pictureInteractionCounts = request.form.getlist("pictureInteractionCounts[]")
        print(pictureInteractionCounts)
        for index, item in enumerate(pictureInteractionCounts):
            p = PictureInteraction(
                user_id=request.form['uuid'],
                position=index+1,
                count=int(item)
            )
            db.session.add(p)
        wikiInteractionFlag = request.form.getlist("wikiInteractionFlag[]")
        gtravelInteractionFlag = request.form.getlist("gtravelInteractionFlag[]")
        print(wikiInteractionFlag)
        print(gtravelInteractionFlag)
        for index, item in enumerate(wikiInteractionFlag):
            inf = InformationInteraction(
                user_id=request.form['uuid'],
                position=index+1,
                wiki=bool(wikiInteractionFlag[index]),
                gtravel=bool(gtravelInteractionFlag[index])
            )
            db.session.add(inf)
        db.session.commit()
        return jsonify({
            "uuid": user.id,
            "persisted": True
        })


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
