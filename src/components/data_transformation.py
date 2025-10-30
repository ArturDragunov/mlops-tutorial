import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """This function is responsible for data transformation"""
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # you connect steps into a chain. First, imputer, then scaler
            # You fit and transform train set. and only transform test set
            num_pipeline= Pipeline( 
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                
                # Scaling with mean does not work (and will raise an exception) when attempted on
                # sparse matrices, because centering them entails building a dense
                # matrix which in common use cases is likely to be too large to fit in
                # memory.
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
              # (pipeline name, defined pipeline, columns to be transformed)
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            # fit_transform on train data and transform on test data
            return preprocessor 
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # numpy arrays are returned after transformations are done
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # np.c_ is a NumPy shortcut for concatenating arrays column-wise.
            # np.c_[A, B]  ≈  np.concatenate((A, B), axis=1)
            train_arr = np.c_[ # np.c_[X, y]
                #       X_train                     Y_train
                input_feature_train_arr, np.array(target_feature_train_df)
            ]                   # X_test                    Y_test
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # alternative syntax would be:
            # preprocessing_obj.set_output(transform="polars")
            # input_feature_train_df = preprocessing_obj.fit_transform(input_feature_train_df)
            # input_feature_test_df = preprocessing_obj.transform(input_feature_test_df)
            # train_df = input_feature_train_df.assign(target=target_feature_train_df)
            # test_df = input_feature_test_df.assign(target=target_feature_test_df)

            logging.info(f"Saved preprocessing object.")

            save_object(
                # artifacts/preprocessor.pkl
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                # defined object from get_data_transformer_object
                # we save it because this object was fit on train data
                # we don't need to retrain it from scratch each time
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
