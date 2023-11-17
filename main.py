from flask import Flask, request, jsonify, render_template
import observations_model_palm as ObservationsModel
import id_associations

app = Flask(__name__)

#dictionary associating observed categories to IDs
core_obs_categories = id_associations.core_obs_categories
facebook_obs_categories = id_associations.facebook_obs_categories
facebook_obs_buildings = id_associations.facebook_obs_buildings
facebook_obs_areas = id_associations.facebook_obs_areas
facebook_obs_levels = id_associations.facebook_obs_levels
facebook_obs_rooms = id_associations.facebook_obs_rooms

def get_app():
    return app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/observations_demo/', methods=['GET'])
def observationsdemo():
    if request.method == 'GET':
        try:
            description = request.args['description']
            output = ObservationsModel.observation_response(description).split(", ")
            output_string = ""
            for item in output:
                output_string += item + "\n"
            return render_template('observations_demo.html', description=description, output=output_string)
        except:
            return render_template('observations_demo.html')

@app.route('/observations/', methods=["GET"])
def observations():
    args = request.args
    description = args['description']
    print("Received observation description: " + description + "\n")
    #print(description)
    output = ObservationsModel.observation_response(description)
    #print(output)
    try:
        splitOutput = output.split(", ")
        category = splitOutput[0].split(": ")[1]
        ob_type = splitOutput[1].split(": ")[1]
        rating = splitOutput[2].split(": ")[1]
        observed_party = splitOutput[3].split(": ")[1]
        location = splitOutput[4].split(": ")[1]
        additional_note = splitOutput[5].split(": ")[1]
        result = {}
        result['Error'] = False
        result['Category'] = category
        result['Type'] = ob_type
        result['Rating'] = rating
        result['Observed Party'] = observed_party
        result['Location'] = location
        result['Additional Note'] = additional_note
        return jsonify(result)
    except:
        result = {}
        result['Error'] = True
        result['Category'] = ""
        result['Type'] = ""
        result['Rating'] = ""
        result['Observed Party'] = ""
        result['Location'] = ""
        result['Additional Note'] = output
        return jsonify(result)
    
@app.route('/core_obs/', methods=["GET"])
def core_obs():
    args = request.args
    description = args['description']
    projects = []
    try:
        projects = args['projects']
    except:
        projects = ["none"]
    divisions = []
    try:
        divisions = args['divisions']
    except:
        divisions = ["none"]
    print("Received core observation description: " + description + "\n")
    #print(description)
    output = ObservationsModel.core_obs_response(description)
    #print(output)
    try:
        splitOutput = output.split(", ")
        category = splitOutput[0].split(": ")[1]
        ob_type = splitOutput[1].split(": ")[1]
        project = splitOutput[2].split(": ")[1]
        division = splitOutput[3].split(": ")[1]
        additional_note = splitOutput[2].split(": ")[1]
        result = {}
        result['Error'] = False
        result['Category'] = category
        result['Category_ID'] = core_obs_categories[category]
        result['Type'] = ob_type
        result['Project'] = ObservationsModel.get_project(project,projects)
        result['Division'] = ObservationsModel.get_division(description,division,divisions)
        result['Additional Note'] = additional_note
        return jsonify(result)
    except:
        result = {}
        result['Error'] = True
        result['Category'] = ""
        result['Category_ID'] = 0
        result['Type'] = ""
        result['Project'] = ObservationsModel.get_project(project,projects)
        result['Division'] = ObservationsModel.get_division(description,division,divisions)
        result['Additional Note'] = output
        return jsonify(result)
    
@app.route('/core_obs_demo/', methods=['GET'])
def coreobsdemo():
    if request.method == 'GET':
        try:
            description = request.args['description']
            projects = ["Express Tire", "Littlerock Hotel", "Project 1032"]
            divisions = ["HVAC", "Plumbing", "Southwest"]
            output = ObservationsModel.core_obs_response(description).split(", ")
            project = output[2].split(": ")[1]
            division = output[3].split(": ")[1]
            output_string = ""
            for item in output:
                output_string += item + "\n"     
            output_string += "Official Project: " + ObservationsModel.get_project(project,projects) + "\n"
            output_string += "Official Division: " + ObservationsModel.get_division(description,division,divisions)
            return render_template('core_obs_demo.html', description=description, output=output_string)
        except:
            return render_template('core_obs_demo.html')
        
