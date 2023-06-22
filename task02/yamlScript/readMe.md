## Introduction
The project deals with OpenApi Yaml files that are used to define the API first development. This is a pyhton project which takes a parent yaml file and generated child yaml file based on the `tags`. As per the OpenApi Documentation, `tags` are used for grouping the paths to form a collection. 

### Input
file `main.py` has a method `input()`. This is a dictionary of service to tag used in the service.

### Output
The output files will be generated in folder `resources/output`. The yaml files will have respective service name specified in the input method.

### OpenAPI keys Supported:
- openapi
- info
- security
- tags
- name
- paths
- externalDocs
- servers
- components

### Future Scope
- In the current implementation, `components` are not extracted from the parent yaml file. 
- Currently the `info` is directly taken from the parent yaml to child yaml file. 