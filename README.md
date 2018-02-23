# PortableMoocs

This tool generates static html courses from a tar.gz imported open.edx course

# Using it 

The mooc2sooc.py script has 4 optional parameters

## --course

This indicates the folder name where the resulting course will be generated.

Also if no --file parameter inidicated the script will search into this folder for a tar.gz file wich could be used to generate the course.

If no value is set will try to generate all the courses into the --dest folder


## --file
indicates the tar.gz file path that will be used to generate the course.

requires the --course param set to work 

## --dest 
by default ./data is the folder that will contain all our courses the idea is to have a file structure like

./data/course1
./data/course2
./data/static

so all the courses into the same --dest shares the static files 

## --ress

defines the resolution of the youtube videos that will be downloaded (by default 720p) accepts the same params as youtube 1080p,720p,360p,240p

if no video is found with that resolution will try to download the video in other ressolution and use it as a placeholder


# Use case

we want to generate a single course from a file into our downloads directory

#/> python mooc2sooc.py --course foldername --dest . --file ~/Downloads/course.tar.gz

# Use case
we want to generate a set of courses 

we will download all the tar.gz files of our courses and organize them into folders like

./set-courses/course1/course.tar.gz
./set-courses/course2/course.tar.gz
./set-courses/course3/course.tar.gz

#/> python mooc2sooc.py --dest ./set-courses










