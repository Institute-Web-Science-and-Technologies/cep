# Cover Evaluation Platform (CEP)

The cover evaluation platform consists of several tools that allows for processing the measurements provided by [Koral](https://github.com/Institute-Web-Science-and-Technologies/koral) and to visualize them by diagrams. Additionally it provides a tool to execute a bunch of queries by varying the query execution strategy several times.

In the following it is assumed that you have built and deployed a Koral cluster. See the description on [Koral's GitHub page](https://github.com/Institute-Web-Science-and-Technologies/koral). In the following it is assumed.

## Build CEP

First, clone CEP:
```
git clone https://github.com/Institute-Web-Science-and-Technologies/cep
```

Copy the koral.jar and Apache Commons CLI into the lib folder:
```
cp koral/build/koral.jar cep/lib/
cp koral/lib/commons-cli-1.3.1.jar cep/lib/
```

Build CEP:
```
cd cep
ant
cd ..
```

## Collect Measurements during Loading

If you want to compare several graph cover strategies, you should create an individual Koral configuration file for each graph cover strategy. In these configuration files the directory properties should be adjusted to be unique for each graph cover strategy.

First, the measurement collector should be started:
```
java -jar koral/build/koral.jar measurementReceiver -o /output/file/for/measurements_loading_Cover1.csv.gz
```
Make sure that the output file names differ for each graph cover strategy.

Then, you should update the configuration file of Koral
```
cd koral/scripts
fab -f koral.py updateConfig:"/path/to/koralConfig_Cover1.xml"
cd ../..
```
and start the Koral cluster:
```
cd koral/scripts
fab -f koral.py start:remoteMeasurementCollector=IPofMeasurementCollector
cd ../..
```

Now, you can load the graph:
```
java -jar koral/build/koral.jar client -m IPofMaster load -c COVER_STRATEGY -n 0 /path/to/graphFile.rdf
```
Depending on the graph size, the loading may take a long time. Therfore, programs like `nohup` or `screen` might be used.

When loading is finished you might either continue with querying or stop the Koral cluster. Wait for some time before shutting down the measurement receiver since it may take some time until the last measurements are received.

## Collect Measurements during Querying

First, the measurement collector should be started:
```
java -jar koral/build/koral.jar measurementReceiver -o /output/file/for/measurements_querying_Cover1.csv.gz
```
Make sure that the output file names differ for each graph cover strategy.

Then, you should update the configuration file of Koral
```
cd koral/scripts
fab -f koral.py updateConfig:"/path/to/koralConfig_Cover1.xml"
cd ../..
```
and start the Koral cluster:
```
cd koral/scripts
fab -f koral.py start:remoteMeasurementCollector=IPofMeasurementCollector
cd ../..
```

Now, you can execute the queries:
```
java -cp cep/build/cep.jar de.unikoblenz.west.cep.queryExecutor.QueryExecutor -m IPofMaster -i /path/to/directory/with/queries/ -o /path/to/directory/for/query/results/ -r 10
```
- With the argument `-m` you specify the IP of the master and optionally its port.
- With the argument `-i` you specify the directory that contains the SPARQL query files.
- With the argument `-o` you specify the directory where the results of the queries are stored. If you do not specify this argument, the results are omitted.
- With the argument `-r` you specify how frequently the list of queries is executed.

Thereafter, you can stop the Koral cluster. Wait for some time before shutting down the measurement receiver since it may take some time until the last measurements are received.

## Preprocess the measured values

Now, you should have the files containing the measurement of the graph loading, e.g., `measuements_loading_Cover1.csv.gz` and `measuements_loading_Cover2.csv.gz`. Furthermore, you should have the measurement for the different query executions, e.g., `measuements_querying_Cover1.csv.gz` and `measuements_querying_Cover2.csv.gz`.

Now, you can preprocess the measurements of the graph loading measurements:
```
java -cp cep/build/cep.jar de.unikoblenz.west.cep.measurementProcessor.MeasurementProcessor -l  measuements_loading_Cover1.csv.gz -o /path/to/directory/for/preprocessed/data
java -cp cep/build/cep.jar de.unikoblenz.west.cep.measurementProcessor.MeasurementProcessor -l  measuements_loading_Cover2.csv.gz -o /path/to/directory/for/preprocessed/data
```
and of the query execution:
```
java -cp cep/build/cep.jar de.unikoblenz.west.cep.measurementProcessor.MeasurementProcessor -q  measuements_querying_Cover1.csv.gz -o /path/to/directory/for/preprocessed/data -c COVER1 -r 10 -Q /path/to/directory/with/queries
java -cp cep/build/cep.jar de.unikoblenz.west.cep.measurementProcessor.MeasurementProcessor -q  measuements_querying_Cover2.csv.gz -o /path/to/directory/for/preprocessed/data -c COVER2 -r 10 -Q /path/to/directory/with/queries
```
- With the argument `-c` the used graph cover strategy is specified.
- With the argument `-r` you specify how frequently the list of queries were executed.
- With the argument `-Q` the path to the directory containing the original queries are specified

## Create Diagramms

The diagrams are created by Python scripts using the library [matplotlib](http://matplotlib.org/). You can install the library by executing:
```
sudo apt-get install python-matplotlib
```

You can generate the corresponding diagrams by executing, e.g.,
```
python cep/diagramCreator/LoadingTime.py /path/to/directory/for/preprocessed/data/loadingTime.csv /path/to/directory/for/diagrams svg
```
- The first argument specifies the required data generated in the previous step. If you execute the python scripts without arguments the required CSV file is printed to the standard output.
- The second argument specifies the directory in which the diagrams should be created.
- The last argument specifies the image type of the generated diagrams.