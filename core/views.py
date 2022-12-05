from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from .models import Announcement, Grade, Parent, Staff, Pupil, feeFirst, feeSecond, feeThird
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required


# from django.http import HttpResponse
# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa

# def render_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# pagination function
def make_pagination(model_list, page):
    paginator = Paginator(model_list, 15)
    try:
        pagination_obj = paginator.page(page)
    except PageNotAnInteger:
        pagination_obj = paginator.page(1)
    except EmptyPage:
        pagination_obj = paginator.page(paginator.num_pages)
    return pagination_obj

# **************404 Error*****************


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

# ************** 500 Errors********************


def handle_server_error(request):
    return render(request, '500.html', status=500)


# **********Index*************************
def index(request):
    announcement = Announcement.objects.latest('created_at')

    context = {
        'announcement': announcement,
    }
    return render(request, 'index.html', context)

# ***************Admin********************


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('admin_home')
        else:
            messages.info(request, 'Inavlid username or password')
            return redirect('admin_login')
    else:
        return render(request, 'admins/admin_login.html')


@login_required(login_url='admin_login')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_home(request):
    num_active_pupils = len(Pupil.objects.filter(status='active'))
    num_graduated_pupils = len(Pupil.objects.filter(status='graduated'))
    num_withdrawn_pupils = len(Pupil.objects.filter(status='withdrawn'))
    num_parents = len(Parent.objects.all())
    num_classes = len(Grade.objects.all())
    num_staff = len(Staff.objects.all())
    fee_count = len(feeFirst.objects.filter(academic_year=2022))

    context = {
        'num_active_pupils': num_active_pupils,
        'num_graduated_pupils': num_graduated_pupils,
        'num_withdrawn_pupils': num_withdrawn_pupils,
        'num_parents': num_parents,
        'num_classes': num_classes,
        'num_staff': num_staff,
        'fee_count': fee_count
    }

    return render(request, 'admins/admin_home.html', context)


# *******************Announcement*************
@login_required(login_url='admin_login')
def announcement(request):
    announcements = Announcement.objects.all().order_by('-created_at')[:6]
    context = {
        'announcements': announcements,
    }
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_announcement = Announcement.objects.create(title=title, body=body)
        new_announcement.save()
        messages.info(request, 'Announcement Posted Successfully')
        return redirect('announcement')

    return render(request, 'announcement/announcement.html', context)

# ******************Staff******************


@login_required(login_url='admin_login')
def view_staff(request):
    staff = Staff.objects.all().order_by('name')
    num_staff = len(staff)

    page = request.GET.get('page', 1)
    staff = make_pagination(staff, page)
    context = {
        'all_staff': staff,
        'num_staff': num_staff
    }
    return render(request, 'staff/view_staff.html', context)


