from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.decorators import dag, task
import maadstml 
import sys
import tsslogging
import os

sys.dont_write_bytecode = True

######################################## USER CHOOSEN PARAMETERS ########################################
default_args = {
 'owner' : 'Sebastian Maurice', # <<< ********** You change as needed
 'companyname': 'Otics',  # <<< ********** You change as needed
  'myname' : 'Sebastian',  # <<< ********** You change as needed
  'myemail' : 'Sebastian.Maurice',  # <<< ********** You change as needed
  'mylocation' : 'Toronto',  # <<< ********** You change as needed
  'replication' : '1',  # <<< ********** You change as needed
  'numpartitions': '1',  # <<< ********** You change as needed
  'enabletls': '1',  # <<< ********** You change as needed
  'brokerhost' : '',  # <<< ********** Leave as is
  'brokerport' : '-999',  # <<< ********** Leave as is
  'microserviceid' : '',  # <<< ********** You change as needed
  'raw_data_topic' : 'iot-raw-data', # Separate multiple topics with comma <<< ********** You change topic names as needed
  'preprocess_data_topic' : 'iot-preprocess-data,iot-preprocess2-data', # Separate multiple topics with comma <<< ********** You change topic names as needed
  'ml_data_topic' : 'ml-data', # Separate multiple topics with comma <<< ********** You change topic names as needed
  'prediction_data_topic' : 'prediction-data', # Separate multiple topics with comma <<< ********** You change topic names as needed
  'description' : 'Topics to store iot data',      
}

######################################## DO NOT MODIFY BELOW #############################################

# Instantiate your DAG
@dag(dag_id="tml_system_step_2_kafka_createtopic_dag_myawesometmlsolution3", default_args=default_args, tags=["tml_system_step_2_kafka_createtopic_dag_myawesometmlsolution3"], start_date=datetime(2023, 1, 1), schedule=None,catchup=False)
def startkafkasetup():
    def empty():
        pass
dag = startkafkasetup()

def setupkafkatopics(**context):
 # Set personal data
  args = default_args
  companyname=args['companyname']
  myname=args['myname']
  myemail=args['myemail']
  mylocation=args['mylocation']
  description=args['description']  

  # Replication factor for Kafka redundancy
  replication=int(args['replication'])
  # Number of partitions for joined topic
  numpartitions=int(args['numpartitions'])
  # Enable SSL/TLS communication with Kafka
  enabletls=int(args['enabletls'])
  # If brokerhost is empty then this function will use the brokerhost address in your
  brokerhost=args['brokerhost']
  # If this is -999 then this function uses the port address for Kafka in VIPER.ENV in the
  # field 'KAFKA_CONNECT_BOOTSTRAP_SERVERS'
  brokerport=int(args['brokerport'])
  # If you are using a reverse proxy to reach VIPER then you can put it here - otherwise if
  # empty then no reverse proxy is being used
  microserviceid=args['microserviceid']

  raw_data_topic=args['raw_data_topic']
  preprocess_data_topic=args['preprocess_data_topic']
  ml_data_topic=args['ml_data_topic']
  prediction_data_topic=args['prediction_data_topic']
  
  VIPERTOKEN = context['ti'].xcom_pull(task_ids='step_1_solution_task_getparams',key="VIPERTOKEN")
  VIPERHOST = context['ti'].xcom_pull(task_ids='step_1_solution_task_getparams',key="VIPERHOSTPRODUCE")
  VIPERPORT = context['ti'].xcom_pull(task_ids='step_1_solution_task_getparams',key="VIPERPORTPRODUCE")
   
  ti = context['task_instance'] 
  ti.xcom_push(key="companyname", value=companyname)
  ti.xcom_push(key="myname", value=myname)
  ti.xcom_push(key="myemail", value=myemail)
  ti.xcom_push(key="mylocation", value=mylocation)
  ti.xcom_push(key="replication", value="_{}".format(replication))
  ti.xcom_push(key="numpartitions", value="_{}".format(numpartitions))
  ti.xcom_push(key="enabletls", value="_{}".format(enabletls))
  ti.xcom_push(key="microserviceid", value=microserviceid)
  ti.xcom_push(key="raw_data_topic", value=raw_data_topic)
  ti.xcom_push(key="preprocess_data_topic", value=preprocess_data_topic)
  ti.xcom_push(key="ml_data_topic", value=ml_data_topic)
  ti.xcom_push(key="prediction_data_topic", value=prediction_data_topic)
  
  print("Vipertoken=", VIPERTOKEN)
  print("VIPERHOST=", VIPERHOST)
  print("VIPERPORT=", VIPERPORT)

  #############################################################################################################
  #                         CREATE TOPIC TO STORE TRAINED PARAMS FROM ALGORITHM  

  topickeys = ['raw_data_topic','preprocess_data_topic','ml_data_topic','prediction_data_topic'] 

  for k in topickeys:
    producetotopic=args[k]
    description=args['description']

    topicsarr = producetotopic.split(",")

    for topic in topicsarr:  
      print("Creating topic=",topic)  
      result=maadstml.vipercreatetopic(VIPERTOKEN,VIPERHOST,VIPERPORT,topic,companyname,
                                 myname,myemail,mylocation,description,enabletls,
                                 brokerhost,brokerport,numpartitions,replication,
                                 microserviceid='')
      print("Result=",result)
