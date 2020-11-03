from app import app
from flask import render_template, make_response, jsonify, request, session
from app.functions import *
import datetime
import calendar

@app.route('/', methods=['GET', 'POST'])



@app.route('/index', methods=['GET', 'POST'])
def index():
    data = {}
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        data["errors"] = str(e)
        return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    data["db_name"] = "automationdb"
    data["content"] = "route /" 
    data["method"] = request.args.get("page")
    if data["method"] == "departments":
        data["page"] = "type1"
    else:
        data["page"] = "type2"

    return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    
    
@app.route('/departments')
def departments():
    data = {}
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        data["errors"] = str(e)
        return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    mycursor = im.mycursor
    data["db_name"] = "automationdb"

    sql_query = \
    """
    SELECT * FROM departments
    """
    mycursor.execute(sql_query)
    data["departments"] = mycursor.fetchall() 

    return render_template('departments.j2', title='Departments', data=data, )




@app.route('/reports')
def reports():
    data = {}
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        data["errors"] = str(e)
        return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    mycursor = im.mycursor
    data["db_name"] = "automationdb"
    data["time_saved"] = []
    sql_query = \
    """
    SELECT MIN(tasks_executions.timestamp) AS min_date FROM tasks_executions
    """
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    cur_year = datetime.datetime.now().year
    if results[0]["min_date"] is None:
        min_year = cur_year
    else:
        min_year = results[0]["min_date"].year
    for year in range(min_year, cur_year + 1):
        max_month = 12
        if year == cur_year:
            max_month = datetime.datetime.now().month
        for month in range(1, max_month + 1):
            first_day = 1
            last_day = calendar.monthrange(year,month)[1]
            sql_query = \
            f"""
            SELECT sum(tasks.time_of_completion) AS time_saved
            FROM tasks_executions
            JOIN tasks
            ON tasks.id=tasks_executions.task_id
            JOIN connections_tasks_automations
            ON tasks.id=connections_tasks_automations.task_id
            WHERE tasks_executions.timestamp >= '{year}-{str(month).zfill(2)}-{str(first_day).zfill(2)}'
            AND tasks_executions.timestamp <= '{year}-{str(month).zfill(2)}-{str(last_day).zfill(2)}'
            """
            mycursor.execute(sql_query)
            results = mycursor.fetchall()
            if results[0]["time_saved"] is None:
                time_saved = 0
            else:
                time_saved = int(results[0]["time_saved"])
            data["time_saved"].append({"year":str(year),"month":str(month).zfill(2), "time_saved":time_saved})
        
    return render_template('reports.j2', title='reports', data=data)


@app.route('/workflows')
def workflows():
    data = {}
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        data["errors"] = str(e)
        return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    mycursor = im.mycursor
    data["db_name"] = "automationdb"

    sql_query = \
    """
    SELECT * FROM departments
    """
    mycursor.execute(sql_query)
    data["departments"] = mycursor.fetchall() 

    sql_query = \
    """
    select workflows.id as workflow_id, 
    workflows.name as workflow_name, 
    workflows.description as workflow_description
    from workflows 
    ORDER BY workflows.name
    """
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    data["workflows"] = {}
    for item in results:
        if data["workflows"].get(item["workflow_id"]) is None:
            data["workflows"][item["workflow_id"]] = {
                "workflow_name": item["workflow_name"],
                "workflow_description": item["workflow_description"],
            }
        sql_query = \
        f"""
        SELECT departments.id, departments.name 
        FROM connections_workflows_departments 
        JOIN departments 
        ON connections_workflows_departments.department_id = departments.id 
        WHERE connections_workflows_departments.workflow_id = {item['workflow_id']}
        ORDER BY departments.name
        """

        mycursor.execute(sql_query)
        results2 = mycursor.fetchall()
        if data["workflows"][item["workflow_id"]].get("departments") is None:
            data["workflows"][item["workflow_id"]]["departments"] = {}
        for task_id in results2:
            data["workflows"][item["workflow_id"]]["departments"][task_id["id"]] = task_id["name"]

        data["workflows"][item["workflow_id"]]["tasks"] = {}


        sql_query = \
        f"""
        SELECT tasks.*, 
        connections_tasks_automations.automation_tool_id, 
        automation_tools.name as automation_tool_name 
        FROM 
        tasks left join connections_tasks_automations 
        on tasks.id= connections_tasks_automations.task_id 
        left join automation_tools 
        on connections_tasks_automations.automation_tool_id = automation_tools.id 
        WHERE
        tasks.workflow_id = {item['workflow_id']} AND
        tasks.visibility = 'enabled'
        ORDER BY tasks.order_number
        """

        mycursor.execute(sql_query)
        results3 = mycursor.fetchall()
        for item3 in results3:
            data["workflows"][item["workflow_id"]]["tasks"][item3["id"]] = {
                "name": item3["name"],
                "time_of_completion": item3["time_of_completion"],
                "order_number": item3["order_number"],
                "automation_tool_id": item3["automation_tool_id"],
                "automation_tool_name": item3["automation_tool_name"],
            }
    sql_query = \
    """
    SELECT * FROM automation_tools
    """
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    data["automation_tools"] = results

    return render_template('workflows.j2', title='workflows', data=data)


