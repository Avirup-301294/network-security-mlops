# Components
from networksecurity.components.data_ingestion import DataIngestion

# Config
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

# Loggers & Exception
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import sys

def data_ingestion():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info(" ##### Initiate the data ingestion ##### ")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(" ##### Data Initiation Completed ##### ")
    except Exception as e:
           raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    data_ingestion()
