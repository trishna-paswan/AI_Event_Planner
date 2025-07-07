# 4. face_recognition_utils.py
import face_recognition
import os
from models import User


def verify_face(user_id, uploaded_path):
    user = User.query.get(user_id)
    if not user or not user.face_image:
        return False
        

    try:
        stored_image_path = os.path.join('uploads', user.face_image)
        known_image = face_recognition.load_image_file(stored_image_path)
        unknown_image = face_recognition.load_image_file(uploaded_path)

        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return results[0]
    except Exception as e:
        print(f"Face recognition error: {e}")
        return False
