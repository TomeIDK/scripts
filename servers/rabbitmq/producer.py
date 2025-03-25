import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, "vhost", pika.PlainCredentials("user", "password")))
channel = connection.channel()


exchanges = [
    'user-management', 'event', 'session', 'sale', 'invoice',
    'monitoring', 'dlx'
]

queues = {
    'pos': ['user', 'event', 'dlq', 'retry'],
    'crm': ['user', 'event', 'session', 'sale', 'invoice', 'dlq', 'retry'],
    'billing': ['user', 'invoice', 'sale', 'dlq', 'retry'],
    'planning': ['user', 'event', 'session', 'dlq', 'retry'],
    'mailing': ['mail', 'dlq', 'retry'],
    'monitoring': ['log', 'success', 'failure', 'heartbeat', 'dlq', 'retry'],
    'frontend': ['user', 'invoice', 'session', 'event', 'dlq', 'retry']
}

routing_keys = {
    'user-management': ['user.register', 'user.update', 'user.delete'],
    'event': ['event.register', 'event.update', 'event.unregister', 'event.cancel', 'event.finished'],
    'session': ['session.register', 'session.unregister', 'session.create', 'session.cancel', 'session.delay', 'session.update'],
    'sale': ['sale.performed'],
    'invoice': ['invoice.payed', 'invoice.send', 'invoice.create', 'invoice.delete'],
    'monitoring': ['monitoring.failure', 'monitoring.report', 'monitoring.success', 'monitoring.heartbeat'],
    'dlx': ['dlq.pos.#', 'dlq.crm.#', 'dlq.billing.#', 'dlq.planning.#', 'dlq.mailing.#', 'dlq.monitoring.#', 'retry.pos.#', 'retry.crm.#', 'retry.billing.#', 'retry.planning.#', 'retry.mailing.#', 'retry.monitoring.#'],
}


def test_publish(exchange, routing_key):
    try:
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=f"Test message to {exchange} with routing key {routing_key}"
        )
        print(f" [x] Successfully sent to {exchange} with routing key {routing_key}")
    except Exception as e:
        print(f" [!] Failed to send to {exchange} with routing key {routing_key}: {e}")


for exchange in exchanges:
    for routing_key in routing_keys.get(exchange, []):
        test_publish(exchange, routing_key)


connection.close()
