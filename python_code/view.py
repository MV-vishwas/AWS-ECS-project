from flask import * 
import jwt
import datetime
from functools import wraps
import boto3
from boto3.dynamodb.conditions import Key,Attr

app = Flask(__name__) #creating the Flask class object   
app.config['SECRET_KEY']='TheSecretKeyCanBeAnyThingAsYouWish'


def vaild_token():
    try:
        if session['uname']:
            # token=session['token']    
            try:
                token=session['token']
                data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            except Exception as e:
                session.pop('uname')
                session.pop('userID')
    except:
        pass


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):

        if 'token' not in session:
            return render_template('login.html',data={'error_msg':"Invalid Username or password"}),401
        token=session['token']     
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        except Exception as e:
            # print(e,token)
            # return jsonify({'response:'token is invalid'}),403
            # session.pop('uname')
            # print('pop out/N fire')
            return render_template('login.html',data={'error_msg':"Invalid Username or password"}),401
        return f(*args,**kwargs)

    return decorated


############# Form ##################
@app.route('/login_form')
def login_form():
    return render_template('login.html')

@app.route('/add_book_form')
def add_book_form():
    return render_template('add_book_form.html')

@app.route('/update_book_form')
def update_book_form():

    return render_template('update_book_form.html')

@app.route('/filter_form')
def filter_form():
    return render_template('filter_form.html')

################# FORM #################








