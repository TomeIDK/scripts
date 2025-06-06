import os
import sys
from pathlib import Path
import pika
from dotenv import load_dotenv

# parameters
# port (optional): AMQP port you want to execute the configuration for
# => defaults to .env RABBITMQ_PORT if none provided

# usage
# 1. connects to a rabbitmq server with provided .env variables
# 2. adds set exchanges, queues, routing keys

env_path = Path(__file__).resolve().parent/ ".env"
load_dotenv(dotenv_path=env_path)

if len(sys.argv) > 1:
    port = sys.argv[1]
    print(f"Port provided: {port}")
else:
    port = os.getenv("RABBITMQ_PORT")
    print(f"No port provided, defaulting to port {port}.")

print("Creating exchanges, queues and routing keys...")

connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"), port, os.getenv("RABBITMQ_VHOST"), pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))))
channel = connection.channel()


#############
# EXCHANGES #
#############
channel.exchange_declare(exchange='user-management', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='company', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='event', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='session', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='sale', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='invoice', exchange_type='direct', durable=True)

channel.exchange_declare(exchange='monitoring', exchange_type='topic', durable=True)
channel.exchange_declare(exchange='dlx', exchange_type='topic', durable=True)


##################
# POINT OF SALES #
##################
channel.queue_declare(queue='pos.user', durable=True)
channel.queue_bind(queue="pos.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="pos.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="pos.user", exchange="user-management", routing_key="user.delete")

channel.queue_declare(queue='pos.company', durable=True)
channel.queue_bind(queue="pos.company", exchange="company", routing_key="company.create")
channel.queue_bind(queue="pos.company", exchange="company", routing_key="company.update")
channel.queue_bind(queue="pos.company", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="pos.company", exchange="company", routing_key="company.register")
channel.queue_bind(queue="pos.company", exchange="company", routing_key="company.unregister")

channel.queue_declare(queue='pos.event', durable=True)
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.register")
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.create")
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.update")
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="pos.event", exchange="event", routing_key="event.finished")

channel.queue_declare(queue='pos.dlq', durable=True)
channel.queue_bind(queue="pos.dlq", exchange="dlx", routing_key="dlq.pos.#")

channel.queue_declare(queue='pos.retry', durable=True)
channel.queue_bind(queue="pos.retry", exchange="dlx", routing_key="retry.pos.#")



#######
# CRM #
#######
channel.queue_declare(queue='crm.user', durable=True)
channel.queue_bind(queue="crm.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="crm.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="crm.user", exchange="user-management", routing_key="user.delete")

channel.queue_declare(queue='crm.company', durable=True)
channel.queue_bind(queue="crm.company", exchange="company", routing_key="company.create")
channel.queue_bind(queue="crm.company", exchange="company", routing_key="company.update")
channel.queue_bind(queue="crm.company", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="crm.company", exchange="company", routing_key="company.register")
channel.queue_bind(queue="crm.company", exchange="company", routing_key="company.unregister")

channel.queue_declare(queue='crm.event', durable=True)
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.register")
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.create")
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.update")
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="crm.event", exchange="event", routing_key="event.finished")


channel.queue_declare(queue='crm.session', durable=True)
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.register")
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.unregister")
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.create")
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.delete")
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.delay")
channel.queue_bind(queue="crm.session", exchange="session", routing_key="session.update")

channel.queue_declare(queue='crm.sale', durable=True)
channel.queue_bind(queue="crm.sale", exchange="sale", routing_key="sale.performed")

channel.queue_declare(queue='crm.invoice', durable=True)
channel.queue_bind(queue="crm.invoice", exchange="invoice", routing_key="invoice.payed")


channel.queue_declare(queue='crm.dlq', durable=True)
channel.queue_bind(queue="crm.dlq", exchange="dlx", routing_key="dlq.crm.#")

channel.queue_declare(queue='crm.retry', durable=True)
channel.queue_bind(queue="crm.retry", exchange="dlx", routing_key="retry.crm.#")



###########
# BILLING #
###########
channel.queue_declare(queue='billing.user', durable=True)
channel.queue_bind(queue="billing.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="billing.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="billing.user", exchange="user-management", routing_key="user.delete")

