from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    salary = db.Column(db.Float)
    department = db.Column(db.String(100))

    def __repr__(self):
        return f"Employee {self.id}"


@app.route('/')
@app.route('/home')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@app.route('/employees/<int:id>')
def employee_detail(id):
    employee = Employee.query.get(id)
    return render_template("employee_detail.html", employee=employee)



@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        department = request.form['department']

        employee = Employee(name=name, position=position, salary=salary, department=department)
        try:
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "При добавлении сотрудника произошла ошибка!!!"
    else:
        return render_template("add_employee.html")
    

@app.route('/employees/<int:id>/delete')
def employee_delete(id):
    employee = Employee.query.get_or_404(id)

    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "При удалении сотрудника произошла ошибка!!!"


@app.route('/employees/<int:id>/update', methods=['POST', 'GET'])
def employee_update(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.position = request.form['position']
        employee.salary = request.form['salary']
        employee.department = request.form['department']       
        try:            
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "При изменении сотрудника произошла ошибка!!!"
    else:
        
        return render_template("employee_update.html", employee=employee)    



if __name__ == '__main__':   
    with app.app_context():
        db.create_all() 
    app.run(debug=True)