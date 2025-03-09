import os
from pandas import DataFrame as df, read_csv

from core.exceptions import raise_400_exception
from core.services.assets import AssetService
from core.services.users import UserService

from django.conf import settings

class FileService:

    @staticmethod
    def download_template_file():
        headers = ["User Id" ,"Asset ID", "Asset Quantity", "Start Date", "End Date"]

        template_dataframe = df(columns=headers)
        template_dataframe.loc[1] = [1, 12, 9, '2025-03-09', '2025-05-31']

        return template_dataframe

    @staticmethod
    def validate_file(uploaded_file):

        error_mssgs, row_wise_status = [], []
        extension_name = uploaded_file.name.split(".")[-1]

        if extension_name != "csv":
            print("Not a valid file! Please upload csv files only!!")
            raise_400_exception(
                detail={"detail": "Not a valid file! Please upload csv files only!!"}
            )
        uploaded_file_df = read_csv(uploaded_file)

        for idx, row in uploaded_file_df.iterrows():
            # print(idx, row)
            row_validation_status = True

            user_id, asset_id, start_date, end_date, quantity = int(row["User Id"]), int(row["Asset ID"]), row["Start Date"], row["End Date"], row["Asset Quantity"]

            if UserService.get_user_by_id(user_id) == "User not found":
                row_validation_status = False
                error_mssgs += ["User with the provided user id not found!"]

            if AssetService.get_asset_by_id(asset_id) is None:
                row_validation_status = False
                error_mssgs += ["Asset with the provided user id not found!"]
                print("*******", AssetService.get_asset_by_id(asset_id))

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
            print("*******")
            path = os.path.join(settings.MEDIA_URL, "validated-files")
            uploaded_file_df.to_csv(path, index=False)
            return True, uploaded_file_df
        else:
            return False, None






















