from kafka import KafkaConsumer
#from .Users.anandkumarpola.Documents.G3.RUTGERS.543.Project2.covid-stream.backend.backend_app import _add_to_db
import sys
sys.path.append('/Users/anandkumarpola/Documents/G3/RUTGERS/543/Project2/covid-stream/backend')
import backend_app

def consumer():
    print("\n entered consumer function")
    try:
        print("\n creating consumer")
        _consumer = KafkaConsumer('new-data',bootstrap_servers=['localhost:9092'])
        print("\n consumer is created")

    except Exception as ex:
        print("Error in creating consumer")
        print(str(ex))

    try:
        print("\n Reading messages....")
        cnt = 1
        for message in _consumer:
            print("Reading message",cnt)
            temp = message.value

            _dict = eval(temp)
            print("the new record dictonary is ",_dict)

            print("Adding dictionary to the data base")
            backend_app._add_to_db(_dict)
            print("Data added successfully")

            
            #print("message value is ",temp," type is ",type(temp))
            #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          #message.offset, message.key,
                                          #message.value))
            cnt = cnt+1

        print("\n reading msgs done")

    except Exception as ex:
        print("Error in reading messages")
        print(str(ex))

        
if __name__ == '__main__':
    print("start")
    consumer()
    print("end")
