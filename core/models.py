from django.db import models

from django.db import models

# Create your models here.
# Staff model


class Staff(models.Model):
    staff_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, blank=True)
    dob = models.DateField()
    address = models.TextField()
    discipline = models.CharField(max_length=50, blank=True)
    qualification = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=20)
    appointment_date = models.DateField()
    appointment_type = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# Parent model


class Parent(models.Model):
    parent_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=80, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name

# Grade (class) model


class Grade(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# pupil model
class Pupil(models.Model):
    pupil_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    year_of_admission = models.PositiveIntegerField()
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Grade, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='active')

    def __str__(self):
        return self.name


# first term fee model
class feeFirst(models.Model):
    pupil_id = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    academic_year = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pupil_id.name

# second term fee model


class feeSecond(models.Model):
    pupil_id = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    academic_year = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pupil_id.name

# third term fee model


class feeThird(models.Model):
    pupil_id = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    academic_year = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pupil_id.name

# announcement model


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
