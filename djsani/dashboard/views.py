from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, SPORTS
from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_manager
from djsani.emergency.models import AARec

from djzbar.utils.informix import do_sql as do_esql, get_session
from djtools.decorators.auth import group_required
from djtools.utils.date import calculate_age
from djtools.utils.database import row2dict
from djtools.utils.users import in_group

EARL = settings.INFORMIX_EARL


def emergency_information(cid, session):
    """
    returns all of the emergency contact information for any given student
    """
    ens = session.query(AARec).filter_by(id=cid).\
        filter(AARec.aa.in_(['ICE','ICE2'])).all()
    return ens

@group_required('MedicalStaff')
def home(request):
    """
    dashboard home with a list of students
    """
    students = None
    sql = '{} AND prog_enr_rec.cl IN ("FF","FR") '.format(STUDENTS_ALPHA)
    sql += "ORDER BY lastname"
    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
    session = get_session(EARL)
    if objs:
        students = [dict(row) for row in objs.fetchall()]
        for s in students:
            adult = "minor"
            if s["birth_date"]:
                age = calculate_age(s["birth_date"])
                if age > 17:
                    adult = "adult"
            s["adult"] = adult
    session.close()
    return render_to_response(
        "dashboard/home.html",
        {"students":students,"sports":SPORTS},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and (in_group(request.user,"MedicalStaff") \
      or request.user.is_superuser):
        sport = request.POST.get("sport")
        sql = " %s WHERE prog_enr_rec.cl IN (%s)" % (
            STUDENTS_ALPHA,request.POST["class"]
        )
        if sport and sport != '0':
            sql += """
                AND cc_student_medical_manager.sports like '%%%s%%'
            """ % sport
        #sql += GROUP_BY
        objs = do_esql(
            sql,key=settings.INFORMIX_DEBUG,earl=EARL
        )
        students = None
        if objs:
            students = objs.fetchall()
        return render_to_response(
            "dashboard/students_data.inc.html",
            {"students":students,"sports":SPORTS,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponse("error", content_type="text/plain; charset=utf-8")

def panels(request, session, mod, student):
    """
    Accepts data model class and student ID.
    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    data = None
    gender = student.sex
    obj = session.query(mod).filter_by(college_id=student.id).\
        filter(mod.current(settings.START_DATE)).first()
    if obj:
        if data:
            init = row2dict(obj)
            if  mod == StudentMedicalHistory:
                form = SmedForm(initial=init, gender=gender)
            if table == AthleteMedicalHistory:
                form = AmedForm(initial=init, gender=gender)
    t = loader.get_template("dashboard/panels/{}.html".format(mod.__name__)
    c = RequestContext(request, {'data':data,'form':form})
    return t.render(c)

@group_required('MedicalStaff')
def student_detail(request,cid=None,content=None):
    """
    main method for displaying student data
    """
    template = "dashboard/student_detail.html"
    if content:
        template = "dashboard/student_print_%s.html" % content
    my_sports = None
    if not cid:
        # search form
        cid = request.POST.get("cid")
    if cid:
        # get manager, just to be certain it exists
        session = get_session(EARL)
        man = get_manager(session, cid)
        # get student
        obj = do_esql(
            "{} WHERE id_rec.id = '{}'".format(STUDENT_VITALS,cid),
            key=settings.INFORMIX_DEBUG,earl=EARL
        )
        if obj:
            student = obj.fetchone()
            if student:
                try:
                    age = calculate_age(student.birth_date)
                except:
                    age = None
                ens = emergency_information(cid, session)
                shi = panels(
                    request, session, StudentHealthInsurance, student
                )
                smh = panels(
                    request, session, StudentMedicalHistory, student
                )
                amh = panels(
                    request, session, AthleteMedicalHistory, student
                )
                # used for staff who update info on the dashboard
                stype = "student"
                if student.athlete:
                    stype = "athlete"
                if student.sports:
                    my_sports = student.sports.split(",")
                if student.sex == "F":
                    sports = SPORTS_WOMEN
                else:
                    sports = SPORTS_MEN
            else:
                age=ens=shi=smh=amh=student=sports=stype=None
            return render_to_response(
                template,
                {
                    "student":student,"age":age,"ens":ens,
                    "shi":shi,"amh":amh,"smh":smh,"cid":cid,
                    "switch_earl": reverse_lazy("set_type"),
                    "sports":sports, "my_sports":my_sports,
                    "stype":stype
                },
                context_instance=RequestContext(request)
            )
        else:
            raise Http404
    else:
        raise Http404

