import yaml
import chardet	
import os

def getEncoding(filepath):
	with open(filepath, 'rb') as file:
		data = file.read()
		result = chardet.detect(data)
		return result['encoding']

def read_yaml_with_safe_loader(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        return data

def guiding_dictionary():
	result = {}
	result['CUFXProductOfferingDataModelAndServices']   = 'ProductOfferingMessage'
	result['CUFXProductServiceRequestModelAndServices'] = 'ProductServiceRequestMessage'
	result['CUFXPartyMessageDataModelAndServices']      = 'PartyMessage'
	result['CUFXPartyAssociationDataModelAndServices']  = 'PartyAssociationMessage'
	return result

def get_child_dict(data, tag):
	result = {}
	result[OPENAPI] = yaml_builder(OPENAPI, data, tag)
	result[INFO] = yaml_builder(INFO, data, tag)
	result[SECURITY] = yaml_builder(SECURITY, data, tag)
	result[TAGS] = yaml_builder(TAGS, data, tag)
	result[PATHS] = yaml_builder(PATHS, data, tag)
	return result
	

def yaml_builder(key ,data, tag):
	switch = {
		'openapi' : getOpenApi(data),
		'info' : getInfo(data),
		'security' : getSecurity(data),
		'tags' : getTags(data,tag),
		'paths' : getPaths(data,tag),
		'externalDocs': getExternalDocs(data),
		'servers' : getServers(data)
	}
	return switch.get(key)

def getOpenApi(data):
	return data[OPENAPI]

def getInfo(data):
	return data[INFO]

def getSecurity(data):
	return data[SECURITY]

def getTags(data, curTag):
	tags = data[TAGS]
	resultTagDict = {}
	for tag in tags:
		if tag.get(TAGS_NAME) == curTag:		
			resultTagDict[TAGS_NAME] = tag.get(TAGS_NAME)
			resultTagDict[EXTERNAL_DOCS] = tag.get(EXTERNAL_DOCS)
			break
	return [resultTagDict]

def getPaths(data, tag):
	paths = data[PATHS]
	result = {}
	for path in paths:
		methods = paths[path]
		resultMethods = {}
		for method in methods:
			tags = methods[method].get(TAGS)
			if (tag in tags):
				resultMethods[method] = methods[method]
		if len(resultMethods) == 0:
			continue
		else:
			result[path] = resultMethods
	return result


def getExternalDocs(data):
	return data[EXTERNAL_DOCS]

def getServers(data):
	return data[SERVERS]

#def getComponents(data):



###Constants
FILE_PATH = './resources/parentYaml.yaml'
OUTPUT_PATH = './resources/output'
YAML_FILENAME = "/{}.yaml"
OPENAPI = 'openapi'
INFO = 'info'
SECURITY = 'security'
TAGS = 'tags'
TAGS_NAME = 'name'
PATHS = 'paths'
EXTERNAL_DOCS = 'externalDocs'
SERVERS = 'servers'
COMPONENTS = 'components'

###Constants


encoding = getEncoding(FILE_PATH)
parent_yaml = read_yaml_with_safe_loader(FILE_PATH, encoding)

guide = guiding_dictionary()
os.makedirs(OUTPUT_PATH, exist_ok = True)
for key in guide:
	service = key
	tag = guide[key]
	print("Creating yaml for service {} with tag as {}".format(service, tag))
	childDict = get_child_dict(parent_yaml, tag)
	outputFilename = YAML_FILENAME.format(service)
	outputPath = OUTPUT_PATH+outputFilename
	with open(outputPath, 'w') as file:
		yaml.dump(childDict, file)