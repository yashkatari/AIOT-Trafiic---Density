import cv2
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Google Sheets setup
SCOPES =
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)
SAMPLE_SPREADSHEET_ID = 

# Get next available row
def get_next_available_row(sheet):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A:B").execute()
    numRows = len(result.get('values', []))
    return numRows + 1

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Timing config
initial_delay = 5   # Wait 5 seconds before first update
update_interval = 8 # Send data every 8 seconds
start_time = time.time()
last_sent_time = None
face_count_to_send = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error accessing webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    face_count = len(faces)

    # Update face count to send (overwrite each frame during interval)
    face_count_to_send = face_count

    # Draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Overlay text
    cv2.putText(frame, f'Density: {face_count}', (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, 'Press Q to Quit', (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Live Face Detection', frame)

    current_time = time.time()

    # After initial delay, update every 8 seconds
    if current_time - start_time >= initial_delay:
        if last_sent_time is None or (current_time - last_sent_time >= update_interval):
            current_time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            data_to_send = [[current_time_str, face_count_to_send]]

            next_row = get_next_available_row(service.spreadsheets())
            service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=f"Sheet1!A{next_row}:B{next_row}",
                valueInputOption="USER_ENTERED",
                body={"values": data_to_send}
            ).execute()

            print("✅ Sent to Google Sheets:", data_to_send)
            last_sent_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

