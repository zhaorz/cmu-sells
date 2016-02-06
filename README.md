# cmu-sells
The better half of For Sale @ CMU.

# How to run
First, make sure the virtual environment is activated. If not, run

```
$ . venv/bin/activate
```

You may have to install some more requirements.

```
$ pip install -r requirements.txt
```

Then, run these two commands to start the server

```
$ ./db_init.sh
$ python run.py run
```

This initializes the database and starts the server.



##Amazing people:
* Richard Zhao
* Jenny Wang
* Harrin Choi
* Jennifer Yang
*

##Description
This web application is designed to take feed information from the facebook group For Sale @ CMU and categorize the items in
an easily accesible and clean format.

  __Design__
  The design of the project is made to look like a typical online storefront, with the user having to login via facebook to
  interact with the site. There are multiple tabs which link to different categorizes to help navigate when searching for a
  particular item.
  Each item will be linked to it's own personal page which displays information such as price, seller, date posted.
  Each user will have an account page which lists information such as name, email, watching list, and items listed by the
  user.
  When users are looking to post or update a new item on the site, they can visit the new-item page where they can add the
  name, description, price, and photo of the item.

  When an user is interested in an item, they can click on the item page and select the option to contact the seller, this
  will mark the item as being on hold until the seller reaches back. Once an agreement is reached, the seller can mark the
  item as sold which will be updated in our online store front.

  __Additional Features__
  * 'eye' - user is keeping tabs on an item which shows up in a "watching" list for the user.
  * 'recommend' - user can tag another user to notify them of a particular item.
  * 'follow' - user can follow another user or group account to have more direct access to items they post.

The purpose of this application is to simplify the shopping and selling process for CMU students.

