from flask import Blueprint, request, jsonify, abort
from .models import db, Teacher, Course, Student, Request
from .auth import auth

api = Blueprint('api', __name__, url_prefix='/api')

def abort_if_not_found(item):
    if not item:
        abort(404)

# TEACHERS CRUD

@api.route('/teachers', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_teachers():
    all_ = Teacher.query.all()
    return jsonify([{
        'id': t.id,
        'full_name': t.full_name,
        'experience': t.experience,
        'specialty':  t.specialty,
        'department': t.department
    } for t in all_])

@api.route('/teachers/<int:id>', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_teacher(id):
    t = Teacher.query.get(id); abort_if_not_found(t)
    return jsonify({
        'id': t.id,
        'full_name': t.full_name,
        'experience': t.experience,
        'specialty':  t.specialty,
        'department': t.department
    })

@api.route('/teachers', methods=['POST'])
@auth.login_required(role='admin')
def create_teacher():
    data = request.get_json() or {}
    for f in ('full_name','experience','specialty','department'):
        if f not in data: abort(400)
    t = Teacher(**{k: data[k] for k in data})
    db.session.add(t); db.session.commit()
    return jsonify({'id': t.id}), 201

@api.route('/teachers/<int:id>', methods=['PUT','PATCH'])
@auth.login_required(role='admin')
def update_teacher(id):
    t = Teacher.query.get(id); abort_if_not_found(t)
    data = request.get_json() or {}
    for f in ('full_name','experience','specialty','department'):
        if f in data: setattr(t, f, data[f])
    db.session.commit()
    return jsonify({'id': t.id})

@api.route('/teachers/<int:id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_teacher(id):
    t = Teacher.query.get(id); abort_if_not_found(t)
    db.session.delete(t); db.session.commit()
    return jsonify({'result': True})


# COURSES CRUD

@api.route('/courses', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_courses():
    all_ = Course.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'teacher_id': c.teacher_id,
        'student_limit': c.student_limit
    } for c in all_])

@api.route('/courses/<int:id>', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_course(id):
    c = Course.query.get(id); abort_if_not_found(c)
    return jsonify({
        'id': c.id,
        'title': c.title,
        'teacher_id': c.teacher_id,
        'student_limit': c.student_limit
    })

@api.route('/courses', methods=['POST'])
@auth.login_required(role='admin')
def create_course():
    data = request.get_json() or {}
    for f in ('title','teacher_id','student_limit'):
        if f not in data: abort(400)
    c = Course(**{k: data[k] for k in data})
    db.session.add(c); db.session.commit()
    return jsonify({'id': c.id}), 201

@api.route('/courses/<int:id>', methods=['PUT','PATCH'])
@auth.login_required(role='admin')
def update_course(id):
    c = Course.query.get(id); abort_if_not_found(c)
    data = request.get_json() or {}
    for f in ('title','teacher_id','student_limit'):
        if f in data: setattr(c, f, data[f])
    db.session.commit()
    return jsonify({'id': c.id})

@api.route('/courses/<int:id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_course(id):
    c = Course.query.get(id); abort_if_not_found(c)
    db.session.delete(c); db.session.commit()
    return jsonify({'result': True})


# STUDENTS CRUD

@api.route('/students', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_students():
    all_ = Student.query.all()
    return jsonify([{
        'id': s.id,
        'full_name': s.full_name,
        'email': s.email,
        'created_at': s.created_at.isoformat()
    } for s in all_])

@api.route('/students/<int:id>', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_student(id):
    s = Student.query.get(id); abort_if_not_found(s)
    return jsonify({
        'id': s.id,
        'full_name': s.full_name,
        'email': s.email,
        'created_at': s.created_at.isoformat()
    })

@api.route('/students', methods=['POST'])
@auth.login_required(role='admin')
def create_student():
    data = request.get_json() or {}
    for f in ('full_name','email'):
        if f not in data: abort(400)
    s = Student(full_name=data['full_name'], email=data['email'])
    db.session.add(s); db.session.commit()
    return jsonify({'id': s.id}), 201

@api.route('/students/<int:id>', methods=['PUT','PATCH'])
@auth.login_required(role='admin')
def update_student(id):
    s = Student.query.get(id); abort_if_not_found(s)
    data = request.get_json() or {}
    for f in ('full_name','email'):
        if f in data: setattr(s, f, data[f])
    db.session.commit()
    return jsonify({'id': s.id})

@api.route('/students/<int:id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_student(id):
    s = Student.query.get(id); abort_if_not_found(s)
    db.session.delete(s); db.session.commit()
    return jsonify({'result': True})


# REQUESTS CRUD

@api.route('/requests', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_requests():
    all_ = Request.query.all()
    return jsonify([{
        'id': r.id,
        'student_id': r.student_id,
        'course_id':  r.course_id,
        'description': r.description,
        'status': r.status,
        'created_at': r.created_at.isoformat()
    } for r in all_])

@api.route('/requests/<int:id>', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_request(id):
    r = Request.query.get(id); abort_if_not_found(r)
    return jsonify({
        'id': r.id,
        'student_id': r.student_id,
        'course_id':  r.course_id,
        'description': r.description,
        'status': r.status,
        'created_at': r.created_at.isoformat()
    })

@api.route('/requests', methods=['POST'])
@auth.login_required(role='admin')
def create_request():
    data = request.get_json() or {}
    for f in ('student_id', 'course_id'):
        if f not in data: abort(400)

    course = Course.query.get(data['course_id'])
    abort_if_not_found(course)

    # Считаем ТОЛЬКО подтверждённые заявки
    existing_count = Request.query.filter_by(
        course_id=course.id,
        status='approved'
    ).count()
    
    if existing_count >= course.student_limit:
        return jsonify({'error': 'Course is full'}), 400

    # Проверяем существующую pending заявку
    if Request.query.filter_by(
        student_id=data['student_id'],
        status='pending'
    ).first():
        return jsonify({'error': 'Student already has a pending request'}), 400

    r = Request(
        student_id=data['student_id'],
        course_id=data['course_id'],
        description=data.get('description'),
        status=data.get('status', 'pending')
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({'id': r.id}), 201

@api.route('/requests/<int:id>', methods=['PUT','PATCH'])
@auth.login_required(role='admin')
def update_request(id):
    r = Request.query.get(id)
    abort_if_not_found(r)
    
    data = request.get_json() or {}
    new_status = data.get('status', r.status)
    new_course_id = data.get('course_id', r.course_id)

    # Validate course limit if status is approved or course_id is changed
    if new_status == 'approved' or 'course_id' in data:
        new_course = Course.query.get(new_course_id)
        if not new_course:
            abort(404)
        
        approved_count = Request.query.filter(
            Request.course_id == new_course_id,
            Request.status == 'approved',
            Request.id != r.id
        ).count()

        if new_status == 'approved':
            approved_count += 1

        if approved_count > new_course.student_limit:
            return jsonify({'error': 'Course is full'}), 400

    # Apply changes
    if 'status' in data:
        r.status = data['status']
    if 'course_id' in data:
        r.course_id = data['course_id']
    if 'description' in data:
        r.description = data['description']
    
    db.session.commit()
    return jsonify({'id': r.id})

@api.route('/requests/<int:id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_request(id):
    r = Request.query.get(id); abort_if_not_found(r)
    db.session.delete(r); db.session.commit()
    return jsonify({'result': True})
