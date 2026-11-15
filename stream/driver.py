import json, os, sys
import pika

name, pattern = sys.argv[1], sys.argv[2]
URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
conn = pika.BlockingConnection(pika.URLParameters(URL))
ch = conn.channel()
ch.exchange_declare(exchange="rapido-dispatch", exchange_type="topic")
q = ch.queue_declare(queue="", exclusive=True).method.queue
ch.queue_bind(exchange="rapido-dispatch", queue=q, routing_key=pattern)
ch.basic_qos(prefetch_count=1)

def on_message(ch, method, props, body):
    msg = json.loads(body)
    if "zone" not in msg:                       # bad message
        print(f"[{name}] REJECTED key={method.routing_key} id={msg['id'][:8]}", flush=True)
        ch.basic_nack(method.delivery_tag, requeue=False)
        return
    print(f"[{name}] received key={method.routing_key} id={msg['id'][:8]}", flush=True)
    ch.basic_ack(method.delivery_tag)

ch.basic_consume(queue=q, on_message_callback=on_message)
print(f"[{name}] bound to {pattern}", flush=True)
ch.start_consuming()
