from datetime import datetime
import os
from django.conf import settings
from pandas import DataFrame as df, read_csv
from operator import attrgetter
from itertools import chain
from typing import Dict

from core.exceptions import raise_400_exception
from core.services.assets import AssetService, AssetOwnerHistoryService
from core.services.users import UserService

class TimeLineUnit:
    def __init__(self, date, start_date_qunatity=0, end_date_qunatity=0):
        self.date = date
        self.start_date_qunatity += start_date_qunatity
        self.end_date_qunatity += end_date_qunatity

    def __str__(self):
        return f'{self.date.__str__()}::{self.start_date_qunatity}::{self.end_date_qunatity}\n'



class FileValidationService:
    def __create_timeline(assets_to_be_assigned, assets_to_be_returned):
        timeline: Dict[datetime.date, TimeLineUnit] = {}

        # creating a timeline for the assets to be assigned.
        for idx, row in assets_to_be_assigned.iterrows():
            start_date, end_date = datetime.strptime(row["Start Date"], "%Y-%m-%d"), datetime.strptime( row["Start Date"], "%Y-%m-%d")

            if start_date not in timeline:
                timeline[start_date] = TimeLineUnit(date=start_date, start_date_qunatity=row["Asset Quantity"])
            else:
                timeline[start_date].start_date_qunatity += row["Asset Quantity"]

            if end_date not in timeline:
                timeline[end_date] = TimeLineUnit(date=end_date, end_date_qunatity=row["Asset Quantity"])
            else:
                timeline[end_date].end_date_qunatity += row["Asset Quantity"]

        # creatting a timeline for the assets to be returned.
        for asset in assets_to_be_returned:
            start_date, end_date = asset.start_date.date(), asset.end_date.date()

            if start_date not in timeline:
                timeline[start_date] = TimeLineUnit(date=start_date, start_date_qunatity=asset.requisition_qunatity)
            else:
                timeline[start_date].start_date_qunatity += asset.requisition_qunatity

            if end_date not in timeline:
                timeline[end_date] = TimeLineUnit(date=end_date, end_date_qunatity=asset.requisition_qunatity)
            else:
                timeline[end_date].end_date_qunatity += asset.requisition_qunatity

        # Sort the timeline by date
        timeline = sorted(timeline.values(), key=attrgetter("date"))

        return timeline

    def __run_totality_check(asset_id, assets_to_be_assigned, assets_to_be_returned):
        """
        1. Find the current quantity of the asset in the db.
        2. Run through the assets and update the present quantity of the asset accordingly.Check if the requisition quantity is less than the current quantity of the asset in the db at all times.
        3. If not, then return error message.
        4. If yes, then return success message.

        """
        # Find the current quantity of the asset in the db.
        asset = AssetService.get_asset_by_id(asset_id)
        current_quantity, current_date = asset.quantity, datetime.now().date()
        totality_check = True

        print("Current Asset ID: ", asset_id)
        print("Current Date: ", current_date)
        print("Current Quantity: ", current_quantity)

        timeline = FileValidationService.__create_timeline(assets_to_be_assigned, assets_to_be_returned)
        [print(time_unit) for time_unit in timeline]


        error_messages = []

        # Run through the assets and update the present quantity of the asset accordingly.
        for time_unit in timeline:
            if (time_unit.date < current_date):
                continue
            current_quantity += (-time_unit.start_date_qunatity + time_unit.end_date_qunatity)

            print(f"On {time_unit.date.__str__()}, New quantity : {current_quantity}")

            # Check if the requisition quantity is less than the current quantity of the asset in the db at all times.
            if current_quantity < 0:
                error_messages += f"Asset ID: {asset_id} has a requisition quantity of {time_unit.start_date_qunatity} on {time_unit.date.__str__()} but the current quantity will be {current_quantity} then."
                print(error_messages)
                totality_check = False

        return totality_check, error_messages  # Return totality_check and error_message

    def __check_file_in_totality(asset_ids, uploaded_file_df):
        totality_check = set()
        totality_error_messages = list()

        for asset_id in asset_ids:
            # get assets from uploaded_file_df
            assets_to_be_assigned = uploaded_file_df[uploaded_file_df["Asset ID"] == asset_id]

            # get asset from db where end date is < today's date[i.e not returned yet]
            assets_to_be_returned = AssetOwnerHistoryService.get_asset_owner_history(asset_id).filter(end_date__gte=datetime.now())

            # Run totality check on the assets.
            check_success, error_messages = FileValidationService.__run_totality_check(asset_id, assets_to_be_assigned, assets_to_be_returned)

            if not check_success:
                print(f"Totality check failed for Asset ID {asset_id}: {"\n".join(error_messages)}")
                totality_check.add(False)
                totality_error_messages += error_messages
            else:
                print(f"Totality check passed for Asset ID {asset_id}.")
                totality_check.add(True)

        return all(totality_check), totality_error_messages

    def __file_extension_validation(uploaded_file):
        """
        Check if the file is a csv file or not.
        """

        if "." not in uploaded_file:
            print("Not a valid file! Please upload files with '.csv' extensions only!!")
            return False, "Not a valid file! Please upload files with '.csv' extensions only!!"

        extension_name = uploaded_file.name.split(".")[-1]
        print("File extension name: ", extension_name)

        if extension_name != "csv":
            print("Not a valid file! Please upload csv files only!!")
            return False, "Not a valid file! Please upload csv files only!!"

        return True, None

    def __row_wise_validation(uploaded_file_df):
        """
        Check if the row data is valid or not.
        """
        error_mssgs, row_wise_status = [], []
        asset_ids = set()
        for idx, row in uploaded_file_df.iterrows():
            print(idx, row)
            row_validation_status = True

            user_id, asset_id, start_date, end_date, quantity = int(row["User Id"]), int(row["Asset ID"]), row["Start Date"], row["End Date"], row["Asset Quantity"]
            asset_ids.add(asset_id)

            if UserService.get_user_by_id(user_id) == "User not found":
                row_validation_status = False
                error_mssgs += ["User with the provided user id not found!"]

            if AssetService.get_asset_by_id(asset_id) is None:
                row_validation_status = False
                error_mssgs += ["Asset with the provided user id not found!"]

            if AssetService.get_asset_by_id(asset_id) != None:
                asset = AssetService.get_asset_by_id(asset_id)
                validation_quantity_res = AssetService.validate_requisition_quantity(asset, quantity)
                validation_dates_res = AssetService.validate_requisition_dates(asset, start_date, end_date)

                print(validation_quantity_res, validation_dates_res)

                if validation_quantity_res != "ok" :
                    row_validation_status = False
                    error_mssgs += list(map(lambda message: message[1], validation_quantity_res))
                if validation_dates_res != "ok":
                    row_validation_status = False
                    error_mssgs += list(map(lambda message: message[1], validation_dates_res))

            row_wise_status += [row_validation_status]
            uploaded_file_df.at[idx, "Status"] = "OK" if row_validation_status is True else "; ".join(error_mssgs)

        if all(row_wise_status) is True:
            return True, uploaded_file_df
        else:
            return False, None

    @staticmethod
    def run_validations(uploaded_file):
        """
        Run all the validations on the uploaded file.
        """
        # Check if the file is a csv file or not.
        file_extension_validation_check, file_extension_check_error_message = FileValidationService.__file_extension_validation(uploaded_file)

        if not file_extension_validation_check:
            return (file_extension_check_error_message)

        # Check if the row data is valid or not.
        uploaded_file_df = read_csv(uploaded_file, sep=",") # Read the uploaded file
        row_wise_data_check, uploaded_file_df = FileValidationService.__row_wise_validation(uploaded_file_df)

        # Check the file in totality for each asset.
        asset_ids = set(uploaded_file_df["Asset ID"])
        totality_check, totality_check_error_messages = FileValidationService.__check_file_in_totality(asset_ids, uploaded_file_df)

        return (
                    (row_wise_data_check, uploaded_file_df),
                    (totality_check, totality_check_error_messages)
                )

