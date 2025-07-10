import paho.mqtt.client as mqtt
import json
import time
import random

# --- Konfigurasi MQTT Broker ---
BROKER_ADDRESS = "broker.emqx.io"
PORT = 1883  # Menggunakan TCP Port
TOPIC = "boey2025-kirei/beoy-dumy-001"
CLIENT_ID = f"python-mqtt-subscriber-{random.randint(0, 1000)}" # ID klien unik

# --- Callback Functions untuk MQTT Client ---

def on_connect(client, userdata, flags, rc):
    """
    Fungsi callback yang dipanggil saat klien berhasil terhubung ke broker.
    """
    if rc == 0:
        print(f"[{time.strftime('%H:%M:%S')}] Connected successfully to MQTT Broker!")
        # Berlangganan topik setelah koneksi berhasil
        client.subscribe(TOPIC)
        print(f"[{time.strftime('%H:%M:%S')}] Subscribed to topic: {TOPIC}")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """
    Fungsi callback yang dipanggil saat ada pesan diterima dari broker.
    """
    print(f"\n--- [{time.strftime('%H:%M:%S')}] Message Received ---")
    print(f"Topic: {msg.topic}")
    print(f"Payload (RAW): {msg.payload.decode()}") # Decode byte payload ke string

    try:
        # Mengurai payload JSON
        data = json.loads(msg.payload.decode('utf-8'))

        print("\n--- Parsed Sensor Data ---")
        print(f"Timestamp: {data.get('timestamp', 'N/A')}")
        print(f"Sensor ID: {data.get('sensor_id', 'N/A')}")
        print(f"pH: {data.get('ph', 'N/A')}")
        print(f"Turbidity (NTU): {data.get('turbidity_ntu', 'N/A')}")
        print(f"Dissolved Oxygen (mg/L): {data.get('do_mg_l', 'N/A')}")
        print(f"Electrical Conductivity (uS/cm): {data.get('ec_us_cm', 'N/A')}")
        print(f"Temperature (C): {data.get('temperature_c', 'N/A')}")

        # Mengurai dan menampilkan data geolokasi
        geolocation = data.get('geolocation')
        if geolocation and isinstance(geolocation, list) and len(geolocation) == 2:
            latitude, longitude = geolocation
            print(f"Geolocation: Latitude={latitude}, Longitude={longitude}")
        else:
            print("Geolocation: N/A or Invalid Format")

    except json.JSONDecodeError:
        print(f"[{time.strftime('%H:%M:%S')}] Error: Could not decode JSON payload.")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] An error occurred while processing message: {e}")

def on_disconnect(client, userdata, rc):
    """
    Fungsi callback yang dipanggil saat klien terputus dari broker.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Disconnected with result code {rc}")

# --- Main Program ---
if __name__ == "__main__":
    # Inisialisasi MQTT Client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message # Menentukan fungsi untuk menangani pesan
    client.on_disconnect = on_disconnect

    # Menghubungkan ke Broker
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Connecting to broker: {BROKER_ADDRESS}:{PORT}...")
        client.connect(BROKER_ADDRESS, PORT, 60) # Keep-alive interval 60 detik
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Connection failed: {e}")
        exit(1)

    # Memulai loop jaringan di background
    # Loop ini akan terus mendengarkan pesan masuk
    print(f"[{time.strftime('%H:%M:%S')}] Starting MQTT loop... Press Ctrl+C to exit.")
    client.loop_forever() # Loop selamanya sampai diinterupsi (Ctrl+C)

    # Kode di bawah ini hanya akan dieksekusi setelah loop_forever berhenti
    print(f"[{time.strftime('%H:%M:%S')}] Loop stopped. Disconnecting from MQTT Broker.")
    client.disconnect()