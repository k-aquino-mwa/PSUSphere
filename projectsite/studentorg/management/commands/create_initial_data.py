from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember
import random


class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_colleges()
        self.create_programs()
        self.create_organization(10)
        self.create_students(50)
        self.create_membership(30)

    def create_colleges(self):
        colleges = ["College of Engineering", "College of Business", "College of Arts"]
        for name in colleges:
            College.objects.get_or_create(college_name=name)

    def create_programs(self):
        colleges = College.objects.all()
        programs = ["BSIT", "BSCS", "BSBA", "BSA"]

        for college in colleges:
            for prog in programs:
                Program.objects.get_or_create(
                    prog_name=prog,
                    college=college
                )

    def create_organization(self, count):
        fake = Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            organization_name = ' '.join(words)

            Organization.objects.create(
                name=organization_name.title(),
                college=random.choice(College.objects.all()),
                description=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS(
            'Organizations created successfully.'
        ))

    def create_students(self, count):
        fake = Faker('en_PH')

        for _ in range(count):
            Student.objects.create(
                student_id=f"{fake.random_int(2020,2025)}-{fake.random_int(1,8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=random.choice(Program.objects.all())
            )

        self.stdout.write(self.style.SUCCESS(
            'Students created successfully.'
        ))

    def create_membership(self, count):
        fake = Faker()

        for _ in range(count):
            OrgMember.objects.create(
                student=random.choice(Student.objects.all()),
                organization=random.choice(Organization.objects.all()),
                date_joined=fake.date_between(
                    start_date="-2y",
                    end_date="today"
                )
            )

        self.stdout.write(self.style.SUCCESS(
            'Memberships created successfully.'
        ))
