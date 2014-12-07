# einzeiler, auf aspra8 ausführen
mysql --host=aspra20.informatik.uni-leipzig.de -u USERNAME -p DATABASENAME < req.sql | sed 's/\t/,/g' > OUTFILE.csv

