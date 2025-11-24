import cv2
import mediapipe as mp
import requests  # ✅ Needed to send answer to Flask

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Start webcam
cap = cv2.VideoCapture(0)

NOSE_TIP = 1
box_width = 100
box_height = 100
box_color = (255, 0, 0)

gesture_detected = False
ref_center_x, ref_center_y = None, None

def get_direction(nose_x, nose_y, box_x1, box_y1, box_x2, box_y2):
    if nose_y < box_y1:
        return 'A'  # Up
    elif nose_y > box_y2:
        return 'B'  # Down
    elif nose_x > box_x2:
        return 'C'  # Right
    elif nose_x < box_x1:
        return 'D'  # Left
    return None

def is_inside_box(nose_x, nose_y, box_x1, box_y1, box_x2, box_y2):
    return box_x1 <= nose_x <= box_x2 and box_y1 <= nose_y <= box_y2

print("📦 Center your nose inside the box to begin.")
print("👉 Move your head to answer. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if ref_center_x is None:
        ref_center_x = w // 2
        ref_center_y = h // 2

    box_x1 = ref_center_x - box_width // 2
    box_y1 = ref_center_y - box_height // 2
    box_x2 = ref_center_x + box_width // 2
    box_y2 = ref_center_y + box_height // 2

    # Draw fixed box
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), box_color, 2)
    cv2.putText(frame, "Neutral Zone", (box_x1, box_y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

    # 🆕 Draw directional labels
    cv2.putText(frame, "A", ((box_x1 + box_x2)//2 - 10, box_y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)  # Top
    cv2.putText(frame, "B", ((box_x1 + box_x2)//2 - 10, box_y2 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)  # Bottom
    cv2.putText(frame, "C", (box_x2 + 10, (box_y1 + box_y2)//2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)  # Right
    cv2.putText(frame, "D", (box_x1 - 30, (box_y1 + box_y2)//2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)  # Left

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose_tip = face_landmarks.landmark[NOSE_TIP]
            nose_x = int(nose_tip.x * w)
            nose_y = int(nose_tip.y * h)

            # Draw circle on nose
            cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)

            if not gesture_detected:
                if not is_inside_box(nose_x, nose_y, box_x1, box_y1, box_x2, box_y2):
                    direction = get_direction(nose_x, nose_y, box_x1, box_y1, box_x2, box_y2)
                    if direction:
                        print(f"\n✅ Answer Given: {direction}")
                        try:
                            # ✅ Fixed endpoint
                            requests.post('http://127.0.0.1:5000/post_gesture', json={'gesture': direction})
                        except Exception as e:
                            print("❌ Failed to send answer:", e)

                        gesture_detected = True
                        print("🕓 Waiting to return to the box...")
            else:
                if is_inside_box(nose_x, nose_y, box_x1, box_y1, box_x2, box_y2):
                    gesture_detected = False
                    print("🟢 Back to neutral. Give next answer...")

    cv2.imshow("Facial Input System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
