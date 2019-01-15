import graphene
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, permission_required

from .account.mutations import (
    CustomerCreate, CustomerUpdate, PasswordReset, SetPassword, StaffCreate,
    StaffUpdate, AddressCreate, AddressUpdate, AddressDelete)
from .account.resolvers import resolve_users
from .account.types import User
from .menu.resolvers import resolve_menu, resolve_menus, resolve_menu_items
from .menu.types import Menu, MenuItem
# FIXME: sorting import by putting below line at the beginning breaks app
from .menu.mutations import (
    AssignNavigation, MenuCreate, MenuDelete, MenuUpdate, MenuItemCreate,
    MenuItemDelete, MenuItemUpdate)
from .descriptions import DESCRIPTIONS
from .discount.resolvers import resolve_sales, resolve_vouchers
from .discount.types import Sale, Voucher
from .discount.mutations import (
    SaleCreate, SaleDelete, SaleUpdate, VoucherCreate, VoucherDelete,
    VoucherUpdate)
from .core.filters import DistinctFilterSet
from .core.mutations import CreateToken, VerifyToken
from .order.filters import OrderFilter
from .order.resolvers import resolve_order, resolve_orders
from .order.types import Order
from .order.mutations.draft_orders import (
    DraftOrderComplete, DraftOrderCreate, DraftOrderDelete, DraftOrderUpdate)
from .order.mutations.fulfillments import (
    FulfillmentCancel, FulfillmentCreate, FulfillmentUpdate)
from .order.mutations.orders import (
    OrderAddNote, OrderCancel, OrderCapture, OrderMarkAsPaid, OrderRefund,
    OrderRelease, OrderUpdate)
from .page.resolvers import resolve_pages, resolve_page
from .page.types import Page
from .page.mutations import PageCreate, PageDelete, PageUpdate
from .product.filters import ProductFilterSet
from .product.mutations.attributes import (
    AttributeChoiceValueCreate, AttributeChoiceValueDelete,
    AttributeChoiceValueUpdate, ProductAttributeCreate, ProductAttributeDelete,
    ProductAttributeUpdate)
from .product.mutations.products import (
    CategoryCreate, CategoryDelete, CategoryUpdate,
    CollectionAddProducts, CollectionCreate, CollectionDelete,
    CollectionRemoveProducts, CollectionUpdate, ProductCreate,
    ProductDelete, ProductUpdate, ProductTypeCreate,
    ProductTypeDelete, ProductImageCreate, ProductImageDelete,
    ProductImageReorder, ProductImageUpdate, ProductTypeUpdate,
    ProductVariantCreate, ProductVariantDelete,
    ProductVariantUpdate, VariantImageAssign, VariantImageUnassign)
from .product.resolvers import (
    resolve_attributes, resolve_categories, resolve_collections,
    resolve_products, resolve_product_types, resolve_product_variants)
from .product.types import (
    Category, Collection, Product, ProductAttribute, ProductType,
    ProductVariant)
from .shipping.resolvers import resolve_shipping_zones
from .shipping.types import ShippingZone
from .shipping.mutations import (
    ShippingZoneCreate, ShippingZoneDelete, ShippingZoneUpdate,
    ShippingPriceCreate, ShippingPriceDelete, ShippingPriceUpdate)

from .shop.types import Shop
from .shop.mutations import (
    ShopDomainUpdate, ShopSettingsUpdate, HomepageCollectionUpdate)


