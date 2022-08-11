from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def get_teacher_assignments(principal):
    """Returns list of assignments submitted to the teacher"""
    teacher_assignments = Assignment.get_assignments_by_teacher(principal.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_student_assignments(principal,payload):
    """grades the assignments submitted by the student"""
    submit_assignment_payload = AssignmentGradeSchema().load(payload)
    graded_assignment = Assignment.grade_assignment(submit_assignment_payload.id,
        principal.teacher_id, submit_assignment_payload.grade)
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


