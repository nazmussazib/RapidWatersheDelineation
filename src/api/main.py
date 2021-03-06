import logging
import os.path
import shutil
from subprocess import call
import json
import tempfile
import uuid

from flask import Flask, jsonify, request

from rwd.Rapid_Watershed_Delineation import Point_Watershed_Function


app = Flask(__name__)

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())


def error_response(error_message):
    response = jsonify(error=error_message)
    response.status_code = 400
    return response


@app.route('/rwd/<lat>/<lon>', methods=['GET'])
def run_rwd(lat, lon):
    """
    Runs RWD for lat/lon and returns the GeoJSON
    for the computed watershed boundary, outlet point
    and snapped point.
    """
    snapping = request.args.get('snapping', '1')
    maximum_snap_distance = request.args.get('maximum_snap_distance', '10000')
    num_processors = '1'
    data_path = '/opt/rwd-data'

    # Create a temporary directory to hold the output
    # of RWD.
    output_path = tempfile.mkdtemp()

    try:
        Point_Watershed_Function(
            lat,
            lon,
            snapping,
            maximum_snap_distance,
            data_path,
            'Delaware_Ocean_stream_dissolve',
            'delaware_gw_5000_diss',
            'Delaware_Missing_Coast_Watershed',
            'DelDEMGeo2fel.tif',
            'DelDEMGeo2Max_elv_upslope.tif',
            'DelDEMGeo2ad8_slope_weighted.tif',
            'DelDEMGeo2ad8.tif',
            'DelDEMGeo2plen.tif',
            'DelDEMGeo2tlen_peuker.tif',
            'DelDEMGeo2gord_peuker.tif',
            num_processors,
            '/opt/taudem',
            '/usr/bin/',
            output_path
        )

        # The Watershed and input coordinates (possibly snapped to stream)
        # are written to disk.  Load them and convert to json
        wshed_shp_path = os.path.join(output_path, 'New_Point_Watershed.shp')
        input_shp_path = os.path.join(output_path, 'New_Outlet.shp')

        output = {
            'watershed': load_json(wshed_shp_path, output_path),
            'input_pt': load_json(input_shp_path, output_path)
        }

        shutil.rmtree(output_path)
        return jsonify(**output)

    except Exception as exc:
        log.exception('Error running Point_Watershed_Function')
        return error_response(exc.message)


def load_json(shp_path, output_path):
    name = '%s.json' % uuid.uuid4().hex
    output_json_path = os.path.join(output_path, name)
    call(['ogr2ogr', output_json_path, shp_path, '-f', 'GeoJSON'])

    try:
        with open(output_json_path, 'r') as output_json_file:
            output = json.load(output_json_file)
            return output
    except:
        log.exception('Could not get GeoJSON from output.')
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0")
