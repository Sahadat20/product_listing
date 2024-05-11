from django.views import generic
from django.http import JsonResponse
from django.db.models import Q, Count
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
import json

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
        # Parse the JSON data from the request body
            data = self.request.POST.dict()
            print(data)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        print(list(variants.all()))
        return context
    def post(self, request, format=None):
        # print(request.data)
        data = self.request.POST
        product_data = json.loads(request.body)
        product_name = product_data['name']
        product_sku = product_data['sku']
        product_description = product_data['description']
        product_varients = product_data['variants']
        product_varients_prices = product_data['variants_prices']
        product = Product.objects.create(title=product_name,sku=product_sku,description=product_description )
        all_varient_object = {}
        for input_varient in product_varients:
            varient_id = input_varient['option']
            varient_tags = input_varient['tags']
            varient = Variant.objects.get(id=varient_id)
            print(varient)
            for tag in varient_tags:
                print(tag)
                product_varient_obj = ProductVariant.objects.create(variant_title=tag,variant=varient,product=product)
                all_varient_object[tag] = product_varient_obj
        for varient_price in product_varients_prices:
            title = varient_price['title']
            price = varient_price['price']
            stock = varient_price['stock']
            title_split = title.split('/')
            varient_one = all_varient_object[title_split[0]]
            varient_two = all_varient_object[title_split[1]]
            varient_three = all_varient_object[title_split[2]]
            ProductVariantPrice.objects.create(product_variant_one=varient_one,product_variant_two=varient_two,product_variant_three=varient_three,
                                               price=price,stock=stock,product=product)
        
        return JsonResponse({'message': 'Product saved successfully'}, status=201)
class ProductView(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True)
        all_choices = {}
        for variant in variants:
            all_choices[variant.title] =  list(variant.productvariant_set.values_list('id','variant_title'))
        print(all_choices)
        unique_choices = {}
        for key, values in all_choices.items():
            id = []
            choice = []
            for item in values:
                if item[1] not in choice:
                    choice.append(item[1])
                    id.append(item[0])
            choises_list = []
            for i in range(len(choice)):
                choises_list.append((id[i],choice[i]))
            unique_choices[key] = choises_list
        print(unique_choices)
   
        # Searching
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')
        products = Product.objects.all()
        if title:
            products = products.filter(title__icontains=title)
        if variant:
            products = products.filter(productvariantprice__product_variant_one=variant)
        if price_from:
            products = products.filter(productvariantprice__price__gte=price_from)
        if price_to:
            products = products.filter(productvariantprice__price__lte=price_to)
        if date:
            products = products.filter(created_at__date=date)
        products = products.distinct()
        
        # Edit and update
        edit_product_id = 0
        edit = self.request.GET.get('edit')
        update = self.request.GET.get('update')
        if update:
            print("=========================")
            product_id=self.request.GET.get('product_id')
            product_title=self.request.GET.get('product_title')
            product_description=self.request.GET.get('product_description')
            
            product = Product.objects.get(id=product_id)
            product.title = product_title
            product.description = product_description
            product.save()
            print(product_title)
            choice_count=self.request.GET.get('choice_count')
            for i in range(1,int(choice_count)+1):
                choice_id = self.request.GET.get('choice_id_'+str(i))
                print("+++++++++++++")
                print(choice_id)
                product_price = self.request.GET.get('product_price_'+str(i))
                product_stock = self.request.GET.get('product_stock_'+str(i))
                varient_price = ProductVariantPrice.objects.get(id=choice_id)
                varient_price.price=product_price
                varient_price.stock=product_stock
                varient_price.save()
        edit_product = self.request.GET.get('edit_product_id')
        if edit and edit_product!=0:
            edit_product_id = edit_product
            products = products.filter(id=edit_product_id)
        print(date)
        print(edit_product_id)
        context['product'] = True
        context['products'] = list(products.all())
        context['variants'] = unique_choices
        context['edit_product_id'] = edit_product_id
        print(list(products.all()))
        return context