@app.route('/automation-tools')
def automation_tools():
    data = {}
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        data["errors"] = str(e)
        return render_template('index.j2', title='Home', data=data, session=session.get("_flashes"))
    mycursor = im.mycursor
    data["db_name"] = "automationdb"

    sql_query = \
    """
    SELECT * FROM automation_tools
    """
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    data["automation-tools"] = []
    for item in results:
        data["automation-tools"].append(item["name"])
        
    return render_template('automation-tools.j2', title='automation-tools', data=data)


@app.route('/database/departments', methods=["POST", "PATCH", "DELETE"])
def database_delete_department():
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        response = {"message": f"Could not connect to database server.\n{str(e)}", "code": "FAILURE"}
        return make_response(jsonify(response), 400)
    mycursor = im.mycursor
    mydb = im.conn
    payload = request.get_json()

    if request.method == "DELETE":
        if payload.get("department_id") is None:
            response = {"message": "department_id is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        query = "DELETE FROM departments WHERE id=%s LIMIT 1"
        try:
            mycursor.execute(query, (payload['department_id'], ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

    if request.method == "PATCH":
        if payload.get("department_id") is None or payload.get("department_name") is None:
            response = {"message": "department_id or department_name is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        query = "UPDATE departments SET name=%s WHERE id=%s LIMIT 1"
        try:
            mycursor.execute(query, (payload['department_name'], payload['department_id'], ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

    if request.method == "POST":
        if payload.get("department") is None:
            response = {"message": "department is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        
        query = "SELECT * FROM departments WHERE name=%s"
        try:
            mycursor.execute(query, (payload['department'], ))
            results = mycursor.fetchall()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": f"SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)

        if len(results) != 0:
            response = {"message": f"Could not insert department {payload['department']} into database because it already exists.", "code": "FAILURE"}
            return make_response(jsonify(response), 400)

        query = "INSERT INTO departments(`id`, `name`) VALUES (null, %s)"
        try:
            mycursor.execute(query, (payload['department'], ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {'message': 'Department inserted into database', 'code': 'SUCCESS'}
        return make_response(jsonify(response), 201)

@app.route('/database/workflows', methods=["POST", "PATCH", "DELETE"])
def database_workflows():
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        response = {"message": f"Could not connect to database server.\n{str(e)}", "code": "FAILURE"}
        return make_response(jsonify(response), 400)
    mycursor = im.mycursor
    mydb = im.conn
    payload = request.get_json()

    if request.method == "POST":
        for parameter in ["name"]:
            if parameter not in payload.keys():
                response = {"message": f"'{parameter}' is not given", "code": "FAILURE"}
                return make_response(jsonify(response), 400)
        query = "INSERT INTO workflows VALUES(null, %s, '')"
        try:
            mycursor.execute(query, (payload['name'], ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)
    if request.method == "PATCH":
        for parameter in ["id", "name"]:
            if parameter not in payload.keys():
                response = {"message": f"'{parameter}' is not given", "code": "FAILURE"}
                return make_response(jsonify(response), 400)
        query = "UPDATE workflows SET name=%s WHERE id=%s LIMIT 1"
        try:
            mycursor.execute(query, (payload['name'], int(payload['id']), ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)
    if request.method == "DELETE":
        for parameter in ["id"]:
            if parameter not in payload.keys():
                response = {"message": f"'{parameter}' is not given", "code": "FAILURE"}
                return make_response(jsonify(response), 400)
        query = "DELETE FROM workflows WHERE id=%s LIMIT 1"
        try:
            mycursor.execute(query, (int(payload['id']), ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)
    
@app.route('/database/tasks', methods=["POST", "PATCH", "DELETE"])
def database_tasks():
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        response = {"message": f"Could not connect to database server.\n{str(e)}", "code": "FAILURE"}
        return make_response(jsonify(response), 400)
    mycursor = im.mycursor
    mydb = im.conn
    payload = request.get_json()

    if request.method == "DELETE":
        if payload.get("id") is None:
            response = {"message": "department_id is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        query = "UPDATE tasks SET visibility='disabled' WHERE id=%s LIMIT 1"
        try:
            mycursor.execute(query, (payload['id'], ))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

    if request.method == "POST":
        if payload.get("name") is None:
            response = {"message": "name is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        if payload.get("workflow_id") is None:
            response = {"message": "workflow_id is not given", "code": "FAILURE"}
            return make_response(jsonify(response), 400)
        # calculate the order_number
        query = "SELECT max(order_number) AS max_order_number FROM tasks WHERE workflow_id = %s"
        try:
            mycursor.execute(query, (payload['workflow_id'],))
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        results = mycursor.fetchall()
        if results[0]["max_order_number"] is None:
            order_number = 1
        else:
            order_number = results[0]["max_order_number"] + 1
        query = "INSERT INTO tasks VALUES(null, %s, %s, 'enabled', %s, 0)"
        try:
            mycursor.execute(query, (int(payload['workflow_id']), payload['name'], order_number))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

    if request.method == "PATCH":
        for idx,elem in enumerate(payload):
            for item in ["id", "name", "time_of_completion", "automation_tool_id"]:
                if item not in elem.keys():
                    response = {"message": f"'{item}' is not given on row {idx}", "code": "FAILURE"}
                    return make_response(jsonify(response), 400)
        for idx,elem in enumerate(payload):
            query = "UPDATE tasks SET name=%s, visibility='enabled', order_number=%s, time_of_completion=%s WHERE id=%s LIMIT 1"
            try:
                mycursor.execute(query, (elem['name'], int(idx+1), int(elem['time_of_completion']), int(elem['id']), ))
                mydb.commit()
            except mysql.connector.errors.ProgrammingError:
                response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
                print(f"Query failed: {query}\n{mycursor.statement}")
                return make_response(jsonify(response), 400)
            query = "SELECT * FROM connections_tasks_automations WHERE task_id=%s"
            try:
                mycursor.execute(query, (int(elem['id']), ))
            except mysql.connector.errors.ProgrammingError:
                response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
                print(f"Query failed: {query}\n{mycursor.statement}")
                return make_response(jsonify(response), 400)
            results = mycursor.fetchall()
            if len(results) != 0 and len(str(elem["automation_tool_id"])) == 0:
                query = "DELETE FROM connections_tasks_automations WHERE task_id=%s LIMIT 1"
                try:
                    mycursor.execute(query, (int(elem["id"]), ))
                    mydb.commit()
                except mysql.connector.errors.ProgrammingError:
                    response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
                    print(f"Query failed: {query}\n{mycursor.statement}")
                    return make_response(jsonify(response), 400)
            if len(results) != 0 and elem["automation_tool_id"] is not None and len(str(elem["automation_tool_id"])) == 0:
                query = "DELETE FROM connections_tasks_automations WHERE task_id=%s LIMIT 1"
                try:
                    mycursor.execute(query, (int(elem["id"]), ))
                except mysql.connector.errors.ProgrammingError:
                    response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
                    print(f"Query failed: {query}\n{mycursor.statement}")
                    return make_response(jsonify(response), 400)
            if len(results) == 0 and elem["automation_tool_id"] is not None and len(str(elem["automation_tool_id"])) != 0:
                query = "INSERT INTO connections_tasks_automations VALUES(null, %s, %s)"
                try:
                    mycursor.execute(query, (int(elem["id"]), elem["automation_tool_id"],))
                    mydb.commit()
                except mysql.connector.errors.ProgrammingError:
                    response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
                    print(f"Query failed: {query}\n{mycursor.statement}")
                    return make_response(jsonify(response), 400)

        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

@app.route('/database/workflows-associations', methods=["POST", "DELETE"])
def database_workflows_associations():
    try:
        im = init_mysql()
    except mysql.connector.errors.ProgrammingError as e:
        response = {"message": f"Could not connect to database server.\n{str(e)}", "code": "FAILURE"}
        return make_response(jsonify(response), 400)
    mycursor = im.mycursor
    mydb = im.conn
    payload = request.get_json()
    print(payload)
    if request.method == "POST":
        for parameter in ["workflow_id", "department_id"]:
            if parameter not in payload.keys() or parameter is None:
                response = {"message": f"'{parameter}' is not given", "code": "FAILURE"}
                return make_response(jsonify(response), 400)
        for parameter in ["workflow_id", "department_id"]:
            if payload[parameter] is None:
                response = {"message": f"'{parameter}' must be not None", "code": "FAILURE"}
                return make_response(jsonify(response), 400)

        query = " INSERT INTO connections_workflows_departments VALUES(null, %s, %s)"
        try:
            mycursor.execute(query, (int(payload["workflow_id"]), int(payload["department_id"]),))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {query}\n{mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)
    if request.method == "DELETE":
        for parameter in ["workflow_id", "department_id"]:
            if parameter not in payload.keys():
                response = {"message": f"'{parameter}' is not given", "code": "FAILURE"}
                return make_response(jsonify(response), 400)
        query = " DELETE FROM connections_workflows_departments WHERE workflow_id=%s AND department_id=%s LIMIT 1"
        try:
            mycursor.execute(query, (int(payload["workflow_id"]), int(payload["department_id"]),))
            mydb.commit()
        except mysql.connector.errors.ProgrammingError:
            response = {"message": "SQL query resulted in an error.", "code": "FAILURE"}
            print(f"Query failed: {query}\n{mycursor.statement}")
            return make_response(jsonify(response), 400)
        response = {"message": "", "code": "SUCCESS"}
        return make_response(jsonify(response), 200)

@app.route('/database/automation-tools-associations', methods=["DELETE"])
def database_delete_automation_tools_associations():
    pass