channel.queue_declare(queue='billing.company', durable=True)
channel.queue_bind(queue="billing.company", exchange="company", routing_key="company.create")
channel.queue_bind(queue="billing.company", exchange="company", routing_key="company.update")
channel.queue_bind(queue="billing.company", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="billing.company", exchange="company", routing_key="company.register")
channel.queue_bind(queue="billing.company", exchange="company", routing_key="company.unregister")

channel.queue_declare(queue='billing.event', durable=True)
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.register")
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.create")
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.update")
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="billing.event", exchange="event", routing_key="event.finished")

channel.queue_declare(queue='billing.invoice', durable=True)
channel.queue_bind(queue="billing.invoice", exchange="invoice", routing_key="invoice.payed")

channel.queue_declare(queue='billing.sale', durable=True)
channel.queue_bind(queue="billing.sale", exchange="sale", routing_key="sale.performed")

channel.queue_declare(queue='billing.dlq', durable=True)
channel.queue_bind(queue="billing.dlq", exchange="dlx", routing_key="dlq.billing.#")

channel.queue_declare(queue='billing.retry', durable=True)
channel.queue_bind(queue="billing.retry", exchange="dlx", routing_key="retry.billing.#")



############
# PLANNING #
############
channel.queue_declare(queue='planning.user', durable=True)
channel.queue_bind(queue="planning.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="planning.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="planning.user", exchange="user-management", routing_key="user.delete")

channel.queue_declare(queue='planning.company', durable=True)
channel.queue_bind(queue="planning.company", exchange="company", routing_key="company.create")
channel.queue_bind(queue="planning.company", exchange="company", routing_key="company.update")
channel.queue_bind(queue="planning.company", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="planning.company", exchange="company", routing_key="company.register")
channel.queue_bind(queue="planning.company", exchange="company", routing_key="company.unregister")

channel.queue_declare(queue='planning.event', durable=True)
channel.queue_bind(queue="planning.event", exchange="event", routing_key="event.register")
channel.queue_bind(queue="planning.event", exchange="event", routing_key="event.update")
channel.queue_bind(queue="planning.event", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="planning.event", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="planning.event", exchange="event", routing_key="event.finished")

channel.queue_declare(queue='planning.session', durable=True)
channel.queue_bind(queue="planning.session", exchange="session", routing_key="session.register")
channel.queue_bind(queue="planning.session", exchange="session", routing_key="session.unregister")

channel.queue_declare(queue='planning.dlq', durable=True)
channel.queue_bind(queue="planning.dlq", exchange="dlx", routing_key="dlq.planning.#")

channel.queue_declare(queue='planning.retry', durable=True)
channel.queue_bind(queue="planning.retry", exchange="dlx", routing_key="retry.planning.#")


###########
# MAILING #
###########
channel.queue_declare(queue='mailing.user', durable=True)
channel.queue_bind(queue="mailing.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="mailing.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="mailing.user", exchange="user-management", routing_key="user.delete")



channel.queue_declare(queue='mailing.mail', durable=True)
channel.queue_bind(queue="mailing.mail", exchange="user-management", routing_key="user.passwordGenerated")
channel.queue_bind(queue="mailing.mail", exchange="user-management", routing_key="user.passwordReset")
channel.queue_bind(queue="mailing.mail", exchange="company", routing_key="company.create")
channel.queue_bind(queue="mailing.mail", exchange="company", routing_key="company.update")
channel.queue_bind(queue="mailing.mail", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="mailing.mail", exchange="company", routing_key="company.register")
channel.queue_bind(queue="mailing.mail", exchange="company", routing_key="company.unregister")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.register")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.create")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.update")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.finished")
channel.queue_bind(queue="mailing.mail", exchange="event", routing_key="event.mailingList")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.register")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.unregister")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.update")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.delete")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.delay")
channel.queue_bind(queue="mailing.mail", exchange="session", routing_key="session.create")
channel.queue_bind(queue="mailing.mail", exchange="invoice", routing_key="invoice.send")
channel.queue_bind(queue="mailing.mail", exchange="monitoring", routing_key="monitoring.failure")
channel.queue_bind(queue="mailing.mail", exchange="monitoring", routing_key="monitoring.report")

