import MySQLdb as mdb
import sys
import os
import logging
import pickle
import itertools


### A few important variables ###

input.file = "/full/path/to/phylota/tree/file"
db.host = "localhost"
db.user = ""
db.password = ""
db.database = ""

###



### Read in a parse the tree file output from trees file

treefile = open(input.file, 'r')
raw_id = []
id = []
for t in treefile:
    tree_id = t.split("\t")
    tree_id = tree_id[0].split("_")
    tree_id[0] = tree_id[0][2:]
    tree_id[1] = tree_id[1][2:]
    id.append(tree_id)

## connect to the database and set a cursor
database = mdb.connect(host=db.host, # your host, usually localhost
                     user=db.user, # your username
                     passwd=db.password, # your password
                     db=db.database) # name of the data base
cluster_db = database.cursor() # define the db cursor


count = 0 #status count
for i in id:
    #sql query to find the sequences that belong to the cluster / taxon that are present in the given tree
    sql = "".join(["SELECT seqs.gi,seqs.seq FROM seqs LEFT JOIN ci_gi_184 ON seqs.gi=ci_gi_184.gi WHERE ci_gi_184.ti=", id[count][0]," AND ci_gi_184.clustid=",id[count][1], " AND ci_gi_184.cl_type='subtree';"])
    cluster_db.execute(sql) #execute the above sql query
    record = cluster_db.fetchall() #fetch all records that meet the query criteria and place them in the list record
    record = list(record) #convert tuple to list
    filename = "".join(["output/fasta/ti",id[count][0],"_ci",id[count][1],".fasta"]) # create a string that contains the appropriate filename for each FASTA file
    f = open(filename,'w+')
    
    for r in record:
        cur_record = list(r) #convert this element of the record list from tuple to a list
        cur_record[0] = str(cur_record[0]) #convert the GID value from long to string
        cur_record = "".join([">gi|",str(cur_record[0]),"\n",cur_record[1]]) #join all elements of the cur_record list into a single string, added formatting for FASTA style
        f.write("%s\n" % cur_record)    
    
    print "Sequences for tree " + str(count) + " successfully written to " + filename + "."
    count = count + 1
    f.close()    
