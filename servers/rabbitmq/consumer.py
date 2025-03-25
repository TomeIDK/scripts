import pika

# Establish connection
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


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


for queue in queues:
    for x in range(len(queues[queue])):
        try:
            channel.basic_consume(
                queue=f"{queue}.{queues[queue][x]}",
                on_message_callback=callback,
                auto_ack=True
            )
            print(f" [*] Waiting for messages from {queue}.{queues[queue][x]}. To exit press CTRL+C")
        except Exception as e:
            print(f" [!] Failed to consume from {queue}.{queues[queue][x]}: {e}")


channel.start_consuming()
