from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

mydb = mysql.connector.connect(
    host="185.87.252.147",
    user="dmlssyrl",
    passwd="190734fB@vesselam",
    database="unhelvasi_wp864"
)

# Create your views here.
def home(request):
    response = HttpResponse('Sosyorol')
    response.set_cookie('current_user', 8)
    current_uid = request.COOKIES.get('current_user')
    if current_uid is None:
        current_uid = 0
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM wpmu_usermeta WHERE user_id='{current_uid}' AND meta_key='language'")
    lang = mycursor.fetchone()
    mycursor.execute("SELECT * FROM wpmu_usermeta WHERE user_id='8' AND meta_key='language'")
    lang = mycursor.fetchone()
    mycursor.execute("SELECT * FROM languages")
    myresult = mycursor.fetchall()
    newDict = filter(lambda elem: elem['lang_code'] == 'tr-TR', myresult)
    return render(request, 'index.html', {'all_items':newDict, 'lang':lang})
