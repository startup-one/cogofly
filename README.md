# cogofly

---->>Delete env folder from your project
---->>Open your project folder in command prompt.. In that install virtual environment
---->>Install Virtual environment and activate that in our project folder by using follow link, we have commands in that page
		https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

	---->>py -m pip --version			::Installing pip
	---->>py -m pip install --upgrade pip	   	::Upgrading pip
	---->>py -m pip install --user virtualenv	::Installing virtualenv
	---->>py -m venv env				::Creating virtual environment
	---->>.\env\Scripts\activate			::Activating it in our folder

---->>Installing all packages by using following command	
		---->>pip install -r requirements_base.txt
				while running that, If you get any errors like
					Running setup.py install for rcssmin ... error   ....Search it in google,
		Below we have the link,to solve those errors		
			https://github.com/django-compressor/django-compressor/issues/807

			pip install rcssmin --install-option="--without-c-extensions"
			pip install rjsmin --install-option="--without-c-extensions"
			pip install django-compressor --upgrade

---->>Again, run this command
		pip install -r requirements_base.txt

---->>python manage.py makemigrations
---->>python manage.py migrate
---->>python manage.py runserver