@app.route('/amazon_obs/', methods=["GET"])
def amazon_obs():
    args = request.args
    description = args['description']
    projects = []
    try:
        projects = args['projects']
    except:
        projects = ["none"]
    divisions = []
    try:
        divisions = args['divisions']
    except:
        divisions = ["none"]
    print("Received Facebook observation description: " + description + "\n")
    #print(description)
    output = ObservationsModel.facebook_obs_response(description)
    #print(output)
    #order: division, project, building, area, level, room, category, contractor, type, rating, corrected
    try:
        splitOutput = output.split(", ")
        division = splitOutput[0].split(": ")[1]
        project = splitOutput[1].split(": ")[1]
        building = splitOutput[2].split(": ")[1]
        area = splitOutput[3].split(": ")[1]
        level = splitOutput[4].split(": ")[1]
        room = splitOutput[5].split(": ")[1]
        category = splitOutput[6].split(": ")[1]
        contractor = splitOutput[7].split(": ")[1]
        ob_type = splitOutput[8].split(": ")[1]
        rating = splitOutput[9].split(": ")[1]
        corrected = splitOutput[10].split(": ")[1]
        result = {}
        result['Error'] = False
        result['Division'] = ObservationsModel.get_division(description,division,divisions)
        result['Project'] = ObservationsModel.get_project(project,projects)
        try:
            result['B1'] = facebook_obs_buildings[building]
        except:
            result['B1'] = building
        try:
            result['B2'] = facebook_obs_areas[area]
        except:
            result['B2'] = area
        try:
            result['B3'] = facebook_obs_levels[level]
        except:
            result['B3'] = level
        try:
            result['B4'] = facebook_obs_rooms[room]
        except:
            result['B4'] = room
        try:
            result['Category'] = facebook_obs_categories[category]
        except:
            result['Category'] = category
        result['Contractors'] = ObservationsModel.get_contractors(contractor,'facebook_contractors.csv','facebook_contractor_embeddings.npy')
        result['Contractor'] = result['Contractors'][0]
        result['ObservationType'] = ob_type
        result['Rating'] = rating
        result['Corrected'] = corrected
        result['Desc'] = description
        return jsonify(result)
    except:
        result = {}
        result['Error'] = True
        result['Division'] = ""
        result['Project'] = ""
        result['B1'] = ""
        result['B2'] = ""
        result['B3'] = ""
        result['B4'] = ""
        result['Category'] = ""
        result['Contractor'] = ""
        result['Contractors'] = []
        result['ObservationType'] = ""
        result['Rating'] = ""
        result['Corrected'] = ""
        result['Desc'] = description
        return jsonify(result)

@app.route('/amazon_obs_demo/', methods=['GET'])
def amazonobsdemo():
    if request.method == 'GET':
        try:
            description = request.args['description']
            projects = ["Express Tire", "Littlerock Hotel", "Project 1032"]
            divisions = ["HVAC", "Plumbing", "Southwest"]
            output = ObservationsModel.facebook_obs_response(description).split(", ")
            division = output[0].split(": ")[1]
            project = output[1].split(": ")[1]
            contractor = output[7].split(": ")[1]
            output_string = ""
            for item in output:
                output_string += item + "\n"
            output_string += "Official Division: " + ObservationsModel.get_division(description,division,divisions) + "\n"
            output_string += "Official Project: " + ObservationsModel.get_project(project,projects) + "\n"
            output_string += "Official Contractor: " + str(ObservationsModel.get_contractors(contractor,'facebook_contractors.csv','facebook_contractor_embeddings.npy'))
            return render_template('amazon_obs_demo.html', description=description, output=output_string)
        except:
            return render_template('amazon_obs_demo.html')