channel.queue_declare(queue='mailing.dlq', durable=True)
channel.queue_bind(queue="mailing.dlq", exchange="dlx", routing_key="dlq.mailing.#")

channel.queue_declare(queue='mailing.retry', durable=True)
channel.queue_bind(queue="mailing.retry", exchange="dlx", routing_key="retry.mailing.#")



##############
# MONITORING #
##############
channel.queue_declare(queue='monitoring.log', durable=True)
channel.queue_bind(queue="monitoring.log", exchange="user-management", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="company", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="session", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="event", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="sale", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="invoice", routing_key="#")
channel.queue_bind(queue="monitoring.log", exchange="dlx", routing_key="#")

channel.queue_declare(queue='monitoring.success', durable=True)
channel.queue_bind(queue="monitoring.success", exchange="monitoring", routing_key="monitoring.success")

channel.queue_declare(queue='monitoring.failure', durable=True)
channel.queue_bind(queue="monitoring.failure", exchange="monitoring", routing_key="monitoring.failure")

channel.queue_declare(queue='monitoring.heartbeat', durable=True)
channel.queue_bind(queue="monitoring.heartbeat", exchange="monitoring", routing_key="monitoring.heartbeat")

channel.queue_declare(queue='monitoring.dlq', durable=True)
channel.queue_bind(queue="monitoring.dlq", exchange="dlx", routing_key="dlq.monitoring.#")

channel.queue_declare(queue='monitoring.retry', durable=True)
channel.queue_bind(queue="monitoring.retry", exchange="dlx", routing_key="retry.monitoring.#")



############
# FRONTEND #
############
channel.queue_declare(queue='frontend.user', durable=True)
channel.queue_bind(queue="frontend.user", exchange="user-management", routing_key="user.register")
channel.queue_bind(queue="frontend.user", exchange="user-management", routing_key="user.unregister")
channel.queue_bind(queue="frontend.user", exchange="user-management", routing_key="user.update")
channel.queue_bind(queue="frontend.user", exchange="user-management", routing_key="user.delete")

channel.queue_declare(queue='frontend.company', durable=True)
channel.queue_bind(queue="frontend.company", exchange="company", routing_key="company.create")
channel.queue_bind(queue="frontend.company", exchange="company", routing_key="company.update")
channel.queue_bind(queue="frontend.company", exchange="company", routing_key="company.delete")
channel.queue_bind(queue="frontend.company", exchange="company", routing_key="company.register")
channel.queue_bind(queue="frontend.company", exchange="company", routing_key="company.unregister")

channel.queue_declare(queue='frontend.invoice', durable=True)
channel.queue_bind(queue="frontend.invoice", exchange="invoice", routing_key="invoice.create")
channel.queue_bind(queue="frontend.invoice", exchange="invoice", routing_key="invoice.payed")
channel.queue_bind(queue="frontend.invoice", exchange="invoice", routing_key="invoice.delete")

channel.queue_declare(queue='frontend.session', durable=True)
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.register")
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.unregister")
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.create")
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.delete")
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.update")
channel.queue_bind(queue="frontend.session", exchange="session", routing_key="session.delay")

channel.queue_declare(queue='frontend.event', durable=True)
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.register")
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.unregister")
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.create")
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.delete")
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.update")
channel.queue_bind(queue="frontend.event", exchange="event", routing_key="event.finished")

channel.queue_declare(queue='frontend.sale', durable=True)
channel.queue_bind(queue="frontend.sale", exchange="sale", routing_key="sale.performed")

channel.queue_declare(queue='frontend.dlq', durable=True)
channel.queue_bind(queue="frontend.dlq", exchange="dlx", routing_key="dlq.frontend.#")

channel.queue_declare(queue='frontend.retry', durable=True)
channel.queue_bind(queue="frontend.retry", exchange="dlx", routing_key="retry.frontend.#")

connection.close()

print("Finished!")