from flask import Flask, render_template, request, redirect, json, url_for, session

app = Flask(__name__)  # templates/ a static/ jsou default

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Přihlášení", methods=["POST", "GET"])
def prihlaseni():
    error = None
    #jestliže je POST získá hodnoty z formuláře
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with open("app/static/data/users.json", "r") as file:
            users = json.load(file)
            
        #kontrola zadání hesla a jména v případě zadání mezery
        if username.strip()=="" or password.strip()=="":
            return redirect(url_for("auth.prihlaseni"))
        
        #uložení jména do session
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = username
                return redirect(url_for("auth.profil"))
        error = "Neznámé uživatelské jméno nebo heslo."
        return render_template("prihlaseni.html", error=error)
    else:
        #jestliže je uživatel v session je přihlášený 
        if "username" in session:
            return redirect(url_for("auth.profil"))
        else:
            return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True) 

@app.route("/Profil")
def profil():
    #kontrola jestli je uživatel v session
    if "username" in session:
        username = session["username"]
        return render_template("profil.html", username=username)
    else:
        return redirect(url_for("prihlaseni"))