#! /bin/bash

echo 'Syncing solr/* config into apache-solr-3.5.0 directory'
cp -rv solr/* apache-solr-3.5.0/example

cd apache-solr-3.5.0/example
java -jar start.jar
