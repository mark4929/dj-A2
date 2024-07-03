from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import ListView
from banks.models import Bank, Branch


# Create your views here.

class AddBank(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return TemplateResponse(request, 'banks/add_Bank.html')
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        inst_num = request.POST.get('inst_num', '')
        swift_code = request.POST.get('swift_code', '')

        context = {'name': [], 'description': [], 'inst_num': [], 'swift_code': [], 'name_value': name,
                   'description_value': description, 'inst_num_value': inst_num, 'swift_code_value': swift_code}

        if name is None or name == "":
            context['name'].append('This field is required')
        elif len(name) > 100:
            context['name'].append("Ensure this value has at most 100 characters (it has " + str(len(name)) + ")")

        if description is None or description == "":
            context['description'].append('This field is required')
        elif len(description) > 100:
            context['description'].append(
                "Ensure this value has at most 100 characters (it has " + str(len(description)) + ")")

        if inst_num is None or inst_num == "":
            context['inst_num'].append('This field is required')
        elif len(inst_num) > 100:
            context['inst_num'].append(
                "Ensure this value has at most 100 characters (it has " + str(len(inst_num)) + ")")

        if swift_code is None or swift_code == "":
            context['swift_code'].append('This field is required')
        elif len(swift_code) > 100:
            context['swift_code'].append(
                "Ensure this value has at most 100 characters (it has " + str(len(swift_code)) + ")")

        if len(context['name']) > 0 or len(context['description']) > 0 or len(context['inst_num']) > 0 or len(
                context['swift_code']) > 0:
            return TemplateResponse(request, 'banks/add_Bank.html',
                                    context=context)
        else:
            user = request.user
            bank = Bank.objects.create(name=name, description=description, inst_num=inst_num, swift_code=swift_code,
                                       owner=user)
            bank_id = bank.id
            return HttpResponseRedirect(f'/banks/{bank_id}/details/')

    HttpResponseNotAllowed(['GET', 'POST'])


class AddBranch(View):

    def get(self, request, *args, **kwargs):

        user_logged_in = request.user
        url_bank_id = self.kwargs['bank_id']

        # Check if user is logged in
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        # context = {'email_value': Branch.get_field(Branch.email).get_default()}
        context = {'email_value': 'admin@utoronto.ca'}

        # Check if bank id exists
        if Bank.objects.filter(id=url_bank_id).exists():
            bank = Bank.objects.get(id=url_bank_id)
            bank_owner = bank.owner
        else:
            return HttpResponse('404 NOT FOUND', status=404)

        # Check if logged in user is the owner of the bank
        if user_logged_in.id == bank_owner.id:
            pass
        else:
            return HttpResponse('403 FORBIDDEN', status=403)

        return TemplateResponse(request, 'banks/add_Branch.html', context=context)

    def post(self, request, *args, **kwargs):

        user_logged_in = request.user
        url_bank_id = self.kwargs['bank_id']

        # Check if user is logged in
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        # Check if bank id exists
        if Bank.objects.filter(id=url_bank_id).exists():
            bank = Bank.objects.get(id=url_bank_id)
            bank_owner = bank.owner
        else:
            return HttpResponse('404 NOT FOUND', status=404)

        # Check if logged in user is the owner of the bank
        if user_logged_in.id == bank_owner.id:
            pass
        else:
            return HttpResponse('403 FORBIDDEN', status=403)

        name = request.POST.get('name', '')
        transit_num = request.POST.get('transit_num', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        capacity = request.POST.get('capacity', '')

        context = {'name': [], 'transit_num': [], 'address': [], 'email': [], 'capacity': [],
                   'name_value': name, 'transit_num_value': transit_num, 'address_value': address,
                   'email_value': email}

        if name is None or name == "":
            context['name'].append('This field is required')
        elif len(name) > 100:
            context['name'].append("Ensure this value has at most 100 characters (it has " + str(len(name)) + ")")

        if transit_num is None or transit_num == "":
            context['transit_num'].append('This field is required')
        elif len(transit_num) > 100:
            context['transit_num'].append(
                "Ensure this value has at most 100 characters (it has " + str(len(transit_num)) + ")")

        if address is None or address == "":
            context['address'].append('This field is required')
        elif len(address) > 100:
            context['address'].append("Ensure this value has at most 100 characters (it has " + str(len(address)) + ")")

        if email is None or email == '':
            context['email'].append('This field is required')
        try:
            validate_email(email)
        except ValidationError:
            context['email'].append("Enter a valid email address")
        else:
            pass

        if capacity is None or capacity == "":
            context['capacity_value'] = None
        elif int(capacity) < 0:
            context['capacity'].append("Ensure this value is greater than or equal to 0")
            context['capacity_value'] = capacity

        if len(context['name']) > 0 or len(context['transit_num']) > 0 or len(context['address']) > 0 or len(
                context['email']) > 0 or len(context['capacity']) > 0:
            return TemplateResponse(request, 'banks/add_Branch.html',
                                    context=context)
        else:
            user = request.user

            if capacity is None or capacity == "":
                capacity = None
            else:
                capacity = int(capacity)

            branch = Branch.objects.create(name=name, transit_num=transit_num, address=address, email=email,
                                           capacity=capacity, bank=bank)
            branch_id = branch.id
            return HttpResponseRedirect(f'/banks/branch/{branch_id}/details/')

    HttpResponseNotAllowed(['GET', 'POST'])


class BankIdDetails(View):

    def get(self, request, *args, **kwargs):
        url_bank_id = self.kwargs['bank_id']

        # Check if bank id exists
        if Bank.objects.filter(id=url_bank_id).exists():
            bank = Bank.objects.get(id=url_bank_id)

            # get all branches of this bank
            data = Branch.objects.filter(bank=bank).values()

            context = {'id': url_bank_id, 'name': bank.name, 'description': bank.description,
                       'swift_code': bank.swift_code, 'inst_num': bank.inst_num, 'data': data}

            return TemplateResponse(request, 'banks/bank_Details.html', context=context)

        else:
            return HttpResponse('404 NOT FOUND', status=404)

    HttpResponseNotAllowed(['GET'])


class BranchIdDetails(View):

    def get(self, request, *args, **kwargs):

        url_branch_id = self.kwargs['branch_id']

        # Check if user is logged in
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        # Check if branch id exists
        if Branch.objects.filter(id=url_branch_id).exists():
            branch = Branch.objects.get(id=url_branch_id)
        else:
            return HttpResponse('404 NOT FOUND', status=404)

        # get branch data
        data = {"id": branch.id, "name": branch.name, "transit_num": branch.transit_num, "address": branch.address,
                "email": branch.email, "capacity": branch.capacity, "last_modified": branch.last_modified}
        return JsonResponse(data)

    HttpResponseNotAllowed(['GET'])


class AllBanks(ListView):
    model = Bank
    template_name = 'banks/bank_list.html'

    def get(self, request, *args, **kwargs):
        return super(AllBanks, self).get(request, *args, **kwargs)

    HttpResponseNotAllowed(['GET'])

class EditBranch(View):
    def get(self, request, *args, **kwargs):
        url_branch_id = self.kwargs['branch_id']

        # Check if user is logged in
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        # Check if branch id exists
        if Branch.objects.filter(id=url_branch_id).exists():
            branch = Branch.objects.get(id=url_branch_id)
        else:
            return HttpResponse('404 NOT FOUND', status=404)

        # Check if user is the owner of the corresponding bank
        bank = branch.bank
        bank_owner = bank.owner
        user_logged_in = request.user

        if user_logged_in.id == bank_owner.id:
            pass
        else:
            return HttpResponse('403 FORBIDDEN', status=403)

        # data = Branch.objects.filter(id=url_branch_id).values()
        context = {'name_value': branch.name, 'transit_num_value': branch.transit_num, 'address_value': branch.address,
                   'email_value': branch.email, 'capacity_value': branch.capacity}

        return TemplateResponse(request, 'banks/edit_Branch.html',
                                context=context)

    def post(self, request, *args, **kwargs):
        url_branch_id = self.kwargs['branch_id']

        # Check if user is logged in
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponse('401 UNAUTHORIZED', status=401)

        # Check if branch id exists
        if Branch.objects.filter(id=url_branch_id).exists():
            branch = Branch.objects.get(id=url_branch_id)
        else:
            return HttpResponse('404 NOT FOUND', status=404)

        # Check if user that's logged in is the owner of the corresponding bank
        bank = branch.bank
        bank_owner = bank.owner
        user_logged_in = request.user

        if user_logged_in.id == bank_owner.id:
            pass
        else:
            return HttpResponse('403 FORBIDDEN', status=403)

        # updated values
        name = request.POST.get('name', '')
        transit_num = request.POST.get('transit_num', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        capacity = request.POST.get('capacity', '')

        context = {'name': [], 'transit_num': [], 'address': [], 'email': [], 'capacity': [], 'name_value': branch.name,
                   'transit_num_value': branch.transit_num, 'address_value': branch.address,
                   'email_value': branch.email, 'capacity_value': branch.capacity}

        if name is None or name == "":
            context['name'].append('This field is required')
        elif len(name) > 100:
            context['name'].append("Ensure this value has at most 100 characters (it has " + str(len(name)) + ")")
        context['name_value'] = name

        if transit_num is None or transit_num == "":
            context['transit_num'].append('This field is required')
        elif len(transit_num) > 100:
            context['transit_num'].append(
                "Ensure this value has at most 100 characters (it has " + str(len(transit_num)) + ")")
        context['transit_num_value'] = transit_num

        if address is None or address == "":
            context['address'].append('This field is required')
        elif len(address) > 100:
            context['address'].append("Ensure this value has at most 100 characters (it has " + str(len(address)) + ")")
        context['address_value'] = address

        if email is None or email == '':
            context['email'].append('This field is required')
        try:
            validate_email(email)
        except ValidationError:
            context['email'].append("Enter a valid email address")
        context['email_value'] = email

        if capacity is None or capacity == "":
            context['capacity_value'] = None
        elif int(capacity) < 0:
            context['capacity'].append("Ensure this value is greater than or equal to 0")
            context['capacity_value'] = capacity

        if len(context['name']) > 0 or len(context['transit_num']) > 0 or len(context['address']) > 0 or len(
                context['email']) > 0 or len(context['capacity']) > 0:

            return TemplateResponse(request, 'banks/edit_Branch.html',
                                    context=context)
        else:
            branch.name = name
            branch.transit_num = transit_num
            branch.address = address
            branch.email = email
            if capacity is None or capacity == "":
                branch.capacity = None
            else:
                branch.capacity = int(capacity)
            branch.save()
            branch_id = branch.id
            return HttpResponseRedirect(f'/banks/branch/{branch_id}/details/')

    HttpResponseNotAllowed(['GET', 'POST'])