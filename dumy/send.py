import paho.mqtt.client as mqtt
import time
import json
import random

# --- Konfigurasi MQTT Broker ---
BROKER_ADDRESS = "broker.emqx.io"
PORT = 1883  # Menggunakan TCP Port
TOPIC = "boey2025-kirei/beoy-dumy-001"
CLIENT_ID = f"python-mqtt-client-{random.randint(0, 1000)}" # ID klien unik

# --- Konfigurasi Data Dummy ---
# Nilai awal geolokasi (sekitar Bandung, Jawa Barat)
initial_latitude = -6.917464
initial_longitude = 107.619125
latitude_offset = 0.0001 # Pergeseran kecil setiap kali kirim
longitude_offset = 0.0001 # Pergeseran kecil setiap kali kirim

# Fungsi untuk menghasilkan data sensor dummy dinamis
def generate_dummy_sensor_data():
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_id": "water-sensor-001",
        "ph": round(random.uniform(6.5, 8.5), 2),  # pH air (sedikit asam hingga basa)
        "turbidity_ntu": round(random.uniform(5, 50), 1), # Kekeruhan (NTU)
        "do_mg_l": round(random.uniform(4.0, 9.0), 2), # Dissolved Oxygen (mg/L)
        "ec_us_cm": round(random.uniform(100, 1000), 0), # Electrical Conductivity (uS/cm)
        "temperature_c": round(random.uniform(20.0, 30.0), 1) # Suhu air (Celcius)
    }
    return data

# --- Callback Functions untuk MQTT Client ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{time.strftime('%H:%M:%S')}] Connected successfully to MQTT Broker!")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Failed to connect, return code {rc}\n")

def on_publish(client, userdata, mid):
    print(f"[{time.strftime('%H:%M:%S')}] Data published. MID: {mid}")

def on_disconnect(client, userdata, rc):
    print(f"[{time.strftime('%H:%M:%S')}] Disconnected with result code {rc}")

# --- Main Program ---
if __name__ == "__main__":
    # Inisialisasi MQTT Client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Menghubungkan ke Broker
    try:
        client.connect(BROKER_ADDRESS, PORT, 60) # Keep-alive interval 60 detik
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Connection failed: {e}")
        exit(1)

    # Memulai loop jaringan di background
    client.loop_start()

    current_latitude = initial_latitude
    current_longitude = initial_longitude

    try:
        while True:
            # Generate data sensor
            sensor_data = generate_dummy_sensor_data()

            # Perbarui geolokasi dummy secara dinamis
            current_latitude += random.uniform(-latitude_offset, latitude_offset)
            current_longitude += random.uniform(-longitude_offset, longitude_offset)

            # Batasi desimal untuk geolokasi agar tidak terlalu panjang
            current_latitude = round(current_latitude, 6)
            current_longitude = round(current_longitude, 6)

            # Tambahkan data geolokasi sebagai array [latitude, longitude]
            sensor_data["geolocation"] = [current_latitude, current_longitude]

            # Konversi data ke format JSON string
            payload = json.dumps(sensor_data)

            # Kirim data ke broker
            print(f"[{time.strftime('%H:%M:%S')}] Publishing: {payload} to topic: {TOPIC}")
            client.publish(TOPIC, payload)

            time.sleep(5) # Kirim data setiap 5 detik

    except KeyboardInterrupt:
        print("\nStopping data transmission...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.loop_stop() # Hentikan loop jaringan
        client.disconnect() # Putuskan koneksi dari broker
        print("Disconnected from MQTT Broker.")