@login_required(login_url='admin_login')
def add_staff(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        dob = str.strip(request.POST['dob'])
        address = request.POST['address']
        designation = request.POST['designation']
        qualification = request.POST['qualification']
        discipline = request.POST['discipline']
        ap_date = request.POST['ap_date']
        ap_type = request.POST['ap_type']
        sex = request.POST['sex']

        initial = 'BHA-S'
        staff_num = str(len(Staff.objects.all())+1)
        id_staff = initial + staff_num

        staff = Staff.objects.create(
            staff_id=id_staff, name=name, phone=phone,
            email=email, address=address, designation=designation, dob=dob,
            qualification=qualification, discipline=discipline,
            appointment_date=ap_date, appointment_type=ap_type, sex=sex)
        staff.save()
        messages.info(request, 'Staff ' + '"' +
                      name + '"' + ' added succesfully')
        return redirect('add_staff')

    else:
        return render(request, 'staff/add_staff.html')


@login_required(login_url='admin_login')
def staff_detail(request, id_staff):
    staff = Staff.objects.get(staff_id=id_staff)

    context = {
        'staff': staff,
    }
    return render(request, 'staff/staff_detail.html', context)


@login_required(login_url='admin_login')
def edit_staff(request, id_staff):
    staff = Staff.objects.get(staff_id=id_staff)
    context = {
        'staff': staff
    }
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        qualification = request.POST['qualification']
        discipline = request.POST['discipline']
        designation = request.POST['designation']
        ap_type = request.POST['ap_type']
        ap_date = request.POST['ap_date']
        address = request.POST['address']
        sex = request.POST['sex']
        dob = request.POST['dob']

        staff.name = name
        staff.phone = phone
        staff.email = email
        staff.designation = designation
        staff.discipline = discipline
        staff.address = address
        staff.qualification = qualification
        staff.dob = dob
        staff.appointment_date = ap_date
        staff.sex = sex
        staff.appointment_type = ap_type
        staff.save()
        messages.info(request, 'Upadted Successfully')
        return render(request, 'staff/edit_staff.html')

    else:
        return render(request, 'staff/edit_staff.html', context)


# ************Parent**********************
@login_required(login_url='admin_login')
def add_parent(request):
    if request.method == 'POST':
        parent_name = request.POST['parent_name']
        parent_phone = request.POST['parent_phone']
        parent_email = request.POST['parent_email']
        parent_address = request.POST['parent_address']
        pupil_name = request.POST['pupil_name']
        pupil_sex = request.POST['pupil_sex']
        pupil_dob = request.POST['pupil_dob']
        pupil_yoa = request.POST['pupil_yoa']
        pupil_class = request.POST['pupil_class']

        initial = 'BHA-P'
        parent_num = str(len(Parent.objects.all())+1)
        id_parent = initial + parent_num

        if Parent.objects.filter(name=parent_name, phone=parent_phone).exists():
            old_parent = Parent.objects.filter(name=parent_name).first()
            old_parent_id = old_parent.parent_id
            messages.info(
                request, 'Parent already exists, ID is ' + old_parent_id)
            return redirect('add_pupil')
        else:
            parent = Parent.objects.create(
                parent_id=id_parent, name=parent_name, phone=parent_phone,
                email=parent_email, address=parent_address)
            parent.save()

            parent_model = Parent.objects.get(
                name=parent_name, phone=parent_phone)
            pupil_class_model = Grade.objects.get(name=pupil_class)

            initial = 'BHA'
            yoa = pupil_yoa[2:]
            if pupil_sex.lower() == 'male':
                sex = '-M'
            else:
                sex = '-F'
            pupil_num = str(len(Pupil.objects.all())+1)
            id_pupil = initial + yoa + sex + pupil_num

            pupil = Pupil.objects.create(
                pupil_id=id_pupil, name=pupil_name, date_of_birth=pupil_dob,
                year_of_admission=pupil_yoa, sex=pupil_sex, parent_id=parent_model, class_id=pupil_class_model)
            pupil.save()
            msg = 'The Parent ' + '"' + parent_name+'"' + \
                ' added successfully. ID is ' + id_parent
            messages.info(request, msg)
        return redirect('add_parent')
    else:
        return render(request, 'parent/add_parent.html')


@login_required(login_url='admin_login')
def view_parent(request):
    parents_list = Parent.objects.all().order_by('name')
    num_parents = len(Parent.objects.all())

    page = request.GET.get('page', 1)
    parents = make_pagination(parents_list, page)

    context = {
        'parents': parents,
        'num_parents': num_parents
    }
    return render(request, 'parent/view_parent.html', context)


@login_required(login_url='admin_login')
def search_parent(request):
    if request.method == 'POST':
        search_key = request.POST['search_parent']
        search_key = str.strip(search_key)

        parents_list = Parent.objects.filter(
            name__icontains=search_key).order_by('name')
        num_parents = len(parents_list)

        context = {
            'parents': parents_list,
            'num_parents': num_parents
        }
        return render(request, 'parent/search_parent.html', context)
    else:
        return render(request, 'admin_home.html')


@login_required(login_url='admin_login')
def parent_detail(request, id_parent):
    parent = Parent.objects.get(parent_id=id_parent)
    pupils = Pupil.objects.filter(parent_id=parent)
    context = {
        'parent': parent,
        'pupils': pupils
    }
    return render(request, 'parent/parent_detail.html', context)


@login_required(login_url='admin_login')
def edit_parent(request, id_parent):

    parent = Parent.objects.get(parent_id=id_parent)
    context = {
        'parent': parent
    }
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']

        parent.name = name
        parent.phone = phone
        parent.email = email
        parent.address = address
        parent.save()
        messages.info(request, 'Upadted Successfully')
        return render(request, 'parent/edit_parent.html')

    else:
        return render(request, 'parent/edit_parent.html', context)


# ********************Pupil*********************
@login_required(login_url='admin_login')
def pupil(request):
    pupil_list = Pupil.objects.filter(status='active').order_by('name')
    num_pupils = len(pupil_list)

    page = request.GET.get('page', 1)
    pupils = make_pagination(pupil_list, page)

    context = {
        'pupils': pupils,
        'num_pupils': num_pupils
    }
    return render(request, 'pupil/pupil.html', context)


@login_required(login_url='admin_login')
def add_pupil(request):
    if request.method == 'POST':
        pupil_name = request.POST['pupil_name']
        pupil_sex = request.POST['pupil_sex']
        pupil_dob = request.POST['pupil_dob']
        pupil_yoa = request.POST['pupil_yoa']
        pupil_parent_id = request.POST['pupil_parent_id']
        pupil_class = request.POST['pupil_class']

        pupil_name = str.strip(pupil_name)
        pupil_dob = str.strip(pupil_dob)
        pupil_parent_id = str.strip(pupil_parent_id)

        # Genarate ID
        initial = 'BHA'
        yoa = pupil_yoa[2:]
        if pupil_sex.lower() == 'male':
            sex = '-M'
        else:
            sex = '-F'
        pupil_num = str(len(Pupil.objects.all())+1)
        id_pupil = initial + yoa + sex + pupil_num

        
        if Pupil.objects.filter(pupil_id=id_pupil).exists():
            # messages.info(request, 'Pupil already exists with the ID: ' + id_pupil)
            pupil_num = str(len(Pupil.objects.all())+2)
            id_pupil = initial + yoa + sex + pupil_num
        elif Pupil.objects.filter(pupil_id=id_pupil).exists():
            pupil_num = str(len(Pupil.objects.all())+3)
            id_pupil = initial + yoa + sex + pupil_num
        

        if pupil_sex == '':
            messages.info(request, 'Please select pupil\'s sex')
            return redirect('add_pupil')
        elif pupil_class == '':
            messages.info(request, 'Please select pupil\'s class')
            return redirect('add_pupil')
        else:
            try:
                parent_model = Parent.objects.get(parent_id=pupil_parent_id)
                pupil_class_model = Grade.objects.get(name=pupil_class)
                pupil = Pupil.objects.create(
                    pupil_id=id_pupil, name=pupil_name, date_of_birth=pupil_dob,
                    year_of_admission=pupil_yoa, sex=pupil_sex, parent_id=parent_model, class_id=pupil_class_model)
                pupil.save()
                msg = 'The Pupil '+'"' + pupil_name + '"' + \
                    ' added successfully. ID is ' + id_pupil
                messages.info(request, msg)
                
            except ObjectDoesNotExist:
                messages.info(request, 'Invaild Parent ID: ' + pupil_parent_id)

            except ValidationError as ve:
                messages.info(request, ve )

            except ValueError as ValueE:
                messages.info(request, ValueE )
            finally:               
                return redirect('add_pupil')
    else:
        return render(request, 'pupil/add_pupil.html')


@login_required(login_url='admin_login')
def view_pupil_by_class(request):
    if request.method == 'POST':
        try:
            class_name = request.POST['pupil_class']
            class_model = Grade.objects.get(name=class_name)
            pupils = Pupil.objects.filter(
                class_id=class_model, status='active').order_by('name')
            num_pupils = len(pupils)

            context = {
                'pupils': pupils,
                'class': class_name,
                'num_pupil': num_pupils
            }
            return render(request, 'pupil/pupil_class.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'Please select class below')
            return render(request, 'pupil/select_class.html')
    else:
        return render(request, 'pupil/select_class.html')


@login_required(login_url='admin_login')
def search_pupil(request):
    if request.method == 'POST':
        search_key = request.POST['search_pupil']
        search_key = str.strip(search_key)

        pupil_list = Pupil.objects.filter(
            name__icontains=search_key).order_by('name')
        num_pupils = len(pupil_list)

        context = {
            'pupils': pupil_list,
            'num_pupils': num_pupils
        }
        return render(request, 'pupil/search_pupil.html', context)
    else:
        return render(request, 'admin_home.html')


@login_required(login_url='admin_login')
def edit_pupil(request, id_pupil):

    pupil = Pupil.objects.get(pupil_id=id_pupil)
    context = {
        'pupil': pupil
    }
    if request.method == 'POST':
        name = request.POST['pupil_name']
        dob = request.POST['pupil_dob']
        yoa = request.POST['pupil_yoa']
        sex = request.POST['pupil_sex']
        pupil_class = request.POST['pupil_class']

        class_obj = Grade.objects.get(name=pupil_class)

        if class_obj.name == 'Graduated':
            pupil.status = 'graduated'
        elif class_obj.name == 'Withdrawn':
            pupil.status == 'withdrawn'
        else:
            pass

        pupil.name = name
        pupil.date_of_birth = dob
        pupil.year_of_admission = yoa
        pupil.sex = sex
        pupil.class_id = class_obj
        pupil.save()
        messages.info(request, 'Upadted Successfully')
        return render(request, 'pupil/edit_pupil.html')

    else:
        return render(request, 'pupil/edit_pupil.html', context)


@login_required(login_url='admin_login')
def pupil_detail(request, id_pupil):
    pupil = Pupil.objects.get(pupil_id=id_pupil)
    if feeFirst.objects.filter(pupil_id__pupil_id=id_pupil).exists():
        fee1 = 'Paid'
    else:
        fee1 = 'Not Paid'
    if feeSecond.objects.filter(pupil_id__pupil_id=id_pupil).exists():
        fee2 = 'Paid'
    else:
        fee2 = 'Not Paid'
    if feeThird.objects.filter(pupil_id__pupil_id=id_pupil).exists():
        fee3 = 'Paid'
    else:
        fee3 = 'Not Paid'
    context = {
        'pupil': pupil,
        'fee1': fee1,
        'fee2': fee2,
        'fee3': fee3
    }
    return render(request, 'pupil/pupil_details.html', context)


# ***************Fee*****************

@login_required(login_url='admin_login')
def fee(request):
    return render(request, 'fee/fee.html')


@login_required(login_url='admin_login')
def check_fee(request):
    if 'html' in request.POST:
        grade = request.POST['pupil_class']
        term = request.POST['term']
        year = request.POST['year']

        try:
            term_name = ''
            if term == 'fee_first':
                term_name = 'Term 1'
                fee_objs = feeFirst.objects.filter(
                    pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')
            elif term == 'fee_second':
                term_name = 'Term 2'
                fee_objs = feeSecond.objects.filter(
                    pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')
            else:
                fee_objs = feeThird.objects.filter(
                    pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')

            num_pupils = len(fee_objs)
            context = {
                'class': grade,
                'term': term_name,
                'pupils': fee_objs,
                'num_pupils': num_pupils,
                'year': year
            }
            return render(request, 'fee/check_fee.html', context)
        except ValueError:
            messages.info(request, 'Please enter a valid year')
            return redirect('fee')

    elif 'pdf' in request.POST:
        pass
        # grade = request.POST['pupil_class']
        # term = request.POST['term']
        # year = request.POST['year']

        # try:
        #     term_name = ''
        #     if term == 'fee_first':
        #         term_name = 'Term 1'
        #         fee_objs = feeFirst.objects.filter(
        #             pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')
        #     elif term == 'fee_second':
        #         term_name = 'Term 2'
        #         fee_objs = feeSecond.objects.filter(
        #             pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')
        #     else:
        #         fee_objs = feeThird.objects.filter(
        #             pupil_id__class_id__name=grade, academic_year=year).order_by('pupil_id__name')

        #     num_pupils = len(fee_objs)
        #     context = {
        #         'class': grade,
        #         'term': term_name,
        #         'pupils': fee_objs,
        #         'num_pupils': num_pupils,
        #         'year': year
        #     }
        # except ValueError:
        #     messages.info(request, 'Please enter a valid year')

        # pdf = render_pdf('fee/check_fee_pdf.html', context)
        # response = HttpResponse(pdf, content_type='application/pdf')
        # filename = grade+'.pdf'
        # content = "attachment; filename=%s" % (filename)
        # response['Content-Disposition'] = content
        # return response
    else:
        return render(request, 'fee/fee.html')


def fee_defaulter(request):
    grade = request.POST['pupil_class']
    term = request.POST['term']
    year = request.POST['year']

    if term == 'Term 1':
        paid = feeFirst.objects.filter(
            academic_year=year, pupil_id__class_id__name=grade)
    elif term == 'Term 2':
        paid = feeSecond.objects.filter(
            academic_year=year, pupil_id__class_id__name=grade)
    else:
        paid = feeThird.objects.filter(
            academic_year=year, pupil_id__class_id__name=grade)

    paid_name = []
    for paid_pupil in paid:
        paid_name.append(paid_pupil.pupil_id.name)
    defaulters = Pupil.objects.filter(class_id__name=grade).exclude(
        name__in=paid_name).order_by('name')
    num_defaulters = len(defaulters)

    context = {
        'class': grade,
        'term': term,
        'year': year,
        'defaulters': defaulters,
        'num_defaulters': num_defaulters
    }
    if 'html' in request.POST:
        return render(request, 'fee/defaulter.html', context)

    elif 'pdf' in request.POST:
        pass
        # pdf = render_pdf('fee/defaulter_pdf.html', context)
        # response = HttpResponse(pdf, content_type='application/pdf')
        # filename = grade+'.pdf'
        # content = "attachment; filename=%s" % (filename)
        # response['Content-Disposition'] = content
        # return response
    else:
        return render(request, 'fee/fee.html')


@login_required(login_url='admin_login')
def pay_id(request, id_pupil=None):
    pupil = Pupil.objects.get(pupil_id=id_pupil)
    context = {
        'pupil': pupil,
        'pupil_id': id_pupil
    }
    return render(request, 'fee/pay.html', context)


@login_required(login_url='admin_login')
def pay(request):
    return render(request, 'fee/pay.html')


@login_required(login_url='admin_login')
def pay_action(request):
    if request.method == 'POST':
        id_pupil = request.POST['pupil_id']
        year = request.POST['year']
        term = request.POST['term']
        amount = request.POST['amount']
        try:
            pupil = Pupil.objects.get(pupil_id=id_pupil)
            if term == 'fee_first':
                fee = feeFirst.objects.create(
                    pupil_id=pupil, amount=amount, academic_year=year)
            elif term == 'fee_second':
                fee = feeSecond.objects.create(
                    pupil_id=pupil, amount=amount, academic_year=year)
            else:
                fee = feeThird.objects.create(
                    pupil_id=pupil, amount=amount, academic_year=year)
            fee.save()
            messages.info(request, 'Added Succesfully')
            return redirect('pay')
        except ObjectDoesNotExist:
             messages.info(request, 'Invaild Pupil ID: '+ id_pupil)
        finally:
            return render(request, 'fee/pay.html')
          
    else:
        return render(request, 'fee.pay.html')
