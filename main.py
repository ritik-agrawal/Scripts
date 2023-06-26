import yaml
import chardet	
import os

def getEncoding(filepath):
	with open(filepath, 'rb') as file:
		data = file.read()
		result = chardet.detect(data)
		return result['encoding']

def readYamlWithSafeLoader(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        return data

def input():
	result = {}
	result['CUFXProductOfferingDataModelAndServices']   = 'ProductOfferingMessage'
	result['CUFXProductServiceRequestModelAndServices'] = 'ProductServiceRequestMessage'
	result['CUFXPartyMessageDataModelAndServices']      = 'PartyMessage'
	result['CUFXPartyAssociationDataModelAndServices']  = 'PartyAssociationMessage'
	return result

def getChildDict(data, tag):
	result = {}
	result[OPENAPI] = yamlBuilder(OPENAPI, data, tag)
	result[INFO] = yamlBuilder(INFO, data, tag)
	result[SECURITY] = yamlBuilder(SECURITY, data, tag)
	result[TAGS] = yamlBuilder(TAGS, data, tag)
	result[PATHS] = yamlBuilder(PATHS, data, tag)
	return result
	

def yamlBuilder(key ,data, tag):
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
parent_yaml = readYamlWithSafeLoader(FILE_PATH, encoding)

guide = input()
os.makedirs(OUTPUT_PATH, exist_ok = True)
for key in guide:
	service = key
	tag = guide[key]
	print("Creating yaml for service {} with tag as {}".format(service, tag))
	childDict = getChildDict(parent_yaml, tag)
	outputFilename = YAML_FILENAME.format(service)
	outputPath = OUTPUT_PATH+outputFilename
	with open(outputPath, 'w') as file:
		yaml.dump(childDict, file)