from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required  

from .tg_client import *
from .tasks import *
from .models import *
from TEOC.settings import TG_LOGGING
# import logging
# import logging.config

def get_request_modal_context(status,context):
    if status == NEED_CODE_REQUEST:
        context['request_code'] = True
        return context
    elif status == NEED_PASSWORD:
        context['request_password'] = True
        return context
    elif status == SUCCESS:
        context['succes'] = True
        return context



@login_required
def parser_manager(request):
    context = {'title': 'Добавление Краулера'}
    config = "client/config.ini"
    context['session_name'], context['api_id'], context['api_hash'], context[
        'phone'] = parse_config(config)
    if request.POST:
        if request.POST.get('create_flag'):
            parser = Parser.objects.get_or_create(
                user=User.objects.get(id=request.user.id),
                api_id=request.POST.get('api_id'),
                api_hash=request.POST.get('api_hash'),
                phone=request.POST.get('phone'),
                session=request.POST.get('session'),
            )[0]
            context['parser_id'] = parser.id
            task = auth_telegram.delay(parser.id)
            status = task.wait(timeout=None, interval=0.5)
            context = get_request_modal_context(status,context)
            if context.get('succes'):
                return redirect('parsers')
            return render(request, 'client/manager.html', context)
        elif request.POST.get('code'):
            task = auth_telegram.delay(
                request.POST.get('parser_id'),
                code = request.POST.get('code'),
                password = request.POST.get('password')
                )
            status = task.wait(timeout=None, interval=0.5)
            context = get_request_modal_context(status,context)
            if context.get('succes'):
                return redirect('parsers')
    return render(request, 'client/manager.html', context)


class parsers_listview(ListView):
    model = Parser
    template_name = 'client/parsers.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Пауки'
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get('run'):
            channels = [channel.url for channel in Tg_Channels.objects.all()]
            if not channels:
                return redirect('tg_channels')
            get_documents.delay(request.POST.get('id'),channels=channels)
        if request.POST.get('del'):
            Parser.objects.get(id=request.POST.get('id')).delete()
        if request.POST.get('auto'):
            parser = Parser.objects.get(id=request.POST.get('id'))
            parser.auto = True
            parser.save()
        return redirect('parsers')



@method_decorator(csrf_exempt, name='dispatch')
class tg_channels_listview(ListView):
    model = Tg_Channels
    template_name= 'client/tg_channels.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Телеграмм каналы'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') and not request.POST.get('url'):
            return redirect('tg_channels')
        if request.POST.get('action')=='save':
            Tg_Channels.objects.get_or_create(url = request.POST.get('url'))
        if request.POST.get('action')=='del':
            channel = Tg_Channels.objects.get(url = request.POST.get('url'))
            if not channel:
                return redirect('tg_channels')
            else:
                channel.delete()
        return redirect('tg_channels')
           

