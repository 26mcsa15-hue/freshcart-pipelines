import json, os, random, time, uuid
from datetime import datetime, timezone
import pika

URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
BAD_EVERY = int(os.getenv("BAD_EVERY", "10"))   # 0 = never send a bad message
ZONES = {"bangalore": ["koramangala", "indiranagar", "whitefield"],
         "chennai": ["tnagar", "whitefield"]}

conn = pika.BlockingConnection(pika.URLParameters(URL))
ch = conn.channel()
ch.exchange_declare(exchange="rapido-dispatch", exchange_type="topic")

n = 0
while True:
    n += 1
    city = random.choice(list(ZONES))
    zone = random.choice(ZONES[city])
    kind = random.choice(["ride", "food"])
    key = f"{city}.{zone}.{kind}"
    if n == 5:                                   # one extra test for D1 question 6
        city, zone, key = "bangalore", "koramangala", "bangalore.koramangala"
    msg = {"id": str(uuid.uuid4()), "city": city, "zone": zone, "type": kind,
           "ts": datetime.now(timezone.utc).isoformat()}
    if BAD_EVERY and n % BAD_EVERY == 0:         # D3: bad message, no zone field
        del msg["zone"]
    ch.basic_publish(exchange="rapido-dispatch", routing_key=key, body=json.dumps(msg))
    print(f"sent #{n} key={key} id={msg['id'][:8]}", flush=True)
    time.sleep(2)
