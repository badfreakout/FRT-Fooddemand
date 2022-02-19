import os
import json

from azureml.studio.core.io.model_directory import ModelDirectory
from pathlib import Path
from azureml.studio.modules.ml.score.score_generic_module.score_generic_module import ScoreModelModule
from azureml.designer.serving.dagengine.converter import create_dfd_from_dict
from collections import defaultdict
from azureml.designer.serving.dagengine.utils import decode_nan
from azureml.studio.common.datatable.data_table import DataTable


model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'trained_model_outputs')
schema_file_path = Path(model_path) / '_schema.json'
with open(schema_file_path) as fp:
    schema_data = json.load(fp)


def init():
    global model
    model = ModelDirectory.load(model_path).model


def run(data):
    data = json.loads(data)
    input_entry = defaultdict(list)
    for row in data:
        for key, val in row.items():
            input_entry[key].append(decode_nan(val))

    data_frame_directory = create_dfd_from_dict(input_entry, schema_data)
    score_module = ScoreModelModule()
    result, = score_module.run(
        learner=model,
        test_data=DataTable.from_dfd(data_frame_directory),
        append_or_result_only=True)
    return json.dumps({"result": result.data_frame.values.tolist()}
                      
                      
endpoint = 'http://e4b10aeb-474a-4fc2-b275-846337b3ab01.centralindia.azurecontainer.io/score' #Replace with your endpoint
key = 'zrkbjURc2NK5zIdakgUdNEdRHPBhA4U6' #Replace with your key

import urllib.request
import json
import os

data ={"input_data":[{"field": [['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
       'city_code', 'region_code', 'category']],"values": [input_features ]}]}
    

body = str.encode(json.dumps(data))


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key)}

req = urllib.request.Request(endpoint, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read()
    json_result = json.loads(result)
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])
    pred = int(predictions['predictions'][0]['values'][0][0])
    print(pred)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers to help debug
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
