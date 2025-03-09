from core.models import Asset, AssetOwnerHistory

from django.contrib.auth import get_user_model

from datetime import datetime, timedelta


class AssetService:

    @staticmethod
    def check_qunatity_greater_than_zero(asset_quantity: int):
        return asset_quantity > 0

    @staticmethod
    def get_asset_by_id(asset_id: int):
        try:
            return Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return None

    @staticmethod
    def get_asset_owner(asset_id: int):
        asset = AssetService.get_asset_by_id(asset_id)
        if asset:
            return asset.current_owner
        else:
            return None

    @staticmethod
    def get_user_assets(user: get_user_model):
        return user.assets

    def get_date(date:str):
        year, month, day = tuple(map(int, date.split("-")))
        return datetime(year, month, day)

    def get_assets(asset_id_list: list):
        return Asset.objects.filter(id__in=asset_id_list)

    def validate_requisition_quantity(asset, requisition_qunatity):
        errors = []

        if asset.quantity < requisition_qunatity: errors += [("Requisition Quantity is more than avaialable quantity.", asset.name)]
        if AssetService.check_qunatity_greater_than_zero(requisition_qunatity) is False: errors += [("Requisition quantity cannot be less than equal to 0", asset.name)]

        if errors == []: return "ok"
        return errors

    def validate_requisition_dates(asset,start_date, end_date):
        start_date, end_date = AssetService.get_date(start_date), AssetService.get_date(end_date)

        errors = []

        if start_date > end_date: errors += [("Start date cannot be after end date.", asset.name)]
        if start_date < datetime.now() - timedelta(days=30): errors += [("Cannot have a start date for a requisition that is over a month old.", asset.name)]
        if start_date > datetime.now() + timedelta(days=30): errors += [("Cannot have a start date for a requisition that is over a month for now.", asset.name)]

        if errors == []: return "ok"
        return errors

    @staticmethod
    def validate_requisitions(requisitions) :

        validation_result = dict()
        asset_not_found_errors, quantity_validation_errors, date_validation_error = [], [], []
        validation_success = True
        assets_and_requisitions = set()

        for requisition in requisitions:
            requisition_values = requisition.values()
            print("requisition_values", requisition_values)
            if len(requisition_values) == 4:
                asset_id, requisition_quantity, requisition_start_date, requisition_end_date = requisition.values()
            elif len(requisition_values) == 3:
                asset_id, requisition_quantity, requisition_start_date, requisition_end_date = requisition.values(), '2999-01-01'

            asset = AssetService.get_asset_by_id(asset_id=asset_id)

            if asset is None:
                asset_not_found_errors.append(("NO asset with matching asset ID found!", asset_id))
            else:
                validation_quantity_res = AssetService.validate_requisition_quantity(asset, requisition_quantity)
                validation_dates_res = AssetService.validate_requisition_dates(asset, requisition_start_date, requisition_end_date)

                print(validation_quantity_res, validation_dates_res)

                if validation_quantity_res != "ok" :
                    quantity_validation_errors += validation_quantity_res
                if validation_dates_res != "ok":
                    date_validation_error += validation_dates_res

            if (
                asset is not None
                and validation_quantity_res == "ok"
                and validation_dates_res == "ok"
            ):
                assets_and_requisitions.add((asset, requisition_quantity, requisition_start_date, requisition_end_date))

        if (
            len(asset_not_found_errors) != 0
            or len(quantity_validation_errors) != 0
            or len(date_validation_error) != 0
        ):
            validation_success = False
            validation_result = {
                "validation_errors": asset_not_found_errors,
                "quantity_validation_errors": quantity_validation_errors,
                'date_validation_error': date_validation_error
            }
        elif (
            len(asset_not_found_errors) == 0
            and len(quantity_validation_errors) == 0
            and len(date_validation_error) == 0
        ):
            validation_success = True
            validation_result = {
                "assets_and_requisitions": assets_and_requisitions,
            }
        return (validation_success, validation_result)

    def create_requisition_record(
        user, asset, start_date, end_date, requisition_quantity
    ):
        AssetOwnerHistory.objects.create(
            user=user,
            asset=asset,
            start_date=start_date,
            end_date=end_date,
            requisition_qunatity=requisition_quantity,
        )

    def assign_asset_to_user(asset, user, requisition_quantity):
        asset.current_owner = user
        print("Before:- ", asset.quantity)
        asset.quantity -= requisition_quantity
        print("After:- ", asset.quantity)
        asset.save()

    @staticmethod
    def assign(user, validation_result):

        assets_and_requisitions = validation_result.get("assets_and_requisitions")
        print(assets_and_requisitions)

        # assigning asset(s) to user
        set(
            map(
                lambda asset_and_requisition: AssetService.assign_asset_to_user(asset=asset_and_requisition[0], user=user, requisition_quantity=asset_and_requisition[1]),
                assets_and_requisitions
            )
        )

        # creating an asset assignment record for each asset that is being assigned to the user.
        set(
            map(
                lambda asset_and_requisition: AssetService.create_requisition_record(user=user, asset=asset_and_requisition[0], start_date=asset_and_requisition[2], end_date=asset_and_requisition[3], requisition_quantity=asset_and_requisition[1]),
                assets_and_requisitions
            )
        )
