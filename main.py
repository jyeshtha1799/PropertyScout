import json, csv
from flask import Flask, jsonify, request, render_template
from homeharvest import scrape_property
from datetime import datetime

app = Flask(__name__)


def search_properties(location, listing_type, past_days):
    # Generate filename based on current timestamp for storing results
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"HomeHarvest_{current_timestamp}.csv"
    
    properties = scrape_property(
        location=location,
        listing_type=listing_type,
        past_days=past_days
    )
    properties.to_csv(filename, index=False)  # Save the results to CSV
    return properties

@app.route('/find', methods=['POST'])
def find_properties():
    refined_properties = []
    return_msg = {}
    try:
        form_data = request.form.to_dict()
        
        properties = search_properties(
            location=form_data['location'],
            listing_type=form_data['listing_type'],
            past_days=int(form_data['past_days'])
        )
        
        # Simplify the properties data to be sent as JSON
        for index, row in properties.iterrows():
            refined_properties.append({
                'mls_id': row['mls_id'],
                'address': f"{row['street']}, {row['city']}, {row['state']} {row['zip_code']}",
                'price': row['list_price'],
                'url': row['property_url'],
                'image': row['property_url']  # Assuming image URL needs to be added or fetched separately
            })
        
        return_msg = {'status': 'OK', 'msg': refined_properties}
    except Exception as ex:
        return_msg = {'status': 'FAIL', 'msg': str(ex)}
    finally:
        return jsonify(data=return_msg)

