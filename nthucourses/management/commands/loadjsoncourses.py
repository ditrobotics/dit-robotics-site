import json

from django.core.management.base import BaseCommand, CommandError

from nthucourses.models import Course, Syllabus, Department


class Command(BaseCommand):
    args = '<jsonfile>'
    help = 'Update course data from json file'

    def progress_iter(self, seq, msg):
        total = len(seq)
        width = len(str(total))
        for n, item in enumerate(seq, start=1):
            yield item
            self.stdout.write(
                '{msg}({n:{width}}/{total:{width}})'.format(
                    msg=msg, n=n, width=width, total=total,
                ),
                ending='\r',
            )
        self.stdout.write('')

    def delete_all(self, model):
        while model.objects.count() >= 1000:
            model.objects.latest('id').delete()
            self.stdout.write('Deleteing...{:5}'.format(model.objects.count()), ending='\r')
        model.objects.all().delete()
        self.stdout.write('Deletion completed.')

    def handle(self, jsonfile, **options):
        with open(jsonfile) as file:
            self.jsondata = json.load(file)
        # self.update_courses()
        self.update_departments()

    def update_courses(self):
        self.delete_all(Course)
        for course in self.progress_iter(
            self.jsondata['courses'].values(),
            'Writing course...'
        ):
            Course.objects.create(
                time=''.join(course['time']),
                number=course['no'],
                capabilities=course['capabilities'],
                credit=course['credit'],
                enrollment=course['enrollment'],
                instructor=course['instructor'],
                room=course['room'],
                title_en=course['title_en'],
                title_zh=course['title_zh'],
                note=course['note'],
            )

    def update_departments(self):
        self.delete_all(Department)
        for department in self.progress_iter(
            self.jsondata['departments'].values(),
            'Writing department...',
        ):
            deprow = Department.objects.create(
                name_zh=department['name'],
                name_en=department['name_en'],
            )
            for course_number in department['curriclum']:
                deprow.courses.add(Course.objects.get(number=course_number))
            deprow.save()
