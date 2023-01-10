from flask import Blueprint , render_template ,request, jsonify , flash ,redirect, url_for
from flask_login import current_user
import  json , re
from .models import Event,Date

res = Blueprint('result' , __name__)

selected_array  = list()

@res.route('/result' , methods = ['GET' , 'POST'])
def result():
        handle_request()
        
        sel = list()
        final_selection=  list()
        eventList=Event.query.all() 
        DateList = Date.query.all()
        

        # the selected integer list 
        for s in selected_array:
            for x in s:
                sel.append(x)

            for s in sel:
                print (eventList[s-1].name)
                for date in DateList:
                    if date.event_id == eventList[s-1].id:
                        print (date.day)

        return  render_template('/result.html', selected = final_selection)
    
def handle_request():
    if request.method =='POST':
        output = request.get_json()
        result = json.dumps(output)
        
        form_selected_items(result=result)


def form_selected_items(result):
    selected_array.clear()
    selected_array.append([int (s) for s  in re.findall(r'\d+',result)])
  
    
