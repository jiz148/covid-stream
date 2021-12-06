from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime


def publish_message(producer_instance, topic_name, key, value):
    print("entered into function")
    try:
        print("entered into try block")
        
        key_bytes = bytes(key, encoding='ascii')
        print("converted key into bytes")
        
        value_bytes = bytes(str(value),encoding='ascii')
        print("converted value into bytes")
        
        print("\n key bytes are ",key_bytes)
        print("\n value bytes are ",value_bytes)
        #producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print("Message published successfully with key = ",key,", value = ",value)

    except Exception as ex:
        print("Error in publishing message")
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        #_producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))

    except Exception as ex:
        print("Exception while connecting Kafka")
        print(str(ex))

    finally:
        return _producer



def produce():
    kafka_producer = connect_kafka_producer()

    #generating key
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
    key = 'new_data_at_'+dt_string

    print("The key being passed is",key)


    #test value
    value = {'res_state': 'CA', 'sex': 'male'}
    print("\n the value being passed is ",value)
    print("type of value is ",type(value))

    print("\n before function")
    publish_message(kafka_producer, 'new-data', key, value)
    print("\n after function")


if __name__ == "__main__":
    produce()
             
    
    

    
    
        

