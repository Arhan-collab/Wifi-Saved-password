from flask import Flask, request, redirect

app = Flask(__name__)

# CLASSES #

class Student:
    def __init__(self, name, roll, m1, m2):
        self.name = name
        self.roll = roll
        self.m1 = m1
        self.m2 = m2


class Batch:
    def __init__(self):
        self.students = []

    def accept(self, name, roll, m1, m2):
        self.students.append(Student(name, roll, m1, m2))

    def display(self):
        return self.students

    def search(self, roll):
        for s in self.students:
            if s.roll == roll:
                return s
        return None

    def delete(self, roll):
        s = self.search(roll)
        if s:
            self.students.remove(s)
            return True
        return False

    def update(self, old, new):
        s = self.search(old)
        if s:
            s.roll = new
            return True
        return False


batch = Batch()

# TEMPLATE #

def page(content):
    return f"""
    <html>
    <head>
        <title>Student Manager</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-dark text-light">

        <div class="container mt-5">
            <h2 class="mb-4 text-center">Student Management System</h2>

            <div class="d-flex justify-content-center mb-4">
                <a href="/" class="btn btn-secondary mx-2">Home</a>
                <a href="/add" class="btn btn-primary mx-2">Add</a>
                <a href="/display" class="btn btn-info mx-2">Display</a>
                <a href="/search" class="btn btn-warning mx-2">Search</a>
                <a href="/delete" class="btn btn-danger mx-2">Delete</a>
                <a href="/update" class="btn btn-success mx-2">Update</a>
            </div>

            <div class="card bg-secondary p-4 rounded">
                {content}
            </div>

        </div>

    </body>
    </html>
    """

# route ("/") #

@app.route("/")
def home():
    return page("<h4>Welcome Non-Chalant Guy Definatly not trying to mention Kushman-goyal ig / hehecat theme lol(change it later alright? lol)</h4>")


# Adding student
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        roll = int(request.form["roll"])
        m1 = int(request.form["m1"])
        m2 = int(request.form["m2"])

        batch.accept(name, roll, m1, m2)
        return redirect("/display")

    return page("""
        <h4>Add Student</h4>
        <form method="POST">
            <input class="form-control mb-2" name="name" placeholder="Name" required>
            <input class="form-control mb-2" name="roll" placeholder="Roll" type="number" required>
            <input class="form-control mb-2" name="m1" placeholder="Marks 1" type="number" required>
            <input class="form-control mb-2" name="m2" placeholder="Marks 2" type="number" required>
            <button class="btn btn-primary w-100">Add</button>
        </form>
    """)


#  display Student Data 
@app.route("/display")
def display():
    students = batch.display()
    if not students:
        return page("<h4>No students available.</h4>")

    rows = ""
    for s in students:
        rows += f"<tr><td>{s.name}</td><td>{s.roll}</td><td>{s.m1}</td><td>{s.m2}</td></tr>"

    return page(f"""
        <h4>All Students</h4>
        <table class="table table-dark table-striped">
            <tr><th>Name</th><th>Roll</th><th>Marks 1</th><th>Marks 2</th></tr>
            {rows}
        </table>
    """)


# Search For Student
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        roll = int(request.form["roll"])
        s = batch.search(roll)
        if s:
            return page(f"""
                <h4>Student Found</h4>
                <p>Name: {s.name}</p>
                <p>Roll: {s.roll}</p>
                <p>Marks: {s.m1}, {s.m2}</p>
            """)
        else:
            return page("<h4>Student not found.</h4>")

    return page("""
        <h4>Search Student</h4>
        <form method="POST">
            <input class="form-control mb-2" name="roll" placeholder="Roll No" type="number" required>
            <button class="btn btn-warning w-100">Search</button>
        </form>
    """)


# Delete
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        roll = int(request.form["roll"])
        if batch.delete(roll):
            return redirect("/display")
        return page("<h4>Student not found.</h4>")

    return page("""
        <h4>Delete Student</h4>
        <form method="POST">
            <input class="form-control mb-2" name="roll" placeholder="Roll No" type="number" required>
            <button class="btn btn-danger w-100">Delete</button>
        </form>
    """)


# update
@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        old = int(request.form["old"])
        new = int(request.form["new"])
        if batch.update(old, new):
            return redirect("/display")
        return page("<h4>Student not found.</h4>")

    return page("""
        <h4>Update Student Roll No</h4>
        <form method="POST">
            <input class="form-control mb-2" name="old" placeholder="Old Roll" type="number" required>
            <input class="form-control mb-2" name="new" placeholder="New Roll" type="number" required>
            <button class="btn btn-success w-100">Update</button>
        </form>
    """)


# running on flask
if __name__ == "__main__":
    app.run(debug=True)
