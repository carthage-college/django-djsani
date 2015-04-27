from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_method

import datetime
NOW = datetime.datetime.now()

Base = declarative_base()

class StudentMedicalHistory(Base):
    __tablename__ = 'cc_student_medical_history'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # medical history fields
    allergies_medical = Column(String)
    allergies_other = Column(String)
    anemia = Column(String)
    anxiety = Column(String)
    bronchospasm = Column(String)
    adhd_add = Column(String)
    birth_defect = Column(String)
    blood_disorder = Column(String)
    bronchitis = Column(String)
    cancer = Column(String)
    chicken_pox = Column(String)
    counseling = Column(String)
    depression = Column(String)
    diabetes = Column(String)
    eating_disorder = Column(String)
    ent_disorder = Column(String)
    headaches = Column(String)
    head_injury = Column(String)
    heart_condition = Column(String)
    hepatitis = Column(String)
    hernia = Column(String)
    hyper_tension = Column(String)
    hiv_aids = Column(String)
    hospitalizations = Column(String)
    ibd = Column(String)
    kidney_urinary = Column(String)
    medications = Column(String)
    meningitis = Column(String)
    mononucleosis = Column(String)
    mrsa = Column(String)
    organ_loss = Column(String)
    pneumonia = Column(String)
    rheumatic_fever = Column(String)
    seizure_disorder = Column(String)
    stroke = Column(String)
    substance_abuse = Column(String)
    thyroid_disorder = Column(String)
    tuberculosis = Column(String)
    other_condition = Column(String)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current medical history for academic year?"""
        return self.created_at > day


class AthleteMedicalHistory(Base):
    __tablename__ = 'cc_athlete_medical_history'

    # core
    id = Column(BigInteger, primary_key=True)
    college_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW, nullable=False)
    # athlete medical history
    exertional_syncope       = Column(String)
    heat_illness             = Column(String)
    intense_chest_pain       = Column(String)
    sickle_cell_trait        = Column(String)
    concussion               = Column(String)
    suspected_concussion     = Column(String)
    head_injuries            = Column(String)
    season_ending            = Column(String)
    cervical_injury          = Column(String)
    stinger_injury           = Column(String)
    neurologist_treatment    = Column(String)
    spine_injury             = Column(String)
    history_headaches        = Column(String)
    history_migraines        = Column(String)
    abdomen_injury           = Column(String)
    rib_injury               = Column(String)
    lumbar_injury            = Column(String)
    shoulder_fracture        = Column(String)
    shoulder_dislocation     = Column(String)
    shoulder_muscle          = Column(String)
    labrum_injury            = Column(String)
    forearm_injury           = Column(String)
    elbow_injury             = Column(String)
    wrist_injury             = Column(String)
    finger_injury            = Column(String)
    hip_pelvis               = Column(String)
    hamstring                = Column(String)
    quadriceps               = Column(String)
    thigh_other              = Column(String)
    knee_ligaments           = Column(String)
    meniscus                 = Column(String)
    patella                  = Column(String)
    knee_other               = Column(String)
    shin_splints             = Column(String)
    stress_fractures         = Column(String)
    compartment_syndrome     = Column(String)
    lower_leg_other          = Column(String)
    ankle_fracture           = Column(String)
    ankle_sprain             = Column(String)
    foot                     = Column(String)
    toe                      = Column(String)
    glasses                  = Column(String)
    contact_lenses           = Column(String)
    hearing_aids             = Column(String)
    dental_appliances        = Column(String)
    previous_year_change     = Column(String)
    physician_prohibition    = Column(String)
    other_information        = Column(String)
    supplements              = Column(String)
    menstrual_cycle          = Column(String)

    def __repr__(self):
        return str(self.college_id)

    @hybrid_method
    def current(self, day):
        """Is this the current medical history for academic year?"""
        return self.created_at > day