@app.route('/check',methods=['POST'])
def check(): #checking login Creadetial
    uname = request.form['uname']
    passwd = request.form['passwd']
    table_name='users'
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
    response = ddb.query(KeyConditionExpression=Key('userID').eq(uname))
    response=response['Items']
    # print(response)
    if len(response)==0:
        return  jsonify({'response':'user ID or password is invalid.'}),401

    if passwd ==str(response[0]['password']):
        # print('if tree')
        token=jwt.encode({'user':uname,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        # print(token)
        session['token']=token
        session['uname']=str(response[0]['full_name'])
        session['userID']=response[0]['userID']
        return redirect('/'),200
    return  jsonify({'response':'user ID or password is invalid.'}),401
    
 
@app.route('/')  
def home():  
    import boto3
    from boto3.dynamodb.conditions import Key,Attr
    table_name='data'
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table('data')
    response= ddb.scan(FilterExpression=Attr('title').begins_with("A") | Attr('title').begins_with("Harry Potter"))
    data=response['Items']
    vaild_token()
    return render_template('home.html',data=data),200    




@app.route('/get_books',methods=['GET','POST']) 
def get_books():  
    key=request.form['condition']
    value=request.form['value']
    s_page=request.form['start_page']
    page_size=request.form['page_size']
    table_name='data'
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
    # print(key=='title')
    # print(key,'title')
    if key=='title':
        # if len(key)<=2 or key.a 
        response= ddb.scan(FilterExpression=Attr('title').contains(value))

        # print(response['Items'])

    elif key=='authors':
        response= ddb.scan(FilterExpression=Attr('authors').contains(value))
        # print(response['Items'])


    elif key=='average_rating':
        response= ddb.scan(FilterExpression=Attr('average_rating').begins_with(value))
        # print('yup')
        # print(response['Items'])

        
    elif key=='isbn':
        response= ddb.scan(FilterExpression=Attr('isbn').eq(value))
        # print(response['Items'])

        
    elif key=='language_code':
        response= ddb.scan(FilterExpression=Attr('language_code').eq(value))
        # print(response['Items'])

        
    elif key=='rating_count':
        response= ddb.scan(FilterExpression=Attr('ratings_count').eq(value))
        # print(response['Items'])




    if len(s_page)==0:s_page=0
    else:s_page=int(s_page)

    if len(page_size)==0:page_size=0
    else:page_size=int(page_size)
    
    if s_page>0 :skip=(s_page-1)*page_size
    else:skip=0
    count=0

    if s_page==0 and page_size==0 or page_size==0:
        # print('gttt')
        main_dict={}
        l1=[]
        for item in response['Items']:
            d1={"bookID":str(item['bookID']),"title":str(item['title']),"authors":str(item['authors']),"average_rating":str(item['average_rating']),"isbn":str(item['isbn']),"language_code":str(item['language_code']),"ratings_count":str(item['ratings_count']),"price":str(item['price'])}
            l1.append(d1)
        main_dict[1]=l1


    else:
        main_dict={}
        current_size=0
        l1=[]
        l1_count=0
        for item in response['Items']:
            count+=1
            if count>=skip:
                if current_size==page_size:
                    # print(l1)
                    l1_count+=1
                    main_dict[l1_count]=l1
                    # print(l1_count)
                    current_size=0
                    l1=[]
                d1={"bookID":str(item['bookID']),"title":str(item['title']),"authors":str(item['authors']),"average_rating":str(item['average_rating']),"isbn":str(item['isbn']),"language_code":str(item['language_code']),"ratings_count":str(item['ratings_count']),"price":str(item['price'])}
                
                l1.append(d1)
                current_size+=1
        # print(l1)
        # print(l1_count)
        if len(l1)>0:main_dict[l1_count+1]=l1
    
    
    try:
        return jsonify({'response':main_dict}),200
    except Exception as e:
        # print(e)
        return jsonify({'response':e}),500


@app.route('/get_book/<string:bookid>',methods=["GET", "POST"]) 
def getbook(bookid):  
    data={}
    # bookid=request.args['bookid']
    # return "get book called";
    # if request.method=='GET':
    try:
        table_name='data'
        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
        response = ddb.query(KeyConditionExpression=Key('bookID').eq(bookid))
        if len(response['Items'])==0:
            return jsonify({'response':'Book is not exist.'}),404
        # print(type(response['Items']))
        data=response['Items']
        # print(data)
    except Exception as e:
        # print(e)
        return jsonify({'response':e}),500
    return jsonify({'response':data}),200




@app.route('/get_favourite/<string:userid>') 
@token_required
def get_favourite(userid):
    if session['userID']!=userid:
        return jsonify({'response':f'You can access only your favourites list not other one and your user ID is {session["userID"]}'})
    try:
        table_name='users'  
        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
        response = ddb.query(KeyConditionExpression=Key('userID').eq(userid))
        fav_list=response['Items'][0]['favourites']
        # print(fav_list)

        table_name='data'
        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
        data=[]
        if len(fav_list)==0 or len(fav_list[0])==0:
            return jsonify({'response': 'No books in your favourite list'}),200
        for id in fav_list:
            print(id)
            id=str(id)
            response = ddb.query(KeyConditionExpression=Key('bookID').eq(id))
            response=response['Items'][0]
            # print(response)
            data.append(response)
        # print(data)
    except Exception as e:
        return jsonify({'response': e}),500
    return jsonify({'response': data}),200
    # return render_template('home.html',data=data)




@app.route('/add_favourite/<string:bookID>/<string:userID>')
@token_required
def add_favourite(bookID,userID): 
    if session['userID']!=userID:
        return jsonify({'response':f'You can add only your favourites list not other one and your user ID is {session["userID"]}'})
    
    try:
        userID="".join(userID.split())
        bookID=str(bookID)
        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table('data')
        response = ddb.query(KeyConditionExpression=Key('bookID').eq(bookID))
        if len(response['Items'])==0:
            return jsonify({'response': 'Book is not exist'}),404

        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table('users')
        response = ddb.query(KeyConditionExpression=Key('userID').eq(userID))
        if len(response['Items'])!=0:
            fav_list=response['Items'][0]['favourites']
            if bookID in fav_list:
                return jsonify({'response': 'Already in your wish list'}),200
            fav_list.append(bookID)
        
        key='favourites'
        value=fav_list
        ddb.update_item(Key={'userID':userID},UpdateExpression=f'SET {key} = :val1',ExpressionAttributeValues={':val1': value})    
            
        
    except Exception as e:
        return jsonify({'response': e}),402

    return jsonify({'response': 'Successfully added.'}),200





@app.route('/remove_favourite/<string:bookID>/<string:userID>')
@token_required
def remove_favourite(bookID,userID): 
    table_name='users'
    userID="".join(userID.split())
    if session['userID']!=userID:
        return jsonify({'response':f'You can remove only from your favourites list not other one and your user ID is {session["userID"]}'})
    
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
    response = ddb.query(KeyConditionExpression=Key('userID').eq(userID))


    if len(response['Items'])!=0:
        fav_list=response['Items'][0]['favourites']
        # print(fav_list)
        if bookID not in fav_list:
            return jsonify({'response': 'Already NOT in your wish list'}),409

        fav_list.remove(bookID)
        value=fav_list
        key='favourites'
        # print(fav_list)
        try:
            ddb.update_item(Key={'userID':userID},UpdateExpression=f'SET {key} = :val1',ExpressionAttributeValues={':val1': value})    
            # ddb.update_item(key={'userID':userID},UpdateExpression='SET favourites = :val1',ExpressionAttributeValues={':val1': fav_list})
            
        except Exception as e:
            return jsonify({'response': e}),500
    
    return jsonify({'response': 'Successfully Removed.'}),200



@app.route('/add_book',methods=['POST']) #decorator drfines the   
@token_required
def add_book(): 
    bookid=request.form['bookid']
    params=request.form['params']
    # print(bookid,params)

    table_name='data'
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
    response = ddb.query(KeyConditionExpression=Key('bookID').eq(bookid))

    if len(response['Items'])!=0:
        return jsonify({'response':bookid+' Already Exsist.'}),409

    ######## checking the JSON validation #####
    if len(params)==0:
        # print('yes')
        params='{"bookID":"'+bookid+'"}'
        # print(params)
        ddb.put_item(Item=json.loads(params))    

        return jsonify({'response':bookid+' Successfully inserted.'}),201


    try:
       json.loads(params)
    except:
        return  jsonify({'response':' Invalid Json Syantax'}),422

    params='{"bookID":"'+bookid+'",'+params[1:]
    ddb.put_item(Item=json.loads(params))    

    return jsonify({'response':bookid+' Successfully inserted.'}),201

@app.route('/update_book',methods=['POST']) #decorator drfines the   
@token_required
def update_book():
    bookid=request.form['bookid']
    params=request.form['params']

    # print(params,'ee')
    # params=''.join(params.s
    # print("############",bookid,params)

    table_name='data'
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)
    response = ddb.query(KeyConditionExpression=Key('bookID').eq(bookid))

    if len(response['Items'])==0:
        return jsonify({'response':bookid+'not exsist.'}),409

    if len(params)==0:return jsonify({'response':'book ID can not change params is empty'}),400
    

    try:
        print(params)
        params=json.loads(params)
        print(params)
    except:
        return  jsonify({'response':' Invalid Json Syantax'}),422

    # print(params)
    # params=json.dumps(params)
    # print(type(params))
    for key,value in params.items():
        # print(key,value)
        ddb.update_item(Key={'bookID':bookid},UpdateExpression=f'SET {key} = :val1',ExpressionAttributeValues={':val1': value})
    # ddb.update_item(Key={'bookID': bookid},AttributeUpdates=params)


    return jsonify({'response':bookid+' Successfully Updated.'}),201

if __name__ =='__main__':  
    app.run(debug = True)  