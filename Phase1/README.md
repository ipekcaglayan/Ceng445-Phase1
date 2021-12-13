A Shared Photo Library Organizer
Simge Tekin 2306686
İpek Çağlayan 2306090

We used exif and pillow. 
Requirements.txt includes information about python packages that are required to run our project.

Virtual environment can be created by running following commands:
1) virtualenv -p python3.8 venv (creates venv)
2) source venv/bin/activate (activates venv)
3) pip install -r Requirements.txt (installs necessary packages)

demo.py is a command line demo application 
Commands must be executed in the order they are written in demo.py which is

1) create_4_user ipek bugris simgos ege
2) create_collection
3) create_view
4) set_filters_for_view
5) set_view_attributes_and_filter ./sample1.jpg ./sample2.jpg ./sample3.jpg ./sample4.jpg ./sample5.jpg
6) upload_photo_and_update_location_tag_datetime ./canon.jpg (10,10,10) (20,20,20) datetime.datetime(2020,10,2) datetime.datetime(2021,4,3)
7) add_fetch_remove_photo_to_collection
8) add_view_to_collection
9) share_collection
10) share_shared_collection
11) add_fetch_remove_photo_to_shared_collection
12) add_view_to_shared_collection
13) add_fetch_remove_photo_to_not_shared_collection
14) add_view_to_not_shared_collection
15) unshare_collection
16) share_view
17) unshare_view
18) bye