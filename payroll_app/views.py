from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

# Create your views here.

def employees(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        overtime_hours = float(request.POST.get('addOvertime'))
        employee = Employee.objects.get(pk=id_number)

        overtime = (employee.getRate() / 160) * 1.5 * overtime_hours
        if employee.overtime_pay:
            employee.overtime_pay += employee.overtime_pay + overtime
        else:
            employee.overtime_pay = overtime

        employee.save()
        return redirect("employees")
    else:
        employee_objs = Employee.objects.all()
        return render(request, 'payroll_app/employees.html',
                    {'employees': employee_objs})

def create_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exists():
            # Optional: Message errors
            return redirect('updaate_employee')
        
        if allowance == "":
            allowance = None
        
        Employee.objects.create(name=name,
                                id_number=id_number,
                                rate=rate,
                                allowance=allowance)
        return redirect('employees')
    else:
        return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    if request.method == "POST":
        pass
    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html',
                      {"e": employee})

def payslips(request):
    employee_objs = Employee.objects.all()
    payslip_objs = Payslip.objects.all()
    
    if request.method == "POST":
        payroll = request.POST.get('payroll')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cycle = request.POST.get('cycle')
        employee = Employee.objects.get(pk=payroll)
        #rate = Employee.objects.get(pk=payroll)  im not sure yet how to get the rate of the foreign key, put 1 as temp value
        Payslip.objects.create(id_number=employee, 
                               month=month, 
                               year=year,
                               pay_cycle=cycle,
                               rate=1,
                               earnings_allowance=1,
                               deductions_tax=1,
                               deductions_health=1,
                               pag_ibig=1,
                               sss=1,
                               overtime=1,
                               total_pay=1, 
                              )
        return redirect('payslips')
    else:
        
        return render(request, 'payroll_app/payslips.html',
                      {'payslips': payslip_objs, "employees": employee_objs})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/view_payslip.html',
                  {"p": payslip})

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')