class Query(graphene.ObjectType):
    attributes = DjangoFilterConnectionField(
        ProductAttribute, filterset_class=DistinctFilterSet,
        query=graphene.String(description=DESCRIPTIONS['attributes']),
        in_category=graphene.Argument(graphene.ID),
        description='List of the shop\'s product attributes.')
    categories = DjangoFilterConnectionField(
        Category, filterset_class=DistinctFilterSet, query=graphene.String(
            description=DESCRIPTIONS['category']),
        level=graphene.Argument(graphene.Int),
        description='List of the shop\'s categories.')
    category = graphene.Field(
        Category, id=graphene.Argument(graphene.ID),
        description='Lookup a category by ID.')
    collection = graphene.Field(
        Collection, id=graphene.Argument(graphene.ID),
        description='Lookup a collection by ID.')
    collections = DjangoFilterConnectionField(
        Collection, query=graphene.String(
            description=DESCRIPTIONS['collection']),
        description='List of the shop\'s collections.')
    menu = graphene.Field(
        Menu, id=graphene.Argument(graphene.ID),
        name=graphene.Argument(graphene.String, description="Menu name."),
        description='Lookup a menu by ID or name.')
    menus = DjangoFilterConnectionField(
        Menu, query=graphene.String(description=DESCRIPTIONS['menu']),
        description="List of the shop\'s menus.")
    menu_item = graphene.Field(
        MenuItem, id=graphene.Argument(graphene.ID),
        description='Lookup a menu item by ID.')
    menu_items = DjangoFilterConnectionField(
        MenuItem, query=graphene.String(description=DESCRIPTIONS['menu_item']),
        description='List of the shop\'s menu items.')
    order = graphene.Field(
        Order, description='Lookup an order by ID.',
        id=graphene.Argument(graphene.ID))
    orders = DjangoFilterConnectionField(
        Order, filterset_class=OrderFilter, query=graphene.String(
            description=DESCRIPTIONS['order']),
        description='List of the shop\'s orders.')
    page = graphene.Field(
        Page, id=graphene.Argument(graphene.ID), slug=graphene.String(),
        description='Lookup a page by ID or by slug.')
    pages = DjangoFilterConnectionField(
        Page, filterset_class=DistinctFilterSet, query=graphene.String(
            description=DESCRIPTIONS['page']),
        description='List of the shop\'s pages.')
    product = graphene.Field(
        Product, id=graphene.Argument(graphene.ID),
        description='Lookup a product by ID.')
    products = DjangoFilterConnectionField(
        Product, filterset_class=ProductFilterSet, query=graphene.String(
            description=DESCRIPTIONS['product']),
        description='List of the shop\'s products.')
    product_type = graphene.Field(
        ProductType, id=graphene.Argument(graphene.ID),
        description='Lookup a product type by ID.')
    product_types = DjangoFilterConnectionField(
        ProductType, filterset_class=DistinctFilterSet,
        description='List of the shop\'s product types.')
    product_variant = graphene.Field(
        ProductVariant, id=graphene.Argument(graphene.ID),
        description='Lookup a variant by ID.')
    product_variants = DjangoFilterConnectionField(
        ProductVariant, filterset_class=DistinctFilterSet,
        ids=graphene.List(graphene.ID),
        description='Lookup multiple variants by ID')
    sale = graphene.Field(
        Sale, id=graphene.Argument(graphene.ID),
        description='Lookup a sale by ID.')
    sales = DjangoFilterConnectionField(
        Sale, query=graphene.String(description=DESCRIPTIONS['sale']),
        description="List of the shop\'s sales.")
    shop = graphene.Field(Shop, description='Represents a shop resources.')
    voucher = graphene.Field(
        Voucher, id=graphene.Argument(graphene.ID),
        description='Lookup a voucher by ID.')
    vouchers = DjangoFilterConnectionField(
        Voucher, query=graphene.String(description=DESCRIPTIONS['product']),
        description="List of the shop\'s vouchers.")
    shipping_zone = graphene.Field(
        ShippingZone, id=graphene.Argument(graphene.ID),
        description='Lookup a shipping zone by ID.')
    shipping_zones = DjangoFilterConnectionField(
        ShippingZone, description='List of the shop\'s shipping zones.')
    user = graphene.Field(
        User, id=graphene.Argument(graphene.ID),
        description='Lookup an user by ID.')
    users = DjangoFilterConnectionField(
        User, description='List of the shop\'s users.',
        query=graphene.String(
            description=DESCRIPTIONS['user']))
    node = graphene.Node.Field()

    def resolve_attributes(self, info, in_category=None, query=None, **kwargs):
        return resolve_attributes(info, in_category, query)

    def resolve_category(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Category)

    def resolve_categories(self, info, level=None, query=None, **kwargs):
        return resolve_categories(info, level=level, query=query)

    def resolve_collection(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Collection)

    def resolve_collections(self, info, query=None, **kwargs):
        return resolve_collections(info, query)

    @permission_required(['account.manage_users'])
    def resolve_user(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, User)

    @permission_required('account.manage_users')
    def resolve_users(self, info, query=None, **kwargs):
        return resolve_users(info, query=query)

    def resolve_menu(self, info, id=None, name=None):
        return resolve_menu(info, id, name)

    def resolve_menus(self, info, query=None, **kwargs):
        return resolve_menus(info, query)

    def resolve_menu_item(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, MenuItem)

    def resolve_menu_items(self, info, query=None, **kwargs):
        return resolve_menu_items(info, query)

    def resolve_page(self, info, id=None, slug=None):
        return resolve_page(info, id, slug)

    def resolve_pages(self, info, query=None, **kwargs):
        return resolve_pages(info, query=query)

    @login_required
    def resolve_order(self, info, id):
        return resolve_order(info, id)

    @login_required
    def resolve_orders(self, info, query=None, **kwargs):
        return resolve_orders(info, query)

    def resolve_product(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Product)

    def resolve_products(self, info, category_id=None, query=None, **kwargs):
        return resolve_products(info, category_id, query)

    def resolve_product_type(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ProductType)

    def resolve_product_types(self, info, **kwargs):
        return resolve_product_types()

    def resolve_shop(self, info):
        return Shop()

    @permission_required('discount.manage_discounts')
    def resolve_sale(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Sale)

    @permission_required('discount.manage_discounts')
    def resolve_sales(self, info, query=None, **kwargs):
        return resolve_sales(info, query)

    def resolve_product_variant(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ProductVariant)

    def resolve_product_variants(self, info, ids=None, **kwargs):
        return resolve_product_variants(info, ids)

    @permission_required('discount.manage_discounts')
    def resolve_voucher(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Voucher)

    @permission_required('discount.manage_discounts')
    def resolve_vouchers(self, info, query=None, **kwargs):
        return resolve_vouchers(info, query)

    def resolve_shipping_zone(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ShippingZone)

    def resolve_shipping_zones(self, info, **kwargs):
        return resolve_shipping_zones(info)


