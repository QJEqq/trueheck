from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView , DetailView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Brand, Transmission, DriveType, FuelType, ModelAuto, ModelAutoImage
from django.db.models import Q 


class IndexView(TemplateView):
    template_name = "main/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context["brands"] = Brand.objects.all()
        context["current_brand"] = None
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/home_content.html' , context)
        return TemplateResponse(request, self.template_name , context)
    
class CatalogView(TemplateView):
    template = 'main/base.html'

    FILLTER_MAPPING = {
        'brand': lambda queryset, value: queryset.filter(brand__slug=value),
        'min_price': lambda queryset, value: queryset.filter(price__gte=value),
        'max_price': lambda queryset, value: queryset.filter(price__lte=value),
        'min_year': lambda queryset, value: queryset.filter(year__gte=value),
        'max_year': lambda queryset, value: queryset.filter(year__lte=value),
        'transmission': lambda queryset, value: queryset.filter(transmission__type=value),
        'drive_type': lambda queryset, value: queryset.filter(drive_type__type=value),
        'fuel_type': lambda queryset, value: queryset.filter(fuel_type__type=value),
        'min_horse_power': lambda queryset, value: queryset.filter(horse_power__gte=value),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_slug = kwargs.get('brand_slug')

        brands = Brand.objects.all()
        cars = ModelAuto.objects.all().select_related(
             'brand', 'transmission', 'drive_type', 'fuel_type'
        ).prefetch_related('images')

        current_brand = None

        if brand_slug:
            current_brand = get_object_or_404(Brand, slug=brand_slug)
            cars = cars.filter(brand=current_brand)

         # ПОИСК по названию модели
        query = self.request.GET.get('q')
        if query:
            cars = cars.filter(
                Q(name__icontains=query) | 
                Q(brand__name__icontains=query)
            )

        # ПРИМЕНЯЕМ ФИЛЬТРЫ из URL-параметров
        filter_params = {}
        for param, filter_func in self.FILTER_MAPPING.items():
            value = self.request.GET.get(param)
            if value:
                cars = filter_func(cars, value)
                filter_params[param] = value
            else:
                filter_params[param] = ''

        filter_params['q'] = query or ''

        # Добавляем всё в контекст
        context.update({
            'brands': brands,
            'cars': cars,
            'current_brand': brand_slug,
            'filter_params': filter_params,
            'transmissions': Transmission.objects.all(),
            'drive_types': DriveType.objects.all(),
            'fuel_types': FuelType.objects.all(),
            'search_query': query or ''
        })

        # Для HTMX - показ/скрытие поиска
        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = True
        
        return context
    
    def get(self, request , *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                return TemplateResponse(request, 'main/search_input.html', context)
            elif context.get('reset_search'):
                return TemplateResponse(request, 'main/search_button.html', {})
            template = 'main/filter_modal.html' if request.GET.get('show_filters') == 'true' else 'main/catalog.html'
            return TemplateResponse(request, template, context)
        return TemplateResponse(request, self.template, context)
    
class CarDetailView(DetailView):
    model = ModelAuto
    template_name = 'main/base.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        
        context['brands'] = Brand.objects.all()
        
        # Похожие автомобили (той же марки)
        context['related_cars'] = ModelAuto.objects.filter(
            brand=car.brand
        ).exclude(id=car.id)[:4]
        
        context['current_brand'] = car.brand.slug
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/car_detail.html', context)
        return TemplateResponse(request, self.template_name, context) 
                
        
    


