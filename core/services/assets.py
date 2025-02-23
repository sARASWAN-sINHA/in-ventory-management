from core.models import Asset

from django.contrib.auth import get_user_model


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

    def get_assets(asset_id_list: list):
        return Asset.objects.filter(id__in=asset_id_list)

    def validate_requisition_quantity(asset, requisition_qunatity):
        return asset.quantity >= requisition_qunatity

    @staticmethod
    def validate_requisitions(requisitions):

        validation_result = dict()
        asset_not_found_errors, quantity_validation_errors = [], []
        validation_success = True
        assets_and_requisitions = set()

        for requisition in requisitions:
            asset_id, requisition_quantity = requisition.values()
            asset = AssetService.get_asset_by_id(asset_id=asset_id)
            if asset is None:
                asset_not_found_errors.append(asset_id)
            elif AssetService.validate_requisition_quantity(asset, requisition_quantity) is False:
                quantity_validation_errors.append(asset_id)
            else:
                assets_and_requisitions.add((asset, requisition_quantity))

        if len(asset_not_found_errors) != 0 or len(quantity_validation_errors) != 0:
            validation_success = False
            validation_result = {
                "validation_errors": asset_not_found_errors,
                "bad_request_errors": quantity_validation_errors,
            }
        elif len(asset_not_found_errors) == 0 and len(quantity_validation_errors) == 0:
            validation_result = {
                "assets_and_requisitions": assets_and_requisitions,
            }
        return (validation_success, validation_result)

    def assign_asset_to_user(asset, user, requisition_quantity):
        asset.current_owner = user
        asset.quantity -= requisition_quantity
        asset.save()

    @staticmethod
    def assign(user, validation_result):
        assets_and_requisitions = validation_result.get("assets_and_requisitions")
        set(map(lambda asset_and_requisition: AssetService.assign_asset_to_user(asset_and_requisition[0], user, asset_and_requisition[1]), assets_and_requisitions))
