from flask import Flask, jsonify, request
from flask import send_from_directory
import psycopg2

app = Flask(__name__)

database = psycopg2.connect(database='Gym', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


@app.route('/authentication', methods=['POST'])
def authentication():
    try:
        print(request.get_json())
        data = request.get_json()
        print(data['login'])
        print(data['password'])
        database_cursor.execute(f"select name, surname, lastname from person where login = '{data['login']}' and "
                                f"password = '{data['password']}'")
        user_info = []
        for row in database_cursor:
            user_info.append(row)

        return_answer = {'answer': 'success', 'name': str(user_info[0][0]),
                         'surname': str(user_info[0][1]),
                         'lastname': str(user_info[0][2])}
        print(return_answer)
        return jsonify(return_answer)
    except IndexError:
        data = request.get_json()
        database_cursor.execute(f"select name from person where login = '{data['login']}'")
        for row in database_cursor:
            if row[0] is not None:
                return_answer = {'answer': 'incorrect password'}
                print(return_answer)
                return jsonify(return_answer)
        return_answer = {'answer': 'incorrect login'}
        print(return_answer)
        return jsonify(return_answer)


@app.route('/registration', methods=['POST'])
def registration():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute(
            "INSERT INTO person (login, password, name, surname, lastname, phone_number) "
            f"VALUES ('{data['login']}','{data['password']}',  '{data['name']}', '{data['surname']}',"
            f" '{data['lastname']}','{data['phone_number']}')")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_stages', methods=['GET'])
def all_stages():
    try:
        data = request.args
        return_answer = {}
        database_cursor.execute(f"select * from stage where person_login = '{data['login']}'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'status': row[1], 'name': row[3]})])
            number += 1
        print(return_answer)
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_previous_stages', methods=['POST'])
def all_previous_stages():
    try:
        print(request.get_json())
        data = request.get_json()
        return_answer = {}
        database_cursor.execute(f"select * from stage where person_login = '{data['login']}' and status = 'Пройден'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'status': row[1], 'name': row[3]})])
            number += 1
        print(return_answer)
        if return_answer == {}:
            return jsonify({'answer': 'fail'})
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_upcoming_stages', methods=['POST'])
def all_upcoming_stages():
    try:
        print(request.get_json())
        data = request.get_json()
        return_answer = {}
        database_cursor.execute(f"select * from stage where person_login = '{data['login']}' and status = 'Не пройден'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'status': row[1], 'name': row[3]})])
            number += 1
        print(return_answer)
        if return_answer == {}:
            return jsonify({'answer': 'fail'})
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_weeks', methods=['POST'])
def all_weeks():
    try:
        print(request.get_json())
        data = request.get_json()
        return_answer = {}
        database_cursor.execute(f"select * from week where stage_id = '{data['stage_id']}'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'number': row[1]})])
            number += 1
        print(return_answer)
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_days', methods=['POST'])
def all_days():
    try:
        print(request.get_json())
        data = request.get_json()
        return_answer = {}
        database_cursor.execute(f"select * from day where week_id = '{data['week_id']}'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'number': row[1]})])
            number += 1
        print(return_answer)
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/all_exercises', methods=['POST'])
def all_exercises():
    try:
        print(request.get_json())
        data = request.get_json()
        return_answer = {}
        database_cursor.execute(f"select id, name, weight, reps, sets from exercise where day_id = '{data['day_id']}'")
        number = 0
        for row in database_cursor:
            print(row)
            return_answer.update([(number, {'id': row[0], 'name': row[1], 'weight': row[2], 'reps': row[3],
                                            'sets': row[4]})])
            number += 1
        print(return_answer)
        return jsonify(return_answer)
    except:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/create_stage', methods=['POST'])
def create_stage():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute("select max(id) from stage")
        stage_id = 0
        for row in database_cursor:
            stage_id = 0 if row[0] is None else int(row[0]) + 1
        print(stage_id)
        database_cursor.execute(
            f"insert into stage (id, status, person_login, name) values ('{stage_id}', '{data['status']}',"
            f" '{data['login']}', '{data['name']}')")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/delete_stage', methods=['POST'])
def delete_stage():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute(f"delete from stage where id = '{data['stage_id']}'")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/create_week', methods=['POST'])
def create_week():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute("select max(id) from week")
        week_id = 0
        for row in database_cursor:
            week_id = 0 if row[0] is None else int(row[0]) + 1
        print(week_id)
        database_cursor.execute(
            f"insert into week (id, number, stage_id) values ('{week_id}', '{data['number']}', '{data['stage_id']}')")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/delete_week', methods=['POST'])
def delete_week():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute(f"delete from week where id = '{data['week_id']}'")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/create_day', methods=['POST'])
def create_day():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute("select max(id) from day")
        day_id = 0
        for row in database_cursor:
            day_id = 0 if row[0] is None else int(row[0]) + 1
        print(day_id)
        database_cursor.execute(
            f"insert into week (id, number, week_id) values ('{day_id}', '{data['number']}', '{data['week_id']}')")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/delete_day', methods=['POST'])
def delete_day():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute(f"delete from day where id = '{data['day_id']}'")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/create_exercise', methods=['POST'])
def create_exercise():
    try:
        print(request.get_json())
        data = request.get_json()
        database_cursor.execute("select max(id) from exercise")
        day_id = 0
        for row in database_cursor:
            day_id = 0 if row[0] is None else int(row[0]) + 1
        print(day_id)
        database_cursor.execute(
            f"insert into exercise (id, name, day_id, weight, reps, sets) values"
            f" ({day_id}', '{data['name']}', {data['day_id']}, {data['weight']}, {data['reps']}, {data['sets']})")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/delete_exercise', methods=['POST'])
def delete_exercise():
    try:
        print(request.get_json())
        data = request.get_json()

        database_cursor.execute(f"delete from exercise where id = '{data['exercise_id']}'")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


if __name__ == "__main__":
    app.run(debug=True)
