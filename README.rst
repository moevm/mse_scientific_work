=====
IS Scientific work
=====

Quick start
-----------

1. Add "scientificWork" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'scientificWork',
      )

2. Include the polls URLconf in your project urls.py like this::

      url(r'^scientificWork/', include('scientificWork.urls')),

3. Run `python manage.py syncdb` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/scientificWork/ to participate in the poll.