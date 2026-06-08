from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging 

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp

import pandas as pd
import os, sys

from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(
            self,data_ingestion_artifact: DataIngestionArtifact,
            data_validation_config: DataValidationConfig
        ):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            # print(self._schema_config)
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns: return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates if all required numerical columns are present in the dataframe
        and confirms they hold numeric data types.
        """
        try:
            # 1. Check for column presence using optimized set operations
            numerical_columns = set(self._schema_config["numerical_columns"])
            dataframe_columns = set(dataframe.columns)
            
            logging.info(f"Required numerical columns count: {len(numerical_columns)}")
            logging.info(f"Required numerical columns: {numerical_columns}")
            
            # Find elements in schema that do not exist in dataframe columns
            missing_columns = numerical_columns - dataframe_columns
            
            if missing_columns:
                logging.error(f"Missing numerical columns in dataframe: {missing_columns}")
                return False
                
            # 2. Check for correct data type (Ensures they are actual numeric values)
            for col in numerical_columns:
                if not pd.api.types.is_numeric_dtype(dataframe[col]):
                    logging.error(f"Column '{col}' is missing or is not numeric. Found type: {dataframe[col].dtype}")
                    return False

            logging.info("All required numerical columns are present and valid.")
            return True
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self,base_df, current_df, threshold = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path  =  self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path  =  os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok = True)
            write_yaml_file(file_path = drift_report_file_path,content = report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            ## 1. fetching the train & test file path
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## 2. Read the data from train and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            ## 3. validate number of columns in train and test dataframe
            status = self.validate_number_of_columns(dataframe = train_dataframe)
            if not status: error_message = f"Train dataframe does not contain all columns.\n"
            
            status  =  self.validate_number_of_columns(dataframe = test_dataframe)
            if not status: error_message = f"Test dataframe does not contain all columns.\n"   

            ## 4. Check if Numerical columns exists
            status = self.validate_numerical_columns_exist(dataframe = train_dataframe)
            if not status: error_message = f"Train dataframe does not contain all numerical columns.\n"
            
            status  =  self.validate_numerical_columns_exist(dataframe = test_dataframe)
            if not status: error_message = f"Test dataframe does not contain all numerical columns.\n"   

            ## 5. lets check datadrift
            status = self.detect_dataset_drift(base_df = train_dataframe, current_df = test_dataframe)
            
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok = True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index = False, header = True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index = False, header = True)
            
            data_validation_artifact  =  DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)