# product_list = []
# carts = []
# id = 1
# Order = """
# <html>
#     <body>
#         {% for item in Order %}
#             <p>商品: {% item.1 %} 價錢: {% item.2 %} 詳細: {% item.3 %} </p>
#         {% endfor %}
#         <br>
#         <br>
#         <p>總計: total_price
#     </body>
# </html>
#          """

# class Front:
#     def __init__(self, id):
#         self.id = id

#     def search_detail(self):
#         return Product.search_product(self.id)

#     def add_to_carts(self):
#         cart = Carts(carts)
#         cart.cart.append(Product.search_product(self.id))

#     def Checkout():
#         total_price = 0
#         carts_list = Carts(carts).cart_views()
#         for product in carts_list:
#             print("My item: ", product)
#             total_price += int(product['price'])
#         print(Order)




# class Product:
#     def __init__(self, product_list):
#         self.product_list = product_list

#     def views(self):
#         return self.product_list

#     def add_product(self, product_name, price, detail):
#         global id
#         self.product_list.append(dict(id=id, product_name=product_name,
#                                  price=price, detail=detail))
#         id += 1
#         return ''

#     def search_product(id):
#         for n in product_list:
#             if n.get('id') == int(id):
#                 return n


# class Carts:
#     def __init__(self, carts):
#         self.cart = carts
    
#     def cart_views(self):
#         return self.cart




# def main():
#     # Add product
#     n_product = ['iphone', 'samsung', 'rog']
#     n_price = ['100', 500, 700]
#     n_detail = ['shit', 'shit', 'shit']

#     for n in range(len(n_product)):
#         product = Product(product_list)
#         product.add_product(n_product[n], n_price[n], n_detail[n])
#     # View product list
#     print("View product_list: ", product.views())

#     # Return Front(id).<search_detail> --> Product.search_product('id)
#     result = Front('1').search_detail()
#     print('Search product result: ', result)

#     # Add product to carts
#     Front('1').add_to_carts()
#     print("View carts:", Carts(carts).cart_views())

#     # Checkout
#     Front.Checkout()

# main()


# class Func:
#     def __init__(self, user):
#         self.user = user
#     def Go_Test(self):
#         return Test(Func('John')).add()

# class Test:
#     def __init__(self, module):
#         self.module = module
#     def add(self):
#         return f'make from {self.module.user}'


# def main():
#     print(Func('John').Go_Test())

# main()
