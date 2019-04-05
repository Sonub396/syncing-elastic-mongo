# Syncing elasticsearch and mongodb

### Note : This is a project done in my internship period at a startup. Hence this is only the sample code to get the basic insights of my work.

This a service wherein we can connect multiple mongo url to our elasticsearch host. 
By using mongo's change streams (db.watch()) we can keep track of the changes made in our mongo collections. 
Using the elasticsearch-py api ([here](https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch))
for accessing our elasticsearch host.

Raw indexes include all the information in the original data sources. In many case you just want some parameters from your data,
hence we can have enrcihed indexes, which you need to provide in config.json file.

## Using config.json file
So a user can specify all the connecion strings for mongo and elastic in config.json file. 
The required fields in record which we want to index into elastic can be specified.
Also we can specify the time interval for sync

### User/Client defined mapping in elasticsearch
In the collection map user/client can specigy the way they want to index their documents from mongo to elastic. 
It consists of the "elastic_str" where user needs to mention the url, index_name, doc_type and id. 
In "flow" we specify the aliases for our attributes in each record, and in "alias" we specify our collection's alias name.

#### Note:
This Readme file still needs to be updated!!!
