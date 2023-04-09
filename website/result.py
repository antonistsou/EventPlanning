from flask import Blueprint , render_template ,request
from flask_login import current_user
import  json , re, requests
from .models import Event,Date,Result
from . import db
from ortools.linear_solver import pywraplp
from datetime import datetime
from sqlalchemy.orm import sessionmaker

res = Blueprint('result' , __name__)

keys = list()
values = list()

count_id =0
@res.route('/result' , methods = ['GET' , 'POST'])
def result():

    id = current_user.id
    if request.method =='POST':
         
        result = list()
        weight = {}
        global count_id
        
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
    
        # the array with the selected events 
        selected_array=list()

        for num in sorted_weight.keys():
            for i in range(len(eventList)):
                if num == eventList[i].id:
                    selected_array.append(eventList[i])
           
        #the array with selected dates in every event
        Date_array=list()
        for events in selected_array:
            for date in DateList:
                if events.id == date.event_id:
                    Date_array.append(date)
        
        values_prior=list()
        for p in sorted_weight.values():
            values_prior.append(p)
        
        #Create the solver
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
            
        #Add the constraint that each event can only be scheduled once
        for event_key in event_vars.keys():
            solver.Add(solver.Sum([event_vars[event_key][date_key] for date_key in event_vars[event_key].keys()]) <= 1)
            
        #Constraint that demands date be different in result
        for date_key in date_vars.keys():
            solver.Add(solver.Sum([event_vars[event_key][date_key] for event_key in event_vars.keys() if date_key in event_vars[event_key]]) <= 1)
             
        # Create the objective function
        objective = solver.Objective()
        c=0
        for event_key in event_vars.keys():
            
            priority = values_prior[c] # get the priority weight for this event
            c+=1
            for date_key in event_vars[event_key].keys():
                objective.SetCoefficient(event_vars[event_key][date_key], priority) # set the coefficient for this event and date combination
            
        objective.SetMaximization()

        # Solve the problem
        p = 0
        status = solver.Solve()
        if status == solver.OPTIMAL:
            # Print the solution
            for event_key in event_vars.keys():
                for date_key in event_vars[event_key].keys():
                    if event_vars[event_key][date_key].solution_value() == 1:
                        p += 1
                        evid= Event.query.filter_by(name=event_key).first()
                        eventID=evid.id
                        obj  =  Date.query.filter_by(day=date_key).filter_by(event_id=eventID).first()
                        time = obj.time
                        result_string =str(p)+". "+ event_key + " on " + date_key +" @ " + time
                        # print( result_string)
                    
                        result.append(result_string)
                        
                        r = Result.query.filter_by(id = id).first()
                        if not r:
                            new_result = Result(result = result_string , user_id =id )
                            try:
                                db.session.add(new_result)
                            except:
                                db.session.rollback()
                                print("Raised Exeption result!!")
                                raise
        else:
            print("Solver returned non-optimal solution")
        db.session.commit()

        return  render_template('/result.html', user=  current_user, result= result)
    else:
        final_result = list()
        result = Result.query.filter_by(user_id = id).all()
        for result_item in result:
            final_result.append(result_item.result+'\n')
        return  render_template('/result.html', user=  current_user, result = final_result)

#Get from index.js Map     
def handle_request():
    
    r = list()

    keys.clear()
    values.clear()
    
    counter= 0 
    
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
  