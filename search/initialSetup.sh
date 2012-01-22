#! /bin/bash

#JS: requires wget, tar, and some recent version of java

if [ -e apache-solr-3.5.0 ]
then
	echo "Cleaning up existing solr directory"
	rm -rf apache-solr-3.5.0
fi

if [ ! -e "apache-solr-3.5.0.tgz" ]
then
	echo "Downloading Apache 3.5.0 package"
	wget http://mirror.csclub.uwaterloo.ca/apache/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
fi

tar xzvf apache-solr-3.5.0.tgz
cp -r solr apache-solr-3.5.0/example

echo "Solr rolodx home directory copied to apache-solr-3.5.0/example"
echo "Run ./startSolrServer.sh, then go to http://localhost:8983/solr/admin/ to test your devlocal server"
echo "To index our rolodx models, in rolodx/rolodx/, you'll need to `python manage.py update_index` or rebuild_index."

