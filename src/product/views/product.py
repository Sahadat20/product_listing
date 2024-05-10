from django.views import generic
from django.db.models import Q, Count
from product.models import Variant, Product, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        print(list(variants.all()))
        return context
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
    #     variants = Variant.objects.annotate(
    #     distinct_product_variants_count=Count('productvariant', distinct=True)
    # ).order_by('id')
        # variants = variants.filter(productvariant__variant_title__icontains='')
        # for variant in variants:
        #     print(variant.variant_title)
        # print(variants)
        # for variant in list(variants.all()):
        #     for choice in variant.productvariant_set
        #     print(variant)
        # products = Product.objects.select_related('productvariant').all()
        # title =''
        # if( self.request.GET.get('title')):
        #     title = self.request.GET.get('title')
        # print(title)
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')
        print(date)
        products = Product.objects.all()
        # products = products.filter(Q(title__icontains=title) & Q(productvariantprice__price__gte=price_from))
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
        # products = Product.objects.filter(title__icontains=title)
        # for instance in products:
        #     print(instance)
        context['product'] = True
        context['products'] = list(products.all())
        context['variants'] = unique_choices
        print(list(products.all()))
        return context
