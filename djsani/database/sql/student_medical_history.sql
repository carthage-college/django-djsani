SELECT
    college_id
FROM
    cc_student_medical_manager
WHERE
    cc_student_medical_history=1
AND
    college_id
NOT IN (
    select college_id from cc_student_medical_history
);
