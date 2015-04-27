from django.conf import settings

# e.g. 2015-05-01 00:00:00
START_DATE = settings.START_DATE.strftime("%Y-%m-%d %H:%M:%S")

#stu_serv_rec.yr   =   YEAR(TODAY)

STUDENTS_ALPHA = """
SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id,
    profile_rec.birth_date,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_acad_rec    ON  id_rec.id   =   stu_acad_rec.id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
    AND
        cc_student_medical_manager.created_at > "{}"
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
WHERE
    prog_enr_rec.subprog    NOT IN  ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
    AND prog_enr_rec.lv_date    IS  NULL
    AND prog_enr_rec.acst   IN  ("GOOD","LOC","PROB","PROC","PROR","READ","RP","SAB","SHAC","SHOC","TRAD")
    AND stu_acad_rec.sess   IN  ("RA","RC","AM","GC","PC","TC")
    AND stu_acad_rec.reg_hrs    >   0
""".format(START_DATE)

GROUP_BY = """
GROUP BY
    lastname, firstname, id_rec.id, athlete, sports,
    cc_student_medical_history, cc_student_health_insurance,
    cc_student_meni_waiver, cc_student_immunization,
    cc_athlete_medical_history, cc_athlete_privacy_waiver,
    cc_athlete_reporting_waiver, cc_athlete_risk_waiver,
    cc_athlete_sicklecell_waiver, waive, proof, results
"""

STUDENT_VITALS = """
SELECT
    UNIQUE
    CASE NVL(UPPER(stu_serv_rec.bldg), '')
        WHEN
            'CMTR'
        THEN
            'Commuter'
        ELSE
            'Resident'
        END
    AS
        residency_status,
    id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,adm_rec.plan_enr_yr,
    cc_student_medical_manager.athlete, cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    cc_athlete_privacy_waiver.ncaa_tool,
    cc_athlete_privacy_waiver.medical_insurance,
    cc_athlete_privacy_waiver.news_media,
    cc_athlete_privacy_waiver.parents_guardians,
    cc_athlete_privacy_waiver.disclose_records,
    profile_rec.birth_date,
    profile_rec.sex,
    mobile_rec.phone as mobile
FROM
    id_rec
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
    AND
        cc_student_medical_manager.created_at > "{}"
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
LEFT JOIN
    cc_athlete_privacy_waiver ON id_rec.id = cc_athlete_privacy_waiver.college_id
    AND
        cc_athlete_privacy_waiver.created_at > "{}"
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec  ON  id_rec.id = stu_serv_rec.id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
""".format(START_DATE, START_DATE)