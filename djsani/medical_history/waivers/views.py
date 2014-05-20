from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.waivers.forms import MeniForm
from djsani.medical_history.waivers.forms import PrivacyForm
from djsani.medical_history.waivers.forms import ReportingForm
from djsani.medical_history.waivers.forms import RiskForm
from djsani.medical_history.waivers.forms import SicklecellForm
from djsani.core.views import get_data, put_data, update_manager

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NEXT_YEAR

@portal_login_required
def form(request,stype,wtype):
    cid = request.session["cid"]
    table = "cc_%s_%s_waiver" % (stype,wtype)
    manager = get_data("cc_student_medical_manager",cid).fetchone()
    # check to see if they already submitted this form
    if manager[table]:
        return HttpResponseRedirect(
            reverse_lazy("home")
        )
    # form name
    fname = "%sForm" % wtype.capitalize()
    if request.method=='POST':
        form = eval(fname)(request.POST)
        form.is_valid()
        data = form.cleaned_data
        # insert
        data["cid"] = cid
        put_data(data,table,noquo=["cid"])
        # update the manager
        update_manager(table,cid)
        return HttpResponseRedirect(
            reverse_lazy("waiver_success")
        )
    else:
        form = eval(fname)
    return render_to_response(
        "medical_history/waivers/%s_%s.html" % (stype,wtype),
        {
            "form":form,"next_year":NEXT_YEAR,
        },
        context_instance=RequestContext(request)
    )
