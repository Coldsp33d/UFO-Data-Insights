# Content Detection Assignment - 3 - 

Features [our analysis](http://ufo.usc.edu) on UFO data obtained from first and second assignments. 

## Team Members

1.  Akashdeep Singh
2.  Koustav Mukherjee
3.  Sayali Ghaisas
4.  Shiva Deviah
5.  Vritti Rohira

## Getting Started

## Part 1 - Visualizations with D3

Scripts for Generating Data for D3 Visualizations can be found in folder: `d3-data-generation-scripts`

Each script name is the name of the visualization followed by the features it uses for analysis. 
To run each file: 

	python dashboard_elevation_statewise_sightings.py

The corresponding data file is generated in `ufo.usc.edu\Data` folder

The D3 HTML files that use this data are found in `ufo.usc.edu\d3-visualizations` with the same naming convention.

## Note - Sometimes it might happen the vizualization doesn't load.Please perform the below changes:
*Right click ->Frame -> Reload Frame*

## Part 2 - Ingesting with Apache Solr

The commands to create a Solr index are all  listed in `solr\commands.txt`

1. Delete any containers with the name "ufo" 

	``	
		solr.cmd delete -c ufo
	``

2. Create a new container for the data you wish to ingest

	``
		solr.cmd create -c ufo -s 2 -rf 2
	``

3. Create a schema for your index

	````
	curl -X POST -H 'Content-type:application/json' --data-binary "{\"add-field\": {\"name\":\"sighted_at\", \"type\":\"pdate\", \"multiValued\":false, \"stored\":true,\"indexed\":true}}" http://localhost:8983/solr/ufo/schema

	curl -X POST -H 'Content-type:application/json' --data-binary "{\"add-field\": {\"name\":\"state\", \"type\":\"string\", \"multiValued\":false, \"stored\":true,\"indexed\":true}}" http://localhost:8983/solr/ufo/schema

	curl -X POST -H 'Content-type:application/json' --data-binary "{\"add-field\": {\"name\":\"shape\", \"type\":\"string\", \"multiValued\":false, \"stored\":true,\"indexed\":true}}" http://localhost:8983/solr/ufo/schema

	curl -X POST -H 'Content-type:application/json' --data-binary "{\"add-copy-field\" : {\"source\":\"*\",\"dest\":\"_text_\"}}" http://localhost:8983/solr/ufo/schema
	````

4. Ingest your index

	``
		java -jar -Dc=ufo -Dauto ../example/exampledocs/post.jar "./sightings_state.csv"
	``

5. Run the dynamic visualization

	Data insights of shape aggregated over 5 years for each state is depicted with a bullet chart that invokes Solr RESTful web services using JSON. Data is dynamically loaded when the state is changed.

	The JavaScript file containing the data can be found at `ufo.usc.edu/js/team6/solr_bullet_chart_integration.js`

	The corresponding HTML file is at `ufo.usc.edu/d3-visualizations/bullet_chart_state_shape_sightings.html`
	
	

## Part 3 - Similarity with Memex ImageCat and Image Space

### Part A - FLANN Plugin 

1. `cd image_space/flann_index/`
2. Run `flann_index.py`, generating the image mappings 
3. Start the webservice with tangelo. Run `./start.sh`

You can now make get requests to port 9220. For example,

    curl "http://localhost:9220?query=/path/to/images/71209.jpg&k=10"

Will return the top 10 most similar images to the 71209.jpg.


### Part B - SMQTK Plugin  
1. `cd image_space/imagespace_smqtk/`
2. Run the following commands
	```
		sudo ./smqtk_services.run_images.sh --docker-network docker_imagespace-network --images /home/koustav/images
		sudo docker exec -it deploy_imagespace-mongo_1 mongo girder --eval 'db.setting.update({key: "core.plugins_enabled"}, {$push: {value: "imagespace_smqtk"}})'
		sudo docker exec -it deploy_imagespace-mongo_1 mongo girder --eval 'db.setting.insert({key: "IMAGE_SPACE_SMQTK_NNSS_URL", value: "http://smqtk-services:12345"})'
		sudo docker exec -it deploy_imagespace-mongo_1 mongo girder --eval 'db.setting.insert({key: "IMAGE_SPACE_SMQTK_IQR_URL", value: "http://smqtk-services:12346"})'
		sudo docker exec -it deploy_imagespace-mongo_1 mongo girder --eval 'db.setting.insert({key: "IMAGE_SPACE_DEFAULT_SIMILARITY_SEARCH", value: "smqtk-similarity"})'
		sudo docker exec -it deploy_imagespace-girder_1 touch /girder/girder/conf/girder.dist.cfg
	```
3. Go to localhost:8989 search for jpg images and then click the search icon (image similarity SMQTK plugin) and it will show up the relevant images