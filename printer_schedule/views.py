from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone

from printer_schedule.models import PrinterSchedule


class ScheduleIndex(ListView):
    template_name = 'printer_schedule/listing.html'
    queryset = PrinterSchedule.objects.filter(time_ended__isnull=True)
    context_object_name = 'schedule_list'


class ScheduleArchive(ListView):
    template_name = 'printer_schedule/archive.html'
    queryset = PrinterSchedule.objects.filter(time_ended__isnull=False)
    context_object_name = 'schedule_list'


class ScheduleCreate(CreateView):
    template_name = 'printer_schedule/create.html'
    model = PrinterSchedule
    fields = ('purpose', 'important', 'gcode_file', 'est_duration')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.submitter = self.request.user
        instance.save()
        return redirect('printer_schedule:index')


class ScheduleStart(UpdateView):
    model = PrinterSchedule
    fields = ()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.time_started = timezone.now()
        instance.started_by = self.request.user
        instance.save()
        return redirect('printer_schedule:index')


class ScheduleEnd(UpdateView):
    model = PrinterSchedule
    fields = ()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.time_ended = timezone.now()
        instance.ended_by = self.request.user
        instance.save()
        return redirect('printer_schedule:index')
