from flask import Flask,render_template,request,redirect,abort
import time
import json

app = Flask(__name__)


@app.route("/")
def ceteleindex():
    err=request.args.get("err")
    allrec = []
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ipaddr = request.environ['REMOTE_ADDR']
    else:
        ipaddr=request.environ['HTTP_X_FORWARDED_FOR']
    
    alljson = json.loads(open("sec.json").read())
    try:
        username = alljson[ipaddr]["username"]
    except:
        username =""

    return render_template("index.html",recommendations=alljson,ctime=time.ctime,username=username,err=err)

@app.route("/recommend",methods=["POST"])
def recommend():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ipaddr = request.environ['REMOTE_ADDR']
    else:
        ipaddr=request.environ['HTTP_X_FORWARDED_FOR']


    try:
        security_json =json.loads( open("sec.json","r").read())
    except:
        security_json = {}
    try:
        oldtime = security_json[str(ipaddr)]["time"]
    except:
        oldtime= 0
    if oldtime+30>time.time():
        return abort(429)

    try:
        security_json[str(ipaddr)]["time"] = time.time()
    except:

        security_json[str(ipaddr)] = {}
        security_json[str(ipaddr)]["time"] = time.time()
    


    username=request.form.get("username").strip()
    if len(username)>20:
        username = username[:20]
    if len(username)<2:
        return redirect("/?err=2000102")
        #Username too short
    security_json[str(ipaddr)]["username"] = username

    recommendation =request.form.get("recommendation").strip()
    if len(recommendation)>500:
        recommendation = recommendation[:500]
    if len(recommendation)<30:
        return redirect("/?err=200123")
        #Recommendation too short
    
    if recommendation != None:
        try:
            
            security_json[str(ipaddr)]["recommendations"].append({"rec":recommendation,"username":username,"time":time.time()})
        except:
            security_json[str(ipaddr)]["recommendations"] = []
            
            security_json[str(ipaddr)]["recommendations"].append({"rec":recommendation,"username":username,"time":time.time()})
        open("rec.txt","a").write(f"{username}|{recommendation} - {time.ctime(time.time())}\n")

        open("sec.json","w").write(json.dumps(security_json,indent=4,ensure_ascii=False))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,port=2000)

