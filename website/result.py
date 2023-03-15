from flask import Blueprint , render_template ,request
from flask_login import current_user
import  json , re, requests
from .models import Event,Date,Result
from . import db
from ortools.linear_solver import pywraplp
from datetime import datetime

res = Blueprint('result' , __name__)

keys = list()
values = list()

count_id =0
@res.route('/result' , methods = ['GET','POST'])
def result():

        weight = {}

        global count_id
        id = current_user.id
        try:
            Result.query.filter_by(user_id=id).delete()
            db.session.commit()
        except:
            db.session.rollback()

        handle_request()

        for i in range(len(keys)) :
                weight[keys[i]]=values[i]

        items= list(weight.items())
        items.sort(key=lambda x: x[0])

        sorted_weight = {k: v for k, v in items}
        eventList= Event.query.all() 
        DateList = Date.query.all()


        #the array with the selected events 
        selected_array=list()

        # print(sorted_weight.keys())
        for num in sorted_weight.keys():
           selected_array.append(eventList[num-1])
           
        #the array with selected dates in every event
        Date_array=list()
        for events in selected_array:
            for date in DateList:
                if events.id == date.event_id:
                    Date_array.append(date)

        # The constraints part         
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
            
        # constraint that each date is different in the result
        for date_key in date_vars.keys():
            solver.Add(solver.Sum([event_vars[event_key][date_key] for event_key in event_vars.keys() if date_key in event_vars[event_key]]) <= 1)
            
        # Create the objective function
        c=0
        objective = solver.Objective()
        for event_key in event_vars.keys():
            for date_key in event_vars[event_key].keys():
                priority = sorted_weight[keys[c]] # get the priority weight for this event
                objective.SetCoefficient(event_vars[event_key][date_key], priority) # set the coefficient for this event and date combination
            c+=1
        objective.SetMaximization()

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

            
        return  render_template('/result.html', user=  current_user)#, selected = final_selection)
    
def handle_request():
    r = list()

    keys.clear()
    values.clear()
    
    counter= 0 
    if request.method == 'POST':
        data = request.get_json()
        map_data = json.dumps(data['map'])

        r.append([int (s) for s  in re.findall(r'\d+',map_data)])
        for i in r :
                for x in i:
                        if counter % 2==0:
                                keys.append(x)  
                        else :
                                values.append(x)
                        counter+=1

def priority_weight(priority):
    if priority == 1:
        return 3
    elif priority == 2:
        return 2
    else:
        return 1  
