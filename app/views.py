from flask import jsonify, request, session, redirect, url_for, render_template
from main import app  # Assuming 'main' is your Flask application object
from assets import donors  # Import 'donors' module you created for the SQLite database

@app.route('/search', methods=['POST'])
def search_donor():
    # Get the search criteria from the request
    data = request.get_json()
    name = data.get("name")
    dob = data.get("dob")
    adhar = data.get("aadhaar")
    nationality = data.get("nationality")
    state = data.get("state")
    address = data.get("address")
    blood_type = data.get("bloodType")
    contact_phone = data.get("contactPhone")

    # Initialize a list to store the results
    search_results = []

    # Read all donors from the database
    donors_ = donors.read_donor()

    # Search individually for each field
    for donor in donors_:
        if (name is None or name.lower() in donor["name"].lower()) and \
           (dob is None or dob.lower() in donor["dob"].lower()) and \
           (adhar is None or adhar.lower() in donor["adhar"].lower()) and \
           (nationality is None or nationality.lower() in donor["nationality"].lower()) and \
           (state is None or state.lower() in donor["state"].lower()) and \
           (address is None or address.lower() in donor["address"].lower()) and \
           (blood_type is None or blood_type.lower() in donor["blood_type"].lower()) and \
           (contact_phone is None or contact_phone.lower() in donor["contact_phone"].lower()):
            search_results.append(donor)

    if len(search_results) == 0:
        return jsonify({"message": "No results found!"}), 200

    return jsonify({"message": "ok", "results": search_results}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    dob = data.get("dob")
    adhar = data.get("aadhaar")
    nationality = data.get("nationality")
    state = data.get("state")
    address = data.get("address")
    blood_type = data.get("bloodType")
    contact_phone = data.get("contactPhone")
    print(data)

    # Perform input validation and error handling here
    if not name or not dob or not adhar or not nationality or not state or not address or not blood_type or not contact_phone:
        return {"message": "Missing required fields"}, 400

    # Insert donor information into the database
    donors.insert_donor(name, dob, adhar, nationality, state, address, blood_type, contact_phone)

    return {"m": "Donor registered successfully","message":"ok"}, 200


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