class Mutations(graphene.ObjectType):
    assign_navigation = AssignNavigation.Field()

    token_create = CreateToken.Field()
    token_refresh = graphql_jwt.Refresh.Field()
    token_verify = VerifyToken.Field()

    set_password = SetPassword.Field()
    password_reset = PasswordReset.Field()

    attribute_choice_value_create = AttributeChoiceValueCreate.Field()
    attribute_choice_value_delete = AttributeChoiceValueDelete.Field()
    attribute_choice_value_update = AttributeChoiceValueUpdate.Field()

    category_create = CategoryCreate.Field()
    category_delete = CategoryDelete.Field()
    category_update = CategoryUpdate.Field()

    customer_create = CustomerCreate.Field()
    customer_update = CustomerUpdate.Field()

    staff_create = StaffCreate.Field()
    staff_update = StaffUpdate.Field()

    address_create = AddressCreate.Field()
    address_update = AddressUpdate.Field()
    address_delete = AddressDelete.Field()

    collection_create = CollectionCreate.Field()
    collection_update = CollectionUpdate.Field()
    collection_delete = CollectionDelete.Field()
    collection_add_products = CollectionAddProducts.Field()
    collection_remove_products = CollectionRemoveProducts.Field()

    menu_create = MenuCreate.Field()
    menu_delete = MenuDelete.Field()
    menu_update = MenuUpdate.Field()

    menu_item_create = MenuItemCreate.Field()
    menu_item_delete = MenuItemDelete.Field()
    menu_item_update = MenuItemUpdate.Field()

    draft_order_create = DraftOrderCreate.Field()
    draft_order_complete = DraftOrderComplete.Field()
    draft_order_delete = DraftOrderDelete.Field()
    draft_order_update = DraftOrderUpdate.Field()
    fulfillment_cancel = FulfillmentCancel.Field()
    fulfillment_create = FulfillmentCreate.Field()
    fulfillment_update = FulfillmentUpdate.Field()
    order_add_note = OrderAddNote.Field()
    order_cancel = OrderCancel.Field()
    order_capture = OrderCapture.Field()
    order_mark_as_paid = OrderMarkAsPaid.Field()
    order_refund = OrderRefund.Field()
    order_release = OrderRelease.Field()
    order_update = OrderUpdate.Field()

    page_create = PageCreate.Field()
    page_delete = PageDelete.Field()
    page_update = PageUpdate.Field()

    product_attribute_create = ProductAttributeCreate.Field()
    product_attribute_delete = ProductAttributeDelete.Field()
    product_attribute_update = ProductAttributeUpdate.Field()

    product_create = ProductCreate.Field()
    product_delete = ProductDelete.Field()
    product_update = ProductUpdate.Field()

    product_image_create = ProductImageCreate.Field()
    product_image_reorder = ProductImageReorder.Field()
    product_image_delete = ProductImageDelete.Field()
    product_image_update = ProductImageUpdate.Field()

    product_type_create = ProductTypeCreate.Field()
    product_type_update = ProductTypeUpdate.Field()
    product_type_delete = ProductTypeDelete.Field()

    product_variant_create = ProductVariantCreate.Field()
    product_variant_delete = ProductVariantDelete.Field()
    product_variant_update = ProductVariantUpdate.Field()

    sale_create = SaleCreate.Field()
    sale_delete = SaleDelete.Field()
    sale_update = SaleUpdate.Field()

    shop_domain_update = ShopDomainUpdate.Field()
    shop_settings_update = ShopSettingsUpdate.Field()
    homepage_collection_update = HomepageCollectionUpdate.Field()

    voucher_create = VoucherCreate.Field()
    voucher_delete = VoucherDelete.Field()
    voucher_update = VoucherUpdate.Field()

    shipping_zone_create = ShippingZoneCreate.Field()
    shipping_zone_delete = ShippingZoneDelete.Field()
    shipping_zone_update = ShippingZoneUpdate.Field()

    shipping_price_create = ShippingPriceCreate.Field()
    shipping_price_delete = ShippingPriceDelete.Field()
    shipping_price_update = ShippingPriceUpdate.Field()

    variant_image_assign = VariantImageAssign.Field()
    variant_image_unassign = VariantImageUnassign.Field()


schema = graphene.Schema(Query, Mutations)
