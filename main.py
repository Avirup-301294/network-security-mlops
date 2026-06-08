# Components
from networksecurity.components.data_ingestion import DataIngestion

# Config
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, TrainingPipelineConfig

# Loggers & Exception
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import sys

def data_ingestion(training_pipeline_config):
    try:
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info(" ##### Initiate the data ingestion ##### ")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(" ##### Data Initiation Completed ##### ")
        return data_ingestion_artifact
    except Exception as e:
           raise NetworkSecurityException(e, sys)

def data_validation(training_pipeline_config, data_ingestion_artifact):
    try:
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info(" ##### Initiate the data Validation ##### ")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info(" ##### data Validation Completed ##### ")
        return data_validation_artifact
    except Exception as e:
           raise NetworkSecurityException(e, sys)
    
def data_transformation(training_pipeline_config, data_validation_artifact):
     try:
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info(" ##### Initiate Data Transformation ##### ")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(" ##### data Transformation completed ##### ")
        return data_transformation_artifact
     except Exception as e:
           raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_artifact = data_ingestion(training_pipeline_config)
    print("\n\n")
    data_validation_artifact = data_validation(training_pipeline_config, data_ingestion_artifact)
    print("\n\n")
    data_transformation_artifact = data_transformation(training_pipeline_config, data_validation_artifact)
