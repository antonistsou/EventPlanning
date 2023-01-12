from flask import Blueprint , render_template ,request
from flask_login import current_user
import  json , re
from .models import Event,Date,Result
from . import db

res = Blueprint('result' , __name__)

selected_array  = list()

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
        
        sel = list()
        final_selection = list()

        eventList=Event.query.all() 
        DateList = Date.query.all()

        # the selected integer list (data formation)
        for s in selected_array:
            for x in s:
                sel.append(x)

        flag = 0
        for s in sel:
                
            count_id+=1    

            r = Result.query.filter_by(id =count_id).first()

            result_text = str(eventList[s-1].id) + "•"+eventList[s-1].name +",  location: "+ eventList[s-1].location
                
            final_selection.append(str(eventList[s-1].id) + "•"+eventList[s-1].name +",  location: "+ eventList[s-1].location)
            for date in DateList:
                if date.event_id == eventList[s-1].id:
                    exact_date = date.day + " " + date.time
                    # print(eventList[s-1].name +" "+dat)
                    if not exact_date in final_selection:
                        result_text += "\n"+exact_date
                        final_selection.append(exact_date)
            if not r:
                    new_selection = Result(id = count_id, result =result_text, user_id=current_user.id)
                    db.session.add(new_selection)
                    db.session.commit()

        return  render_template('/result.html', user=  current_user, selected = final_selection)
    
def handle_request():
    if request.method =='POST':
        output = request.get_json()
        result = json.dumps(output)
        
        form_selected_items(result=result)


def form_selected_items(result):
    selected_array.clear()
    selected_array.append([int (s) for s  in re.findall(r'\d+',result)])
  
    
