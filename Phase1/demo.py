import cmd, sys
from SharedPhotoLibrary import *
from User import *
from collections import defaultdict
from pprint import pprint
import datetime

users = {}
collections = defaultdict(list)
views = {}


class SharedPhotoLibraryShell(cmd.Cmd):
    intro = 'Welcome to the Shared Photo Library shell. Type help or ? to list commands.\n'
    prompt = '(SharedPhotoLib) '
    file = None

    # create_4_user ipek bugris simgos ege
    def do_create_4_user(self, arg):

        """Creates 4 users with names given as arguments:
create_user name1 name2 name3 name4"""
        arg = arg.split(" ")
        for i in range(4):
            user = User(arg[i])
            users[arg[i]] = user
            print(user)

    # list_users
    def do_list_users(self, arg):
        """List created users: list_users"""
        pprint(users)

    # create_collection
    def do_create_collection(self, arg):
        """Each user creates 2 collection to show that User can create multiple collections: create_collection"""
        for username, u in users.items():
            collections[u.id].append(u.createCollection(f"{u.username}'s Collection1"))
            collections[u.id].append(u.createCollection(f"{u.username}'s Collection2"))
            print(u)

    def do_create_view(self, arg):
        """Each user creates 1 view: create_view"""
        for username, u in users.items():
            views[u.id] = u.createView(f"{u.username}'s View")
            print(u)

    def do_set_filters_for_view(self, arg):
        """First user sets filter of his/her first view: set_filters_for_view  """

        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_view = list(first_user.views)[0]
        print("first view before setting filters\n", first_view)
        first_user.setTagFilterToView(first_view, ["vacation", "summer"])
        first_user.setLocationRectToView(first_view, (1,2,3,4))
        first_user.setTimeIntervalToView(first_view, datetime.datetime(2020, 10, 3), datetime.datetime(2021, 4, 10))
        print("first view after setting filters\n", first_view)

    def do_set_view_attributes_and_filter(self, arg):
        """1) A user is created.
           2) User uploads photos and sets tags location and datetime.
           3) User creates collection and adds 4 photos from given paths
           4) User creates view and adds this view to collection created in 3rd step
           5) User lists filtered photos based on view
           example: set_view_attributes_and_filter path1 path2 path3 path4 path5"""
        arg = arg.split(" ")
        test_user = User("test")
        for i in range(5):
            test_user.uploadPhoto(arg[i])

        photokeys = list(test_user.photos.keys())
        test_user.setLocationOfPhoto(photokeys[0], (100, 1000, 10), (2000, 20, 20))
        test_user.setDatetimeOfPhoto(photokeys[0], "2021:07:31 10:38:11")
        test_user.addTagToPhoto(photokeys[0], "winter")

        test_user.setLocationOfPhoto(photokeys[1], (20, 20, 20), (20, 20, 20))
        test_user.setDatetimeOfPhoto(photokeys[1], "2011:07:20 10:38:11")
        test_user.addTagToPhoto(photokeys[1], "winter")
        test_user.addTagToPhoto(photokeys[1], "cold")

        test_user.setDatetimeOfPhoto(photokeys[2], "2011:07:20 10:38:11")
        test_user.addTagToPhoto(photokeys[2], "child")

        test_user.setLocationOfPhoto(photokeys[3], (10, 10, 10), (10, 10, 10))
        test_user.setDatetimeOfPhoto(photokeys[3], "2011:07:20 10:38:11")
        test_user.addTagToPhoto(photokeys[3], "child")

        print(
            "Photos of test user after she added 4 photos, tagged them and set location and datetime of some of them: ")
        print(test_user.photos)

        test_user.createCollection(f"Test user's Collection")

        for i in range(5):
            test_user.addPhotoToCollection(test_user.collections[0], test_user.photos[photokeys[i]])
        print(f"Test user created collection and added photos : {test_user}")

        test_user.createView(f"Test user's view")
        for i in test_user.views:
            i.setTagFilter(["winter"])
            i.setLocationRect(((0, 0, 0), (100, 100, 100), (0, 0, 0), (100, 100, 100)))
            i.setTimeInterval("2010:07:20 10:38:11", "2030:07:20 10:38:11")
            test_user.collections[0].addView(i)
        print(f"Test user created view and added to collection: {test_user}")

        for i in test_user.views:
            print(f"Photo in test users view {i.filtered_photos_ids}")

    #  upload_photo_and_update_location_tag_datetime ./canon.jpg (10,10,10) (20,20,20) datetime.datetime(2020,10,2) datetime.datetime(2021,4,3)
    def do_upload_photo_and_update_location_tag_datetime(self, arg):
        """"First, second and third users upload a photo from given path then
first user sets the location to given longitude and latitude and removes ,
adds given tag to photo and removes, and sets datetime to given datetime:
upload_photo_and_update_location_tag_datetime path long latt tag datetime """
        arg = arg.split(" ")
        path = arg[0]
        long = arg[1]
        latt = arg[2]
        tag = arg[3]
        datetime = arg[4]
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        second_user = users[usernames[1]]
        third_user = users[usernames[2]]
        second_user.uploadPhoto(path)
        third_user.uploadPhoto(path)
        print("First user before uploading a photo\n", first_user)
        first_user.uploadPhoto(path)
        print("First user after uploading a photo\n", first_user)
        keys = list(first_user.photos.keys())
        first_user.setLocationOfPhoto(keys[0], long, latt)
        first_user.setDatetimeOfPhoto(keys[0], datetime)
        first_user.addTagToPhoto(keys[0], tag)

        print(f"Photo after First User adds tag,datetime,location {first_user.photos[keys[0]]}")
        first_user.removeLocationFromPhoto(keys[0])

        first_user.removeTagFromPhoto(keys[0], tag)
        print(f"Photo after First User removes tag and location {first_user.photos[keys[0]]}")

    def do_add_fetch_remove_photo_to_collection(self, arg):
        """"First user uploads his/her first photo to his/her first collection, fetches photo from the collection,
and than removes it: add_fetch_remove_photo_to_collection  """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        photos_ids = list(first_user.photos.keys())
        first_photo = first_user.photos[photos_ids[0]]
        print("First collection before uploading a photo\n", first_collection_of_first_user)
        first_user.addPhotoToCollection(first_collection_of_first_user, first_photo)
        print("First collection after uploading a photo\n", first_collection_of_first_user)
        print("newly added photo will be fetched from the collection\n")
        first_user.fetchPhotoFromCollection(first_collection_of_first_user, first_photo.id)
        first_user.removePhotoFromCollection(first_collection_of_first_user, first_photo)
        print("First collection after removing a photo\n", first_collection_of_first_user)

    def do_add_view_to_collection(self, arg):
        """"First user adds his/her first view to his/her first collection: add_view_to_collection  """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        first_view = list(first_user.views)[0]
        print("First collection before adding a view\n", first_collection_of_first_user)
        first_user.addViewToCollection(first_collection_of_first_user, first_view)
        print("First collection after adding a view\n", first_collection_of_first_user)

    # share_collection
    def do_share_collection(self, arg):
        """First user will share his/her first collection with the second user: share_collection"""
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        second_user = users[usernames[1]]
        print("second user before collection shared with him/her\n", second_user)
        first_collection_of_first_user = first_user.collections[0]
        first_user.shareCollection(first_collection_of_first_user, second_user)
        print("second user after collection shared with him/her\n", second_user)

    def do_share_shared_collection(self, arg):
        """Second user will try to share first collection of the first user, which is shared by first user with him ,
 with the third user: share_shared_collection"""
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        second_user = users[usernames[1]]
        third_user = users[usernames[2]]
        first_collection_of_first_user = first_user.collections[0]
        print("third user before collection shared with him/her\n", third_user)
        second_user.shareCollection(first_collection_of_first_user, third_user)
        print("third user after collection shared with him/her\n", third_user)

    def do_add_fetch_remove_photo_to_shared_collection(self, arg):

        """"Second user uploads his/her first photo to a collection shared with him/her (first collection of first user)
fetches photo from collection and than removes it: add_fetch_remove_photo_to_shared_collection  """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        second_user = users[usernames[1]]
        photos_ids = list(second_user.photos.keys())
        first_photo = second_user.photos[photos_ids[0]]
        print("First collection before uploading a photo\n", first_collection_of_first_user)
        second_user.addPhotoToCollection(first_collection_of_first_user, first_photo)
        print("First collection after uploading a photo\n", first_collection_of_first_user)
        print("newly added photo will be fetched from the collection\n")
        second_user.fetchPhotoFromCollection(first_collection_of_first_user, first_photo.id)
        second_user.removePhotoFromCollection(first_collection_of_first_user, first_photo)
        print("First collection after removing a photo\n", first_collection_of_first_user)

    def do_add_view_to_shared_collection(self, arg):
        """"Second user adds his/her first view to a collection shared with him/her (first collection of first user):
add_view_to_shared_collection  """

        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        second_user = users[usernames[1]]
        first_view = list(second_user.views)[0]
        print("First collection before adding a view\n", first_collection_of_first_user)
        second_user.addViewToCollection(first_collection_of_first_user, first_view)
        print("First collection after adding a view\n", first_collection_of_first_user)

    def do_add_fetch_remove_photo_to_not_shared_collection(self, arg):

        """"Third user tries to upload his/her first photo to a first collection of first user
(third user not owner and collection not shared with him/her)
fetch a photo from collection and than remove it: add_fetch_remove_photo_to_not_shared_collection  """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        third_user = users[usernames[2]]
        photos_ids = list(third_user.photos.keys())
        first_photo = third_user.photos[photos_ids[0]]
        print("First collection before add fetch and remove operations\n", first_collection_of_first_user)
        third_user.addPhotoToCollection(first_collection_of_first_user, first_photo)
        third_user.fetchPhotoFromCollection(first_collection_of_first_user, first_photo.id)
        third_user.removePhotoFromCollection(first_collection_of_first_user, first_photo)
        print("First collection after add fetch and remove operations\n", first_collection_of_first_user)

    def do_add_view_to_not_shared_collection(self, arg):
        """"Third user adds his/her first view to first collection of first user
(third user not owner and collection not shared with him/her): add_view_to_not_shared_collection  """

        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        third = users[usernames[2]]
        first_view = list(third.views)[0]
        print("First collection before adding a view\n", first_collection_of_first_user)
        third.addViewToCollection(first_collection_of_first_user, first_view)
        print("First collection after adding a view\n", first_collection_of_first_user)

    def do_unshare_collection(self, arg):
        """First user unshares his/her first collection with second user and then second user cannot add a photo
to first collection of first user: unshare_collection"""
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        first_collection_of_first_user = first_user.collections[0]
        second_user = users[usernames[1]]
        photos_ids = list(second_user.photos.keys())
        first_photo = second_user.photos[photos_ids[0]]
        print("second use before unshare\n", second_user)
        first_user.unshareCollection(first_collection_of_first_user, second_user)
        print("second use after unshare\n", second_user)
        print("second user tries to add a photo to first collection of first user\n")
        second_user.addPhotoToCollection(first_collection_of_first_user, first_photo)

    def do_share_view(self, arg):
        """Share first view of first user with the third user: share_view """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        third_user = users[usernames[2]]
        first_view = list(first_user.views)[0]
        print("third user before sharing\n", third_user)
        first_view.share(third_user)
        print("third user after sharing\n", third_user)

    def do_unshare_view(self, arg):
        """Unshare first view of first user with the third user: unshare_view """
        usernames = list(users.keys())
        first_user = users[usernames[0]]
        third_user = users[usernames[2]]
        first_view = list(first_user.views)[0]
        print("third user before unsharing\n", third_user)
        first_view.unshare(third_user)
        print("third user after unsharing\n", third_user)



    def do_bye(self, arg):
        print('Thank you for using Shared Photo Library Shell')
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    SharedPhotoLibraryShell().cmdloop()
