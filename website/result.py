from flask import Blueprint , render_template ,request
from flask_login import current_user
import  json , re
from .models import Event,Date,Result
from . import db
from ortools.linear_solver import pywraplp
from datetime import datetime

res = Blueprint('result' , __name__)

selected_numbers_array  = list()

count_id =0
@res.route('/result' , methods = ['GET' , 'POST'])
def result():
        global count_id
        id = current_user.id
        try:
            Result.query.filter_by(user_id=id).delete()
            db.session.commit()
        except:
            db.session.rollback()

        handle_request()
        
        num_array = list()
        final_selection = list()

        eventList=Event.query.all() 
        DateList = Date.query.all()

        # the selected integer list (data formation)
        for s in selected_numbers_array:
            for x in s:
                num_array.append(x)

        #the array with the selected events 
        selected_array=list()
        selected_name =list()
        for num in num_array:
           selected_array.append(eventList[num-1])
           selected_name.append(eventList[num-1].name)
           
        #the array with selected dates in every event
        Date_array=list()
        for events in selected_array:
            for date in DateList:
                if events.id == date.event_id:
                    Date_array.append(date)

        #now the constraints part         
        # Create the solver
        solver = pywraplp.Solver('EventScheduler', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        # Create variables for each event and date combination
        event_vars = {}
        date_vars = {}
        for event in selected_array:
            for date in Date_array:
                if date.event_id == event.id:
                    event_key = event.name
                    date_key = date.day.strftime("%Y-%m-%d")
                    if event_key not in event_vars:
                        event_vars[event_key] = {}
                    event_vars[event_key][date_key] = solver.BoolVar('')
                    if date_key not in date_vars:
                        date_vars[date_key] = solver.BoolVar('')

        # Add the constraint that each event can only be scheduled once
        for event_key in event_vars.keys():
            solver.Add(solver.Sum([event_vars[event_key][date_key] for date_key in event_vars[event_key].keys()]) <= 1)

        #constraint that each date is different in the result
        for date_key in date_vars.keys():
            solver.Add(solver.Sum([event_vars[event_key][date_key] for event_key in event_vars.keys() if date_key in event_vars[event_key]]) <= 1)

        # Create the objective function
        objective = solver.Maximize(solver.Sum([event_vars[event_key][date_key] for event_key in event_vars.keys() for date_key in event_vars[event_key].keys()]))

        # Solve the problem
        p = 0
        data_result = list()
        status = solver.Solve()
        if status == solver.OPTIMAL:
            # Print the solution
            for event_key in event_vars.keys():
                for date_key in event_vars[event_key].keys():
                    if event_vars[event_key][date_key].solution_value() == 1:
                        p += 1
                        print(str(p) + "." + event_key + " on " + date_key)
        else:
            print("Solver returned non-optimal solution")

            
        return  render_template('/result.html', user=  current_user, selected = final_selection)
    
def handle_request():
    if request.method =='POST':
        output = request.get_json()
        result = json.dumps(output)
        
        form_selected_items(result=result)


def form_selected_items(result):
    selected_numbers_array.clear()
    selected_numbers_array.append([int (s) for s  in re.findall(r'\d+',result)])
  
    
