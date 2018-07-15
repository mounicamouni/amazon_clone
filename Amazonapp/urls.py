from django.conf.urls import url
from django.urls import path
from Amazonapp import views


from Amazonapp.views import *


urlpatterns = [

    path('signup/', signup, name='signup'),
    path('login/',LoginController.as_view(),name="login_html"),
path('accounts/login/',LoginController.as_view(),name="login_html"),
    path('logout/',logout_user,name="logout_html"),

url(r'^$',CategoryListView.as_view(),name="home"),
    path("category/",CategoryListView.as_view(),name="category_html"),

    path("category/<int:pk>",SubcategoryList.as_view(),name="subcategory_html"),

    path("category/<int:category_id>/subcategory/<int:pk>/products/add",CreateSubcategoryProductView.as_view(),name="subcategoryproduct_add_html"),
    path("category/<int:category_id>/subcategory/<int:pk>",SubcategoryProductList.as_view(),name="product_html"),
    path("category/<int:category_id>/subcategory/<int:subcategory_id>/products/<int:pk>/edit", UpdateSubcategoryProductView.as_view(),
         name="subcategoryproduct_edit_html"),
path("category/<int:category_id>/subcategory/<int:subcategory_id>/products/<int:pk>/delete", DeleteSubcategoryProductView.as_view(),
         name="subcategoryproduct_delete_html"),
    path("category/add",CreateCategoryView.as_view(),name="categoryadd_html"),

    path('category/<int:pk>/edit',UpdateCategoryView.as_view(),name="edit_category_html"),
    path('category/<int:pk>/delete',DeleteCategoryView.as_view(),name="delete_category_html"),

    path("category/<int:pk>/subcategory/add", CreateSubcategoryView.as_view(), name="subcategory_add_html"),
path("category/<int:category_id>/subcategory/<int:pk>/edit",UpdateSubcategoryView.as_view(),name="subcategory_edit_html"),
path("category/<int:category_id>/subcategory/<int:pk>/delete",DeleteSubcategoryView.as_view(),name="subcategory_delete_html"),


    path("address/<int:pk>",AddressListView.as_view(),name="address_html"),
    path("address/<int:pk>/delete",DeleteAddressView.as_view(),name="address_delete_html"),
    path("address/<int:pk>/edit",UpdateAddressView.as_view(),name="address_edit_html"),
    path("address/add",CreateAddressView.as_view(),name="address_add_html"),

    path("address/",address,name="address"),

    path("cart/<int:pk>",CartListView.as_view(),name="cart_html"),
    path("addtocart/<int:pk>",cart_create,name="addtocart_html"),
    path("increment/<int:pk>", increment_cart, name="increment_html"),
    path("decrement/<int:pk>", decrement_cart, name="decrement_html"),
    path("deletecart/<int:pk>",delete_cart,name="delete_cart_html"),

    path("cart/",cart,name="cart"),

    path("placeorder/",place_order,name="place_order"),
    path("order/<int:pk>",OrderListView.as_view(),name="order_html"),
    path("order/",order,name="order"),

    path('search/', search_all, name='list'),

    path('categorysearch/<slug:string>/',SearchCategoryView, name='list_category'),
    path('subcategorysearch/<slug:string>/',SearchSubcategoryView, name='list_subcategory'),

    path('productsearch/<slug:string>/', SearchProductView, name='list_product'),

    # path('categorysearch/<slug:string>/',SearchCategoryView.as_view(), name='list_category'),
# path('categorysearch/(?P<sub_slug>\w+)/$',SearchCategoryView.as_view(), name='list_category'),

    # url("subcategorysearch/<value>/", SearchSubcategoryView.as_view(), name='list_subcategory'),


]