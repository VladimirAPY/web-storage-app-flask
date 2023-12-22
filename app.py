from flask import Flask, render_template, request, redirect
import db_manage

app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    number = request.args.get("search")
    number = number.replace(" ", "")
    numbers = number.split(",")
    numberss = list(map(int, numbers))
    result_lines = []
    places = []

    # Получаем строки с номерами комплектов из логов
    for num in numbers:
        with open("log.txt", "r") as F:
            file = reversed(F.readlines())
            for line in file:
                if str(num) in line:
                    result_lines.append(line)
    # Ищем места в базе данных и заполняем ими массив результата
    for num in numbers:
        places += db_manage.db_search(num,)
    results = [list(a) for a in zip(numberss, places)]

    return render_template("search.html", result_lines=result_lines, results=results)


@app.route("/add", methods=["POST"])
def add():
    place = request.form.get("place")
    number = request.form.get("number")
    if not place or not number:
        return render_template("failure.html")

    if db_manage.new_place(place, number) is False:
        return redirect("/failure")
    else:
        return redirect("/history")


@app.route("/table")
def table():
    places = db_manage.get_all()
    places2 = []
    places3 = []
    f = len(places) // 3
    le = len(places)

    for i in range(le, f, -1):
        if le >= i > le - f:
            places3.append(places.pop())
        else:
            places2.append(places.pop())
    places2 = reversed(places2)
    places3 = reversed(places3)

    return render_template("table1.html", places=places, places2=places2, places3=places3)


@app.route("/history")
def history():
    with open("log.txt", "r") as F:
        log = reversed(F.readlines())
        return render_template("history.html", log=log)


@app.route("/delete", methods=["POST"])
def delete():

    if request.method == "POST":
        number = request.form.get('number')
        db_manage.db_delete(number)
        return redirect("/history")


@app.route("/failure")
def failure():
    return render_template("/failure.html")