class FileService:

    @staticmethod
    def download_template_file():
        headers = ["User Id" ,"Asset ID", "Asset Quantity", "Start Date", "End Date"]

        template_dataframe = df(columns=headers)
        template_dataframe.loc[1] = [1, 12, 9, datetime.now().strftime('%Y-%m-%d'), '2999-12-31']

        return template_dataframe

    @staticmethod
    def validate_file(uploaded_file):
        validation_result = FileValidationService.run_validations(uploaded_file)

        if type(validation_result) == str:
            raise_400_exception(validation_result)

        else:
            # unpack the validation result
            row_wise_validation, totality_check_validation = validation_result


            row_wise_data_check, uploaded_file_df = row_wise_validation
            totality_check, totality_check_error_messages = totality_check_validation


            return (
                all([row_wise_data_check, totality_check]),
                uploaded_file_df,
                totality_check, # totality check status
                totality_check_error_messages, # error messages from totality check
            )

    @staticmethod
    def generate_file_path(request):
        dirpath = os.path.join(settings.MEDIA_ROOT, "validated-files")
        os.makedirs(dirpath, exist_ok=True)

        filename = f"{request.user.email}##{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}##Asset_Upload.csv"
        file_path = os.path.join(dirpath, filename)

        print(file_path)
        return file_path




