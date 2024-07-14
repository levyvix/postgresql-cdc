from rich import print

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9093"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)

# print(consumer.topics())

consumer.subscribe(
    [
        "cdc-.sales.orders",
    ]  # "cdc.sales.products", "cdc.sales.orders"]
)

for m in consumer:
    print(m.topic, m.value)
